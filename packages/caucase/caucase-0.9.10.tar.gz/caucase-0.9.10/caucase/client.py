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
import httplib
import json
import ssl
from urlparse import urlparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import cryptography.exceptions
import pem
from . import exceptions
from . import utils
from . import version

__all__ = (
  'CaucaseError',
  'CaucaseHTTPError',
  'CaucaseSSLError',
  'CaucaseClient',
  'HTTPSOnlyCaucaseClient',
)

_cryptography_backend = default_backend()

class CaucaseError(Exception):
  """
  Base error for errors when communicating with a caucase server.
  """
  pass

class CaucaseHTTPError(CaucaseError):
  """
  Raised when server responds with an HTTP error status.
  """
  pass

class CaucaseSSLError(CaucaseError):
  """
  Raised when there is an SSL error while communicating with the server.
  """
  pass

class CaucaseClient(object):
  """
  Caucase HTTP(S) client.

  Expose caucase REST API as pythonic methods.
  """
  HTTPConnection = httplib.HTTPConnection
  HTTPSConnection = httplib.HTTPSConnection

  @classmethod
  def updateCAFile(cls, url, ca_crt_path):
    """
    Bootstrap and maintain a CA file up-to-date.

    url (str)
      URL to caucase, ending in eithr /cas or /cau.
    ca_crt_path (str)
      Path to the CA certificate file or directory, which may not exist.
      If it does not exist, it is created. If there is an extension, a file is
      created, otherwise a directory is.

    Return whether an update happened (including whether an already-known
    certificate expired and was discarded).
    """
    loaded_ca_pem_list = utils.getCertList(ca_crt_path)
    if not loaded_ca_pem_list:
      with cls(ca_url=url) as client:
        utils.saveCertList(ca_crt_path, [client.getCACertificate()])
      updated = True
      # Note: reloading from file instead of using ca_pem, to exercise the
      # same code path as future executions, to apply the same checks.
      loaded_ca_pem_list = utils.getCertList(ca_crt_path)
    else:
      updated = False
    ca_pem_list = []
    for loaded_ca_pem in loaded_ca_pem_list:
      try:
        utils.load_ca_certificate(loaded_ca_pem)
      except exceptions.CertificateVerificationError:
        continue
      else:
        ca_pem_list.append(loaded_ca_pem)
    with cls(ca_url=url, ca_crt_pem_list=ca_pem_list) as client:
      ca_pem_list.extend(client.getCACertificateChain())
    if ca_pem_list != loaded_ca_pem_list:
      utils.saveCertList(ca_crt_path, ca_pem_list)
      updated = True
    return updated

  @classmethod
  def updateCRLFile(cls, url, crl_path, ca_list):
    """
    Bootstrap anf maintain a CRL file up-to-date.

    url (str)
      URL to caucase, ending in eithr /cas or /cau.
    crl_path (str)
      Path to the CRL file or directory, which may not exist.
      If it does not exist, it is created. If there is an extension, a file is
      created, otherwise a directory is.
    ca_list (list of cryptography.x509.Certificate instances)
      One of these CA certificates must have signed the CRL for it to be
      accepted.

    Return whether an update happened.
    """
    def _asCRLDict(crl_pem_list):
      result = {}
      for crl_pem in crl_pem_list:
        try:
          crl = utils.load_crl(crl_pem, ca_list)
        except cryptography.exceptions.InvalidSignature:
          continue
        else:
          result[utils.getAuthorityKeyIdentifier(crl)] = crl_pem
      return result
    local_crl_list = utils.getCRLList(crl_path)
    try:
      local_crl_dict = _asCRLDict(crl_pem_list=local_crl_list)
    except x509.extensions.ExtensionNotFound:
      # BBB: caucased used to issue CRLs without the AuthorityKeyIdentifier
      # extension. In such case, local CRLs need to be replaced.
      local_crl_list = []
      local_crl_dict = {}
      updated = True
    else:
      updated = len(local_crl_list) != len(local_crl_dict)
    with cls(ca_url=url) as client:
      server_crl_list = client.getCertificateRevocationListList()
    for ca_key_id, crl_pem in _asCRLDict(
      crl_pem_list=server_crl_list,
    ).iteritems():
      updated |= local_crl_dict.pop(ca_key_id, None) != crl_pem
    updated |= bool(local_crl_dict)
    if updated:
      utils.saveCRLList(crl_path, server_crl_list)
    return updated

  def __init__(
    self,
    ca_url,
    ca_crt_pem_list=None,
    user_key=None,
    http_ca_crt_pem_list=None,
  ):
    # XXX: set timeout to HTTP connections ?
    http_url = urlparse(ca_url)
    port = http_url.port or 80
    self._http_connection = self.HTTPConnection(
      http_url.hostname,
      port,
      #timeout=,
    )
    self._ca_crt_pem_list = ca_crt_pem_list
    self._path = http_url.path
    ssl_context = ssl.create_default_context(
      # unicode object needed as we use PEM, otherwise create_default_context
      # expects DER.
      cadata=(
        utils.toUnicode(''.join(http_ca_crt_pem_list))
        if http_ca_crt_pem_list
        else None
      ),
    )
    if http_ca_crt_pem_list: # pragma: no cover
      pass
    else:
      ssl_context.check_hostname = False
      ssl_context.verify_mode = ssl.CERT_NONE
    if user_key:
      try:
        ssl_context.load_cert_chain(user_key)
      except ssl.SSLError as exc:
        raise ValueError('Failed to load user key: %r' % (exc, ))
    self._https_connection = self.HTTPSConnection(
      http_url.hostname,
      443 if port == 80 else port + 1,
      #timeout=,
      context=ssl_context,
    )

  def _request(self, connection, method, url, body=None, headers=None):
    path = self._path + url
    headers = headers or {}
    headers.setdefault('User-Agent', 'caucase ' + version.__version__)
    try:
      connection.request(method, path, body, headers)
      response = connection.getresponse()
      response_body = response.read()
    except ssl.SSLError as exc:
      raise CaucaseSSLError(exc.errno, exc.strerror)
    if response.status >= 400:
      raise CaucaseHTTPError(
        response.status,
        response.getheaders(),
        response_body,
      )
    assert response.status < 300 # caucase does not redirect
    if response.status == 201:
      return response.getheader('Location')
    return response_body

  def _http(self, method, url, body=None, headers=None):
    return self._request(self._http_connection, method, url, body, headers)

  def _https(self, method, url, body=None, headers=None):
    return self._request(self._https_connection, method, url, body, headers)

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()

  def close(self):
    """
    Close any open connection.
    """
    self._http_connection.close()
    self._https_connection.close()

  def getCertificateRevocationList(self, authority_key_identifier):
    """
    [ANONYMOUS] Retrieve latest CRL for given integer authority key
    identifier.
    """
    return self._http(
      'GET',
      '/crl/%i' % (authority_key_identifier, ),
    )

  def getCertificateRevocationListList(self):
    """
    [ANONYMOUS] Retrieve the latest CRLs for each CA certificate.
    """
    return [
      x.as_bytes()
      for x in pem.parse(self._http('GET', '/crl'))
      if isinstance(x, pem.CertificateRevocationList)
    ]

  def getCertificateSigningRequest(self, csr_id):
    """
    [ANONYMOUS] Retrieve an CSR by its identifier.
    """
    return self._http('GET', '/csr/%i' % (csr_id, ))

  def getPendingCertificateRequestList(self):
    """
    [AUTHENTICATED] Retrieve all pending CSRs.
    """
    return json.loads(self._https('GET', '/csr').decode('utf-8'))

  def createCertificateSigningRequest(self, csr):
    """
    [ANONYMOUS] Store a CSR and return its identifier.
    """
    return int(self._http('PUT', '/csr', csr, {
      'Content-Type': 'application/pkcs10',
    }))

  def deletePendingCertificateRequest(self, csr_id):
    """
    [AUTHENTICATED] Reject a pending CSR.
    """
    self._https('DELETE', '/csr/%i' % (csr_id, ))

  def _getCertificate(self, crt_id):
    return self._http('GET', '/crt' + crt_id)

  def getCertificate(self, csr_id):
    """
    [ANONYMOUS] Retrieve CRT by its identifier (same as corresponding CRL
    identifier).
    """
    return self._getCertificate('/%i' % (csr_id, ))

  def getCACertificate(self):
    """
    [ANONYMOUS] Retrieve current CA certificate.
    """
    return self._getCertificate('/ca.crt.pem')

  def getCACertificateChain(self):
    """
    [ANONYMOUS] Retrieve CA certificate chain, with CA certificate N+1 signed
    by CA certificate N, allowing automated CA cert rollout.
    """
    found = False
    previous_ca = trust_anchor = sorted(
      (
        utils.load_ca_certificate(x)
        for x in self._ca_crt_pem_list
      ),
      key=lambda x: x.not_valid_before,
    )[-1]
    result = []
    for entry in json.loads(
      self._getCertificate('/ca.crt.json').decode('utf-8'),
    ):
      try:
        payload = utils.unwrap(
          entry,
          lambda x: x['old_pem'],
          utils.DEFAULT_DIGEST_LIST,
        )
      except cryptography.exceptions.InvalidSignature:
        continue
      if not found:
        found = utils.load_ca_certificate(
          utils.toBytes(payload['old_pem']),
        ) == trust_anchor
      if found:
        if utils.load_ca_certificate(
          utils.toBytes(payload['old_pem']),
        ) != previous_ca:
          raise ValueError('CA signature chain broken')
        new_pem = utils.toBytes(payload['new_pem'])
        result.append(new_pem)
        previous_ca = utils.load_ca_certificate(new_pem)
    return result

  def renewCertificate(self, old_crt, old_key, key_len):
    """
    [ANONYMOUS] Request certificate renewal.
    """
    new_key = utils.generatePrivateKey(key_len=key_len)
    return (
      utils.dump_privatekey(new_key),
      self._http(
        'PUT',
        '/crt/renew',
        json.dumps(
          utils.wrap(
            {
              'crt_pem': utils.toUnicode(utils.dump_certificate(old_crt)),
              'renew_csr_pem': utils.toUnicode(utils.dump_certificate_request(
                x509.CertificateSigningRequestBuilder(
                ).subject_name(
                  # Note: caucase server ignores this, but cryptography
                  # requires CSRs to have a subject.
                  old_crt.subject,
                ).sign(
                  private_key=new_key,
                  algorithm=utils.DEFAULT_DIGEST_CLASS(),
                  backend=_cryptography_backend,
                ),
              )),
            },
            old_key,
            utils.DEFAULT_DIGEST,
          ),
        ).encode('utf-8'),
        {'Content-Type': 'application/json'},
      ),
    )

  def revokeCertificate(self, crt, key=None):
    """
    Revoke certificate.
    [ANONYMOUS] if key is provided.
    [AUTHENTICATED] if key is missing.
    """
    crt = utils.toUnicode(crt)
    if key:
      method = self._http
      data = utils.wrap(
        {
          'revoke_crt_pem': crt,
        },
        utils.load_privatekey(key),
        utils.DEFAULT_DIGEST,
      )
    else:
      method = self._https
      data = utils.nullWrap({
        'revoke_crt_pem': crt,
      })
    method(
      'PUT',
      '/crt/revoke',
      json.dumps(data).encode('utf-8'),
      {'Content-Type': 'application/json'},
    )

  def revokeSerial(self, serial):
    """
    Revoke certificate by serial.

    This method is dangerous ! Prefer revokeCRT whenever possible.

    [AUTHENTICATED]
    """
    self._https(
      'PUT',
      '/crt/revoke',
      json.dumps(utils.nullWrap({'revoke_serial': serial})).encode('utf-8'),
      {'Content-Type': 'application/json'},
    )

  def createCertificate(self, csr_id, template_csr=''):
    """
    [AUTHENTICATED] Sign certificate signing request.
    """
    header_dict = {}
    if template_csr:
      header_dict['Content-Type'] = 'application/pkcs10'
    self._https('PUT', '/crt/%i' % (csr_id, ), template_csr, header_dict)

class HTTPSOnlyCaucaseClient(CaucaseClient):
  """
  Like CaucaseClient, but forces anonymous accesses to go through HTTPS as
  well.
  """
  def __init__(self, *args, **kw):
    super(HTTPSOnlyCaucaseClient, self).__init__(*args, **kw)
    self._http_connection = self._https_connection
