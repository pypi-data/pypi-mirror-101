# This file is part of caucase
# Copyright (C) 2017-2020  Nexedi SA
#     Alain Takoudjou <alain.takoudjou@nexedi.com>
#     Vincent Pelletier <vincent@nexedi.com>
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.
"""
Caucase - Certificate Authority for Users, Certificate Authority for SErvices
"""
from __future__ import absolute_import
from random import getrandbits
import os
import sqlite3
from threading import local
from time import time
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from .exceptions import NoStorage, NotFound, Found
from .utils import toBytes, toUnicode, datetime2timestamp

__all__ = ('SQLite3Storage', )

_cryptography_backend = default_backend()
DAY_IN_SECONDS = 60 * 60 * 24

class NoReentryConnection(sqlite3.Connection):
  """
  Refuse to start an already started transaction.

  Allows detecting code bugs which would lead to non-atomic updates (partial
  outer transaction getting committed by an inner transaction).
  """
  __entered = False

  def __enter__(self):
    if self.__entered: # pragma: no cover
      raise Exception('Subtransactions are not supported')
    self.__entered = True
    return super(NoReentryConnection, self).__enter__()

  def __exit__(self, exc_type, exc_value, traceback):
    self.__entered = False
    return super(NoReentryConnection, self).__exit__(exc_type, exc_value, traceback)

class SQLite3Storage(local):
  """
  CA data storage.

  Every cryptographic type this class deals with must be PEM-encoded.
  """
  def __init__(
    self,
    db_path,
    table_prefix,
    max_csr_amount=50,
    crt_keep_time=1,
    crt_read_keep_time=0.05, # About 1 hour
    enforce_unique_key_id=False,
    mode=0o600,
  ):
    """
    db_path (str)
      SQLite connection string.
    table_prefix (str)
      Name to use as a prefix for all tables managed by this storage adapter.
      Allows sharing the database, although it should only be within the same
      caucase process for access permission reasons.
    max_csr_amount (int)
      Maximum number of allowed pending certificate signing requests.
      To prevent flood.
    crt_keep_time (float)
      Time to keep signed certificates for, in days.
    crt_read_keep_time (float)
      Time to keep CRT content for after it was first read, in days.
      Allows requester to fail retrieving the certificate by tolerating
      retries.
    enforce_unique_key_id (bool)
      When true, certificate requests cannot be appended if there is already
      and known entry for the same private key.
      Note: this only makes sense if crt_keep_time and crt_read_keep_time are
      set at least to the certificate life span.
      Useful for backups, to ensure the certificate to revoke can be uniquely
      identified from the key used to decrypt the backup archive.
    mode (int)
      Permissions of the main database file upon creation.
    """
    super(SQLite3Storage, self).__init__()
    # Create database file if it does not exist, so mode can be controlled.
    os.close(os.open(
      db_path,
      os.O_CREAT | os.O_RDONLY,
      mode,
    ))
    self._db = db = sqlite3.connect(db_path, factory=NoReentryConnection)
    self._table_prefix = table_prefix
    db.row_factory = sqlite3.Row
    self._max_csr_amount = max_csr_amount
    self._crt_keep_time = crt_keep_time * DAY_IN_SECONDS
    self._crt_read_keep_time = crt_read_keep_time * DAY_IN_SECONDS
    with db:
      # Note about revoked.serial: certificate serials exceed the 63 bits
      # sqlite can accept as integers, so store these as text. Use a trivial
      # string serialisation: not very space efficient, but this should not be
      # a limiting issue for our use-cases anyway.
      c = db.cursor()
      c.executescript('''
        CREATE TABLE IF NOT EXISTS %(prefix)sca (
          expiration_date INTEGER,
          key TEXT,
          crt TEXT
        );
        CREATE TABLE IF NOT EXISTS %(prefix)scrt (
          id INTEGER PRIMARY KEY,
          key_id TEXT %(key_id_constraint)s,
          expiration_date INTEGER,
          csr TEXT,
          crt TEXT
        );
        CREATE TABLE IF NOT EXISTS %(prefix)srevoked (
          serial TEXT PRIMARY KEY,
          revocation_date INTEGER,
          expiration_date INTEGER
        );
        CREATE TABLE IF NOT EXISTS %(prefix)scounter (
          name TEXT PRIMARY KEY,
          value INTEGER
        );
        CREATE TABLE IF NOT EXISTS %(prefix)sconfig_once (
          name TEXT PRIMARY KEY,
          value TEXT
        );
        CREATE TABLE IF NOT EXISTS %(prefix)sconfig (
          name TEXT PRIMARY KEY,
          value TEXT
        );
      ''' % {
        'prefix': table_prefix,
        'key_id_constraint': 'UNIQUE' if enforce_unique_key_id else '',
      })
      try:
        crl_row = self._executeSingleRow(
          'SELECT crl FROM %(prefix)scrl '
          'ORDER BY expiration_date DESC LIMIT 1',
        )
      except sqlite3.OperationalError as exc:
        # XXX: no error codes in sqlite and only a generic error class ?
        if not exc.args[0].startswith('no such table: '): # pragma: no cover
          raise
        crl_row = None
      if crl_row is not None:
        self._setConfig(
          'crl_last_update',
          str(datetime2timestamp(x509.load_pem_x509_crl(
            toBytes(crl_row['crl']),
            _cryptography_backend,
          ).last_update)),
        )
        self._execute(c, 'DROP TABLE IF EXISTS %(prefix)scrl')

  def _execute(self, cursor, sql, parameters=()):
    return cursor.execute(
      sql % {
        'prefix': self._table_prefix,
      },
      parameters,
    )

  def _incrementCounter(self, name, increment=1, initial=0):
    """
    Increment counter with <name> by <increment> and return resulting value.
    If <name> is not found, it is created with <initial>, and then incremented.
    Does not commit.
    """
    row = self._executeSingleRow(
      'SELECT value FROM %(prefix)scounter WHERE name = ? LIMIT 2',
      (name, ),
    )
    if row is None:
      value = initial
    else:
      value = row['value']
    value += increment
    self._execute(
      self._db.cursor(),
      'INSERT OR REPLACE INTO %(prefix)scounter (name, value) VALUES (?, ?)',
      (name, value),
    )
    return value

  def _executeSingleRow(self, sql, parameters=()):
    """
    Execute <sql>, raise if it produces more than 1 row, and return it.
    """
    result_list = self._execute(self._db.cursor(), sql, parameters).fetchall()
    if result_list:
      result, = result_list
      return result
    return None

  def getConfigOnce(self, name, default):
    """
    Retrieve the value of <name> from config-once list, or <default> if not
    stored.
    """
    with self._db:
      result = self._executeSingleRow(
        'SELECT value FROM %(prefix)sconfig_once WHERE name = ?',
        (name, ),
      )
    if result is None:
      return default
    return result['value']

  def setConfigOnce(self, name, value):
    """
    Store <value> as <name> in config-once list, if it was not already stored.
    If it was already stored, do nothing.
    """
    try:
      with self._db as db:
        self._execute(
          db.cursor(),
          'INSERT INTO %(prefix)sconfig_once (name, value) VALUES (?, ?)',
          (name, value),
        )
    except sqlite3.IntegrityError:
      pass

  def _getConfig(self, name, default):
    """
    Retrieve the value of <name> from config list, or <default> if not
    stored.
    """
    result = self._executeSingleRow(
      'SELECT value FROM %(prefix)sconfig WHERE name = ?',
      (name, ),
    )
    if result is None:
      return default
    return result['value']

  def _setConfig(self, name, value):
    """
    Store <value> as <name> in config list, possibly overwriting an existing
    entry.
    """
    self._execute(
      self._db.cursor(),
      'INSERT OR REPLACE INTO %(prefix)sconfig (name, value) VALUES (?, ?)',
      (name, value),
    )

  def getCAKeyPairList(self, prune=True):
    """
    Return the chronologically sorted (oldest in [0], newest in [-1])
    certificate authority key pairs.
    """
    with self._db as db:
      c = db.cursor()
      if prune:
        self._execute(
          c,
          'DELETE FROM %(prefix)sca WHERE expiration_date < ?',
          (time(), ),
        )
      return [
        {
          'crt_pem': toBytes(x['crt']),
          'key_pem': toBytes(x['key']),
        }
        for x in self._execute(
          c,
          'SELECT key, crt FROM %(prefix)sca ORDER BY expiration_date ASC',
        ).fetchall()
      ]

  def appendCAKeyPair(self, expiration_timestamp, key_pair):
    """
    Store a certificate authority key pair.
    expiration_timestamp (int)
      Unix GMT timestamp of CA certificate "valid until" date.
    key_pair (dict with 'key_pem' and 'crt_pem' items)
      CA key pair to store, as bytes.
    """
    with self._db as db:
      self._execute(
        db.cursor(),
        'INSERT INTO %(prefix)sca '
        '(expiration_date, key, crt) VALUES (?, ?, ?)',
        (
          expiration_timestamp,
          key_pair['key_pem'],
          key_pair['crt_pem'],
        ),
      )

  def appendCertificateSigningRequest(
    self,
    csr_pem,
    key_id,
    override_limits=False,
  ):
    """
    Store acertificate signing request and generate a unique ID for it.
    Note: ID uniqueness is only guaranteed among pending CSR, and may be reused
    after the original CSR has been discarded (by being rejected or signed).
    """
    with self._db as db:
      known_csr = self._executeSingleRow(
        'SELECT id FROM %(prefix)scrt WHERE csr = ? LIMIT 2',
        (csr_pem, ),
      )
      if known_csr is not None:
        return known_csr['id'], None
      if override_limits:
        # Ignore max pending count
        # Do not increment the number of auto-signed certificates, but do not
        # automatically sign either.
        requested_count = None
      else:
        if self._executeSingleRow(
          'SELECT COUNT(*) FROM %(prefix)scrt WHERE crt IS NULL',
        )[0] >= self._max_csr_amount:
          raise NoStorage
        requested_count = self._incrementCounter('received_csr')
      csr_id = getrandbits(63)
      c = db.cursor()
      self._execute(
        c,
        'INSERT INTO %(prefix)scrt (id, key_id, csr) VALUES (?, ?, ?)',
        (
          csr_id,
          key_id,
          csr_pem,
        ),
      )
      self._execute(
        c,
        'DELETE FROM %(prefix)scrt WHERE expiration_date < ?',
        (time(), ),
      )
      return csr_id, requested_count

  def deletePendingCertificateSigningRequest(self, csr_id):
    """
    Forget about a pending CSR. Does nothing if the CSR was already signed
    (it will be automatically garbage-collected later).
    Raises NotFound if there is no matching CSR.
    """
    with self._db as db:
      c = db.cursor()
      self._execute(
        c,
        'DELETE FROM %(prefix)scrt WHERE id = ? AND crt IS NULL',
        (csr_id, ),
      )
      if c.rowcount == 1:
        return
      raise NotFound

  def getCertificateSigningRequest(self, csr_id):
    """
    Retrieve a PEM-encoded certificate signing request.

    csr_id (int)
      Desired CSR id, as given when the CSR was stored.

    Raises NotFound if there is no matching CSR.
    """
    with self._db:
      result = self._executeSingleRow(
        'SELECT csr FROM %(prefix)scrt WHERE id = ?',
        (csr_id, ),
      )
      if result is None:
        raise NotFound
      return toBytes(result['csr'])

  def getCertificateSigningRequestList(self):
    """
    Return the list of all pending CSRs.

    Ignores any CSR for which a certificate was issued.
    """
    with self._db as db:
      return [
        {
          'id': str(x['id']),
          # XXX: because only call chain will end up serialising this value in
          # json, and for some reason python3 json module refuses bytes.
          # So rather than byte-ify (consistently with all PEM-encoded values)
          # to then have to unicode-ify, just unicode-ify here.
          'csr': toUnicode(x['csr']),
        }
        for x in self._execute(
          db.cursor(),
          'SELECT id, csr FROM %(prefix)scrt WHERE crt IS NULL',
        ).fetchall()
      ]

  def storeCertificate(self, csr_id, crt):
    """
    Store certificate for pre-existing CSR.

    Raises NotFound if there is no matching CSR, or if a certificate was
    already stored.
    """
    with self._db as db:
      c = db.cursor()
      self._execute(
        c,
        'UPDATE %(prefix)scrt SET crt=?, expiration_date = ? '
        'WHERE id = ? AND crt IS NULL',
        (
          crt,
          int(time() + self._crt_keep_time),
          csr_id,
        ),
      )
      if c.rowcount == 0:
        raise NotFound

  def getCertificate(self, crt_id):
    """
    Retrieve a PEM-encoded certificate.

    crt_id (int)
      Desired certificate id, which is the same as corresponding CSR's id.

    Raises NotFound if there is no matching CRT or if no certificate was issued
    for it.
    """
    with self._db as db:
      row = self._executeSingleRow(
        'SELECT crt, expiration_date FROM %(prefix)scrt '
        'WHERE id = ? AND crt IS NOT NULL',
        (crt_id, ),
      )
      if row is None:
        raise NotFound
      new_expiration_date = int(time() + self._crt_read_keep_time)
      if row['expiration_date'] > new_expiration_date:
        self._execute(
          db.cursor(),
          'UPDATE %(prefix)scrt SET expiration_date = ? WHERE id = ?',
          (
            new_expiration_date,
            crt_id,
          )
        )
      return toBytes(row['crt'])

  def getCertificateByKeyIdentifier(self, key_id):
    """
    Return the certificate corresponding to given key_id.

    Raises NotFound if there is no matching CRT or if no certificate was issued
    for it.
    """
    with self._db:
      row = self._executeSingleRow(
        'SELECT crt FROM %(prefix)scrt WHERE key_id = ? AND crt IS NOT NULL',
        (key_id, ),
      )
      if row is None:
        raise NotFound
      return toBytes(row['crt'])

  def iterCertificates(self):
    """
    Iterator over stored certificates.
    """
    with self._db as db:
      c = db.cursor()
      self._execute(
        c,
        'SELECT crt FROM %(prefix)scrt WHERE crt IS NOT NULL',
      )
      while True:
        row = c.fetchone()
        if row is None:
          break
        yield toBytes(row['crt'])

  def revoke(self, serial, expiration_date):
    """
    Add given certificate serial to the list of revoked certificates.
    Flushes any current CRL.

    serial (int)
      Serial of the certificate to revoke.
    expiration_date (int)
      Unix timestamp at which the certificate expires, allowing to remove this
      entry from the CRL.
    """
    with self._db as db:
      c = db.cursor()
      try:
        self._execute(
          c,
          'INSERT INTO %(prefix)srevoked '
          '(serial, revocation_date, expiration_date) '
          'VALUES (?, ?, ?)',
          (
            str(serial),
            int(time()),
            expiration_date,
          ),
        )
      except sqlite3.IntegrityError:
        raise Found
      self._incrementCounter('crl_number')

  def getNextCertificateRevocationListNumber(self):
    """
    Get next CRL sequence number.
    """
    with self._db:
      return self._incrementCounter('crl_number')

  def storeCRLLastUpdate(self, last_update):
    """
    Get next CRL sequence number.
    """
    with self._db:
      self._setConfig('crl_last_update', str(last_update))

  def storeCRLNumber(self, crl_number):
    """
    Set the current CRL sequence number.
    Use only when importing an existing CA.
    """
    with self._db as db:
      self._execute(
        db.cursor(),
        'INSERT OR REPLACE INTO %(prefix)scounter (name, value) VALUES (?, ?)',
        (
          'crl_number',
          crl_number,
        ),
      )

  def getCurrentCRLNumberAndLastUpdate(self):
    """
    Get the current CRL sequence number.
    """
    with self._db:
      last_update = self._getConfig('crl_last_update', None)
      return (
        # Note: does not increment the counter, but may set it to the default
        # value.
        self._incrementCounter('crl_number', increment=0),
        (
          last_update
          if last_update is None else
          int(last_update, 10)
        ),
      )

  def getRevocationList(self):
    """
    Get the list of all revoked certificates.

    Returns a list of dicts, each containing:
    - revocation_date (int)
      Unix timestamp of certificate revocation.
    - serial (int)
      Revoked certificate's serial.
    """
    with self._db as db:
      c = db.cursor()
      self._execute(
        c,
        'DELETE FROM %(prefix)srevoked WHERE expiration_date < ?',
        (time(), ),
      )
      return [
        {
          'revocation_date': int(x['revocation_date']),
          'serial': int(x['serial']),
        }
        for x in self._execute(
          c,
          'SELECT revocation_date, serial FROM %(prefix)srevoked',
        )
      ]

  def dumpIterator(self):
    """
    Backs the *entire* dabase up. This is not limited to tables managed by this
    class (so not limited to table_prefix).
    """
    for statement in self._db.iterdump():
      yield toBytes(statement, 'utf-8') + b'\0'

  @staticmethod
  def restore(db_path, restorator):
    """
    Restores a dump which is the concatenated output of dumpIterator.
    Should not be called directly, but via
    ca.CertificateAuthority.restoreBackup .

    db_path (str)
      Path to the SQLite database to produce. Must not exist.

    restorator (iterable)
      Produces chunks which correspond (in content, not necessarily in size)
      to what dumpIterator produces.
    """
    buf = b''
    if os.path.exists(db_path):
      raise ValueError('%r exists, not restoring.' % (db_path, ))
    c = sqlite3.connect(db_path, isolation_level=None).cursor()
    for chunk in restorator:
      statement_list = (buf + chunk).split(b'\0')
      buf = statement_list.pop()
      for statement in statement_list:
        c.execute(toUnicode(statement, 'utf-8'))
    if buf:
      raise ValueError('Short read, backup truncated ?')
