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
from binascii import hexlify, unhexlify
import datetime
import json
import os
import struct
import threading
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from . import utils
from .exceptions import (
  CertificateVerificationError,
  NotACertificateSigningRequest,
)

__all__ = ('CertificateAuthority', 'UserCertificateAuthority', 'Extension')

_cryptography_backend = default_backend()
_AUTO_SIGNED_NO = 0
_AUTO_SIGNED_YES = 1
_AUTO_SIGNED_PASSTHROUGH = 2
_SUBJECT_OID_DICT = {
  'C' : x509.oid.NameOID.COUNTRY_NAME,
  'O' : x509.oid.NameOID.ORGANIZATION_NAME,
  'OU': x509.oid.NameOID.ORGANIZATIONAL_UNIT_NAME,
  'ST': x509.oid.NameOID.STATE_OR_PROVINCE_NAME,
  'CN': x509.oid.NameOID.COMMON_NAME,
  'L' : x509.oid.NameOID.LOCALITY_NAME,
  'SN': x509.oid.NameOID.SURNAME,
  'GN': x509.oid.NameOID.GIVEN_NAME,
}
_BACKUP_MAGIC = b'caucase\0'
_CONFIG_NAME_AUTO_SIGN_CSR_AMOUNT = 'auto_sign_csr_amount'

DEFAULT_BACKUP_SYMETRIC_CIPHER = 'aes256_cbc_pkcs7_hmac_10M_sha256'

def Extension(value, critical):
  """
  Avoid oid redundant parameter when creating an extension.
  """
  return x509.Extension(
    oid=value.oid,
    critical=critical,
    value=value,
  )

class CertificateAuthority(object):
  """
  This class implements CA policy and lifetime logic:
  - how CA key pair is generated
  - what x509.3 extensions and attributes are enforced on signed certificates
  - CA and CRL automated renewal
  """
  def __init__(
    self,
    storage,
    ca_subject_dict=(),
    ca_extension_list=(),
    ca_key_size=2048,
    crt_life_time=31 * 3, # Approximately 3 months
    ca_life_period=4, # Approximately a year
    crl_renew_period=0.33, # Approximately a month
    crl_base_url=None,
    digest_list=utils.DEFAULT_DIGEST_LIST,
    auto_sign_csr_amount=0,
    lock_auto_sign_csr_amount=False,
  ):
    """
    storage (caucase.storage.Storage)
      Persistent storage of certificate authority data.

    ca_subject_dict (dict)
      Items to use as Certificate Authority certificate subject.
      Supported keys are: C, O, OU, ST, CN, L, SN, GN.

    ca_extension_list (list of cryptography.x509.Extension)
      Extensions to apply to Certificate Authority certificae besides:
      Basic Constraints and Key Usage. See Extension helper function in
      this module.

    ca_key_size (int, None)
      Number of bits to use as Certificate Authority key.
      None to disable CA renewal.

    crt_life_time (float)
      Validity duration for every issued certificate, in days.

    ca_life_period (float)
      Number of crt_life_time periods for which Certificate Authority
      certificate will be valid.
      Must be greater than 3 to allow smooth rollout.

    crl_renew_period (float)
      Number of crt_life_time periods for which a revocation list is
      valid for.

    crl_base_url (str)
      The CRL distribution URL to include in signed certificates.
      None to not declare a CRL distribution point in generated certificates.
      Revocations are be functional even if this is None.

    digest_list (list of str)
      List of digest algorithms considered acceptable for authenticating
      renewal and revocation requests, and CA renewal list responses.
      The first item will be the one used, others are accepted but not used.

    auto_sign_csr_amount (int)
      Automatically sign the first <auto_sign_csr_amount> CSRs.
      As certificate gets unconditionally emitted and only vital attributes
      and extensions are forced during signature, you should choose the
      smallest amount possible to get a functional service.
      For a typical HTTP(S) caucase service, 1 should be enough for CAS usage
      (first service certificate being to serve HTTPS for caucase), and 1 for
      CAU usage (first user, which can then sign more user certificate
      requests).
      To verify nothing accessed the service before intended automated
      requests, check issued certificate has an extension with OID:
        2.25.285541874270823339875695650038637483517.0
      (a message is printed when retrieving the certificate)
      This mark is propagated during certificate renewal.

    lock_auto_sign_csr_amount (bool)
      When given with a true value, auto_sign_csr_amount is stored and the
      value given on later instanciation will be ignored.
    """
    self._current_crl_dict = {}
    self._storage = storage
    self._ca_renewal_lock = threading.Lock()
    if lock_auto_sign_csr_amount:
      storage.setConfigOnce(
        _CONFIG_NAME_AUTO_SIGN_CSR_AMOUNT,
        auto_sign_csr_amount,
      )
    self._auto_sign_csr_amount = int(storage.getConfigOnce(
      _CONFIG_NAME_AUTO_SIGN_CSR_AMOUNT,
      auto_sign_csr_amount,
    ))

    self._ca_key_size = ca_key_size
    self._digest_list = digest_list
    self._default_digest_class = getattr(hashes, self.digest_list[0].upper())
    self._crt_life_time = datetime.timedelta(crt_life_time, 0)
    self._crl_base_url = crl_base_url
    self._ca_subject = x509.Name([
      x509.NameAttribute(
        oid=_SUBJECT_OID_DICT[key],
        value=value,
      )
      for key, value in dict(ca_subject_dict).iteritems()
    ])
    self._ca_extension_list = list(ca_extension_list)
    if ca_life_period < 3:
      raise ValueError("ca_life_period must be >= 3 to allow CA rollout")
    self._crl_life_time = datetime.timedelta(
      crt_life_time * crl_renew_period,
      0,
    )
    self._crl_renew_time = datetime.timedelta(
      crt_life_time * crl_renew_period * .5,
      0,
    )
    self._ca_life_time = datetime.timedelta(crt_life_time * ca_life_period, 0)
    self._loadCAKeyPairList()
    self._renewCAIfNeeded()

  @property
  def digest_list(self):
    """
    Read-only access to digest_list ctor parameter.
    """
    return list(self._digest_list)

  def _loadCAKeyPairList(self):
    digest = self._digest_list[0]
    ca_key_pair_list = []
    ca_certificate_chain = []
    previous_crt_pem = None
    previous_key = None
    for pem_key_pair in self._storage.getCAKeyPairList():
      utils.validateCertAndKey(
        pem_key_pair['crt_pem'],
        pem_key_pair['key_pem'],
      )
      crt_pem = pem_key_pair['crt_pem']
      crt = utils.load_ca_certificate(pem_key_pair['crt_pem'])
      key = utils.load_privatekey(pem_key_pair['key_pem'])
      ca_key_pair_list.append({
        'crt': crt,
        'key': key,
        'authority_key_identifier': utils.getAuthorityKeyIdentifier(crt),
      })
      if previous_key is not None:
        ca_certificate_chain.append(utils.wrap(
          {
            'old_pem': utils.toUnicode(previous_crt_pem),
            'new_pem': utils.toUnicode(crt_pem),
          },
          previous_key,
          digest,
        ))
      previous_crt_pem = crt_pem
      previous_key = key
    self._current_crl_dict.clear()
    self._ca_key_pairs_list = ca_key_pair_list
    self._ca_certificate_chain = tuple(
      ca_certificate_chain
    )

  def getCertificateSigningRequest(self, csr_id):
    """
    Retrieve a PEM-encoded certificate signing request.

    csr_id (int)
      As returned when the CSR was stored.
    """
    return self._storage.getCertificateSigningRequest(csr_id)

  def appendCertificateSigningRequest(self, csr_pem, override_limits=False):
    """
    Store certificate signing request and return its identifier.
    May trigger its signature if the quantity of submitted CSRs is less than
    auto_sign_csr_amount (see __init__).

    csr_pem (str)
      PEM-encoded certificate signing request.
    """
    try:
      csr = utils.load_certificate_request(csr_pem)
    except ValueError:
      raise NotACertificateSigningRequest
    # Note: requested_amount is None when a known CSR is re-submitted
    csr_id, requested_amount = self._storage.appendCertificateSigningRequest(
      csr_pem=csr_pem,
      key_id=hexlify(x509.SubjectKeyIdentifier.from_public_key(
        csr.public_key(),
      ).digest),
      override_limits=override_limits,
    )
    if requested_amount is not None and \
    requested_amount <= self._auto_sign_csr_amount:
      # if allowed to sign this certificate automaticaly
      self._createCertificate(csr_id, auto_signed=_AUTO_SIGNED_YES)
    return csr_id

  def deletePendingCertificateSigningRequest(self, csr_id):
    """
    Reject a pending certificate signing request.

    csr_id (int)
      CSR id, as returned when the CSR was stored.
    """
    self._storage.deletePendingCertificateSigningRequest(csr_id)

  def getCertificateRequestList(self):
    """
    Return the list of pending certificate signature requests, individually
    PEM-encoded.
    """
    return self._storage.getCertificateSigningRequestList()

  def createCertificate(self, csr_id, template_csr=None):
    """
    Sign a pending certificate signing request, storing produced certificate.

    csr_id (int)
      CSR id, as returned when the CSR was stored.
    template_csr (None or X509Req)
      Copy extensions and subject from this CSR instead of stored one.
      Useful to renew a certificate.
      Public key is always copied from stored CSR.
    """
    self._createCertificate(
      csr_id=csr_id,
      auto_signed=_AUTO_SIGNED_NO,
      template_csr=template_csr,
    )

  def _createCertificate(self, csr_id, auto_signed, template_csr=None):
    """
    auto_signed (bool)
      When True, mark certificate as having been auto-signed.
      When False, prevent such mark from being set.
      When None, do not filter (useful when renewing).
    tempate_csr (None or X509Req)
      Copy extensions and subject from this CSR instead of stored one.
      Useful to renew a certificate.
      Public key is always copied from stored CSR.
    """
    csr_pem = self._storage.getCertificateSigningRequest(csr_id)
    csr = utils.load_certificate_request(csr_pem)
    if template_csr is None:
      template_csr = csr
    ca_key_pair = self._getCurrentCAKeypair()
    ca_crt = ca_key_pair['crt']

    public_key = csr.public_key()
    now = datetime.datetime.utcnow()
    builder = x509.CertificateBuilder(
      subject_name=template_csr.subject,
      issuer_name=ca_crt.subject,
      not_valid_before=now,
      not_valid_after=now + self._crt_life_time,
      serial_number=x509.random_serial_number(),
      public_key=public_key,
      extensions=[
        Extension(
          x509.BasicConstraints(
            ca=False,
            path_length=None,
          ),
          critical=True, # "MAY appear as critical or non-critical"
        ),
        Extension(
          x509.SubjectKeyIdentifier.from_public_key(
            public_key,
          ),
          critical=False, # "MUST mark this extension as non-critical"
        ),
        Extension(
          ca_crt.extensions.get_extension_for_class(
            x509.AuthorityKeyIdentifier,
          ).value,
          critical=False, # "MUST mark this extension as non-critical"
        ),
      ],
    )
    if self._crl_base_url:
      builder = builder.add_extension(
        x509.CRLDistributionPoints([
          x509.DistributionPoint(
            full_name=[
              x509.UniformResourceIdentifier(
                self._crl_base_url + (
                  '/%i' % (
                    utils.getAuthorityKeyIdentifier(ca_crt),
                  )
                ),
              ),
            ],
            relative_name=None,
            crl_issuer=None,
            reasons=None,
          ),
        ]),
        critical=False, # "SHOULD be non-critical"
      )
    try:
      key_usage_extension = template_csr.extensions.get_extension_for_class(
        x509.KeyUsage,
      )
    except x509.ExtensionNotFound:
      pass
    else:
      key_usage = key_usage_extension.value
      if key_usage.key_agreement:
        encipher_only = key_usage.encipher_only
        decipher_only = key_usage.decipher_only
      else:
        encipher_only = decipher_only = False
      builder = builder.add_extension(
        x509.KeyUsage(
          digital_signature =key_usage.digital_signature,
          content_commitment=key_usage.content_commitment,
          key_encipherment  =key_usage.key_encipherment,
          data_encipherment =key_usage.data_encipherment,
          key_agreement     =key_usage.key_agreement,
          key_cert_sign     =False,
          crl_sign          =False,
          encipher_only     =encipher_only,
          decipher_only     =decipher_only,
        ),
        # "SHOULD mark this extension critical"
        critical=key_usage_extension.critical,
      )
    try:
      extended_key_usage = template_csr.extensions.get_extension_for_class(
        x509.ExtendedKeyUsage,
      )
    except x509.ExtensionNotFound:
      pass
    else:
      builder = builder.add_extension(
        x509.ExtendedKeyUsage(
          [
            x for x in extended_key_usage.value
            if x != x509.oid.ExtendedKeyUsageOID.OCSP_SIGNING
          ]
        ),
        critical=extended_key_usage.critical,
      )
    try:
      subject_alt_name = template_csr.extensions.get_extension_for_class(
        x509.SubjectAlternativeName,
      )
    except x509.ExtensionNotFound:
      pass
    else:
      # Note: as issued certificates may be used without any subject
      # validation (ex: connecting to mariadb via a variable IP), we
      # voluntarily do not enforce any constraint on subjectAltName.
      builder = builder.add_extension(
        subject_alt_name.value,
        critical=subject_alt_name.critical,
      )
    # subjectDirectoryAttributes ?
    try:
      certificate_policies = template_csr.extensions.get_extension_for_class(
        x509.CertificatePolicies,
      )
    except x509.ExtensionNotFound:
      if auto_signed == _AUTO_SIGNED_YES:
        builder = builder.add_extension(
          x509.CertificatePolicies([
            utils.CAUCASE_POLICY_INFORMATION_AUTO_SIGNED,
          ]),
          critical=False, # (no recommendations)
        )
    else:
      policy_list = []
      for policy in certificate_policies.value:
        if policy.policy_identifier.dotted_string.startswith(
          utils.CAUCASE_LEGACY_OID_TOP
        ):
          # Always migrate CAUCASE_LEGACY_OID_TOP to CAUCASE_OID_TOP
          # by copying current policy and replacing its prefix to the new
          # OID prefix
          identifier_suffix = policy.policy_identifier.dotted_string[
            len(utils.CAUCASE_LEGACY_OID_TOP):
          ]
          policy = x509.PolicyInformation(
            x509.oid.ObjectIdentifier(utils.CAUCASE_OID_TOP + identifier_suffix),
            policy.policy_qualifiers,
          )
        policy_list.append(policy)

      if auto_signed != _AUTO_SIGNED_PASSTHROUGH:
        # Prevent any caucase extension from being smuggled, especially the
        # "auto-signed" one...
        policy_list = [
          x for x in policy_list
          if not x.policy_identifier.dotted_string.startswith(
            utils.CAUCASE_OID_TOP,
          )
        ]
        if auto_signed == _AUTO_SIGNED_YES:
          # ...but do add auto-signed extension if we are auto-signing.
          policy_list.append(utils.CAUCASE_POLICY_INFORMATION_AUTO_SIGNED)
      builder = builder.add_extension(
        x509.CertificatePolicies(policy_list),
        critical=certificate_policies.critical, # (no recommendations)
      )

    cert_pem = utils.dump_certificate(builder.sign(
      private_key=ca_key_pair['key'],
      algorithm=self._default_digest_class(),
      backend=_cryptography_backend,
    ))
    self._storage.storeCertificate(csr_id, cert_pem)
    return cert_pem

  def getCertificate(self, csr_id):
    """
    Return PEM-encoded signed certificate.

    csr_id (int)
      As returned when the corresponding CSR was stored.
    """
    return self._storage.getCertificate(csr_id)

  def _renewCAIfNeeded(self):
    """
    Create a new CA certificate if latest one has less than two
    ca_life_periods of validity left.
    Updates self._ca_key_pairs_list .
    """
    if (
      self._ca_key_size is not None and not self._ca_key_pairs_list or (
        self._ca_key_pairs_list[-1]['crt'].not_valid_after -
        datetime.datetime.utcnow()
      ).total_seconds() / self._crt_life_time.total_seconds() <= 2
    ) and self._ca_renewal_lock.acquire(False):
      try:
        # No CA certificate at all or less than 2 certificate validity periods
        # left with latest CA certificate. Prepare the next one so it starts
        # getting distributed.
        private_key = rsa.generate_private_key(
          public_exponent=65537,
          key_size=self._ca_key_size,
          backend=_cryptography_backend,
        )
        if self._ca_key_pairs_list:
          latest_crt = self._ca_key_pairs_list[-1]['crt']
          subject = latest_crt.subject
          extension_list = latest_crt.extensions
        else:
          # Provide a default subject extension set.
          subject = self._ca_subject
          extension_list = [
            Extension(
              x509.BasicConstraints(
                ca=True,
                path_length=0,
              ),
              critical=True, # "MUST mark the extension as critical"
            ),
            Extension(
              x509.KeyUsage(
                digital_signature =False,
                content_commitment=False,
                key_encipherment  =False,
                data_encipherment =False,
                key_agreement     =False,
                key_cert_sign     =True,
                crl_sign          =True,
                encipher_only     =False,
                decipher_only     =False,
              ),
              critical=True, # "SHOULD mark this extension critical"
            ),
          ] + self._ca_extension_list
        public_key = private_key.public_key()
        now = datetime.datetime.utcnow()
        crt_builder = x509.CertificateBuilder(
          subject_name=subject,
          issuer_name=subject,
          not_valid_before=now,
          not_valid_after=now + self._ca_life_time,
          serial_number=x509.random_serial_number(),
          public_key=public_key,
          extensions=[
            Extension(
              x509.SubjectKeyIdentifier.from_public_key(public_key),
              critical=False, # "MUST mark this extension as non-critical"
            ),
            Extension(
              x509.AuthorityKeyIdentifier.from_issuer_public_key(public_key),
              critical=False, # "MUST mark this extension as non-critical"
            ),
          ],
        )
        # Copy all extensions, except the ones which depend on the key (and
        # which we just set).
        skipped_extension_oid_set = (
          x509.SubjectKeyIdentifier.oid,
          x509.AuthorityKeyIdentifier.oid,
        )
        for extension in extension_list:
          if extension.oid not in skipped_extension_oid_set:
            crt_builder = crt_builder.add_extension(
              extension.value,
              extension.critical,
            )
        certificate = crt_builder.sign(
          private_key=private_key,
          algorithm=self._default_digest_class(),
          backend=_cryptography_backend,
        )
        self._storage.appendCAKeyPair(
          utils.datetime2timestamp(certificate.not_valid_after),
          {
            'key_pem': utils.dump_privatekey(private_key),
            'crt_pem': utils.dump_certificate(certificate),
          },
        )
        self._loadCAKeyPairList()
        assert self._ca_key_pairs_list
      finally:
        self._ca_renewal_lock.release()

  def _getCurrentCAKeypair(self):
    """
    Return the currently-active CA certificate key pair.

    Currently-active CA certificate is the CA to use when signing. It may not
    be the latest one, as all certificate holders must know the latest one
    before its use can start.
    """
    self._renewCAIfNeeded()
    now = datetime.datetime.utcnow()
    for key_pair in reversed(self._ca_key_pairs_list):
      if key_pair['crt'].not_valid_before + self._crt_life_time < now:
        # This CA cert is valid for more than one certificate life time,
        # we can assume clients to know it (as they had to renew their
        # cert at least once since it became available) so we can start
        # using it.
        break
    else:
      # No CA cert is valid for more than one certificate life time, so just
      # pick the newest one.
      key_pair = self._ca_key_pairs_list[-1]
    return key_pair

  def getCACertificate(self):
    """
    Return oldest still-valid CA certificate, PEM-encoded.
    """
    self._renewCAIfNeeded()
    # XXX: _loadCAKeyPairList seems a bit too expensive for such simple operation.
    # So do out-of-storage self._ca_key_pairs_list pruning only.
    now = datetime.datetime.utcnow()
    while self._ca_key_pairs_list[0]['crt'].not_valid_after <= now:
      self._ca_key_pairs_list.pop(0)
    return utils.dump_certificate(self._ca_key_pairs_list[0]['crt'])

  def getCACertificateList(self):
    """
    Return the current list of CA certificates as X509 obbjects.
    """
    self._renewCAIfNeeded()
    return [x['crt'] for x in self._ca_key_pairs_list]

  def getValidCACertificateChain(self):
    """
    Return the CA certificate chain based on oldest CA certificate.

    Each item in the chain is a wrapped dict with the following keys:
    old (str)
      N-1 certificate as PEM, used to check wrapper signature.
      If item is the first in the chain, this is the oldest CA certificate
      server still knows about.
    new (str)
      N certificate as PEM.

    The intent is for a client knowing one CA certificate to retrieve any newer
    CA certificate and autonomously decide if it may trust them: each item is
    signed with the previous certificate. The oldest CA certificate is not
    returned in this list, as it cannot be signed by another one.

    CA user must check that there is an uninterrupted signed path from its
    already-known CA certificate to use any contained "new" certificate.
    It must skip any certificate pair for which it does not already trust
    an ancestor certificate.

    Note: the chain may contain expired CA certificates. CA user should skip
    these, and consider their signature invalid for CA chain validation
    purposes.
    """
    self._renewCAIfNeeded()
    return self._ca_certificate_chain

  def revoke(self, crt_pem):
    """
    Revoke certificate.

    crt_pem (str)
      PEM-encoded certificat to revoke.
    """
    crt = utils.load_certificate(
      crt_pem,
      self.getCACertificateList(),
      crl_list=[
        x509.load_pem_x509_crl(x, _cryptography_backend)
        for x in self.getCertificateRevocationListDict().itervalues()
      ],
    )
    self._storage.revoke(
      serial=crt.serial_number,
      expiration_date=utils.datetime2timestamp(
        # https://tools.ietf.org/html/rfc5280#section-3.3
        # An entry MUST NOT be removed
        # from the CRL until it appears on one regularly scheduled CRL issued
        # beyond the revoked certificate's validity period.
        crt.not_valid_after + self._crl_life_time,
      ),
    )
    self._current_crl_dict.clear()

  def revokeSerial(self, serial):
    """
    Revoke a certificate by its serial only.

    Revocation will expire when the latest CA certificate of this instance
    expires, meaning it will stay longer in the revocation list than when
    certificate expiration date can be retrieved from the certificate.

    Also, there cannot be any check on the validity of the serial, typos
    are accepted verbatim.

    Using this method is hence not recomended.
    """
    self._storage.revoke(
      serial=serial,
      expiration_date=utils.datetime2timestamp(
        max(
          x.not_valid_after for x in self.getCACertificateList()
        ) + self._crl_life_time,
      ),
    )
    self._current_crl_dict.clear()

  def renew(self, crt_pem, csr_pem):
    """
    Renew certificate.

    crt_pem (str)
      PEM-encoded certificate to renew.
    csr_pem (str)
      PEM-encoded certificate signing request.
    """
    crt = utils.load_certificate(
      crt_pem,
      self.getCACertificateList(),
      crl_list=[
        x509.load_pem_x509_crl(x, _cryptography_backend)
        for x in self.getCertificateRevocationListDict().itervalues()
      ],
    )
    return self._createCertificate(
      csr_id=self.appendCertificateSigningRequest(
        csr_pem,
        override_limits=True,
      ),
      auto_signed=_AUTO_SIGNED_PASSTHROUGH,
      # Do a dummy signature, just so we get a usable
      # x509.CertificateSigningRequest instance. Use latest CA private key just
      # because it is available for free (unlike generating a new one).
      template_csr=x509.CertificateSigningRequestBuilder(
        subject_name=crt.subject,
        extensions=crt.extensions,
      ).sign(
        private_key=self._ca_key_pairs_list[-1]['key'],
        algorithm=self._default_digest_class(),
        backend=_cryptography_backend,
      ),
    )

  def getCertificateRevocationListDict(self):
    """
    Return PEM-encoded certificate revocation lists for all CAs.
    """
    now = datetime.datetime.utcnow()
    result = {}
    crl_pem_dict = self._current_crl_dict
    self._renewCAIfNeeded()
    storage = self._storage
    crl_number, last_update = storage.getCurrentCRLNumberAndLastUpdate()
    has_renewed = last_update is None
    last_update = (
      None
      if last_update is None else
      utils.timestamp2datetime(last_update)
    )
    revoked_certificate_list = None
    for ca_key_pair in self._ca_key_pairs_list:
      authority_key_identifier = ca_key_pair['authority_key_identifier']
      try:
        crl_pem, crl_expiration_date = crl_pem_dict[authority_key_identifier]
      except KeyError:
        crl_pem = None
      if crl_pem is None or crl_expiration_date < now:
        if not has_renewed and crl_pem is not None:
          # CRL expired, generate a new serial
          last_update = None
          has_renewed = True
        if (
          last_update is None or
          last_update + self._crl_renew_time < now
        ):
          # We cannot use the existing CRL (or maybe none exist), generate a
          # new one.
          last_update = now
          crl_number = storage.getNextCertificateRevocationListNumber()
          storage.storeCRLLastUpdate(
            last_update=utils.datetime2timestamp(last_update),
          )
        if revoked_certificate_list is None:
          revoked_certificate_list = [
            x509.RevokedCertificateBuilder(
              serial_number=x['serial'],
              revocation_date=utils.timestamp2datetime(x['revocation_date']),
            ).build(_cryptography_backend)
            for x in storage.getRevocationList()
          ]
        ca_crt = ca_key_pair['crt']
        crl_pem = x509.CertificateRevocationListBuilder(
          issuer_name=ca_crt.issuer,
          last_update=last_update,
          next_update=last_update + self._crl_life_time,
          extensions=[
            Extension(
              x509.CRLNumber(crl_number),
              critical=False, # "MUST mark this extension as non-critical"
            ),
            Extension(
              ca_crt.extensions.get_extension_for_class(
                x509.AuthorityKeyIdentifier,
              ).value,
              critical=False, # No mention in RFC5280 5.2.1
            ),
          ],
          revoked_certificates=revoked_certificate_list,
        ).sign(
          private_key=ca_key_pair['key'],
          algorithm=self._default_digest_class(),
          backend=_cryptography_backend,
        ).public_bytes(serialization.Encoding.PEM)
        crl_pem_dict[authority_key_identifier] = (
          crl_pem,
          last_update + self._crl_renew_time,
        )
      result[authority_key_identifier] = crl_pem
    return result

class UserCertificateAuthority(CertificateAuthority):
  """
  Backup-able CertificateAuthority.

  See backup schema in documentation.
  """
  # Note to developers: dict structure can and will change
  __backup_format_dict = {
    'aes256_cbc_pkcs7_hmac_10M_sha256': 10 * 1024 * 1024,
    # For tests only, to exercise block boundaries
    'TESTS_INTERNAL_USE_ONLY': 32,
  }

  def doBackup(self, write):
    """
    Backup the entire storage to given path, enciphering it using all stored
    certificates.
    """
    ca_cert_list = self.getCACertificateList()
    crl_list = [
      x509.load_pem_x509_crl(x, _cryptography_backend)
      for x in self.getCertificateRevocationListDict().itervalues()
    ]
    signing_key = os.urandom(32)
    symetric_key = os.urandom(32)
    iv = os.urandom(16)
    encryptor = Cipher(
      algorithms.AES(symetric_key),
      modes.CBC(iv),
      backend=_cryptography_backend,
    ).encryptor()
    authenticator = hmac.HMAC(
      signing_key,
      hashes.SHA256(),
      backend=_cryptography_backend,
    )
    symetric_cipher_name = DEFAULT_BACKUP_SYMETRIC_CIPHER
    HMAC_PAYLOAD_SIZE = self.__backup_format_dict[symetric_cipher_name]
    key_list = []
    for crt_pem in self._storage.iterCertificates():
      try:
        crt = utils.load_certificate(crt_pem, ca_cert_list, crl_list)
      except CertificateVerificationError:
        continue
      public_key = crt.public_key()
      key_list.append({
        'id': utils.toUnicode(hexlify(
          x509.SubjectKeyIdentifier.from_public_key(public_key).digest,
        )),
        'cipher': {
          'name': 'rsa_oaep_sha1_mgf1_sha1',
        },
        'key': utils.toUnicode(hexlify(public_key.encrypt(
          signing_key + symetric_key,
          OAEP(
            mgf=MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
          ),
        ))),
      })
    if not key_list:
      # No users yet, backup is meaningless
      return False
    header = utils.toBytes(json.dumps({
      'cipher': {
        'name': symetric_cipher_name,
        'parameter': utils.toUnicode(hexlify(iv)),
      },
      'key_list': key_list,
    }))
    padder = padding.PKCS7(128).padder()
    write(_BACKUP_MAGIC)
    write(struct.pack('<I', len(header)))
    write(header)
    def signingIterator():
      """
      Iterate over cleartext dump, inserting HMAC between each chunk.
      """
      buf = b''
      for chunk in self._storage.dumpIterator():
        buf += chunk
        while len(buf) >= HMAC_PAYLOAD_SIZE:
          chunk = buf[:HMAC_PAYLOAD_SIZE]
          buf = buf[HMAC_PAYLOAD_SIZE:]
          authenticator.update(chunk)
          yield chunk
          yield authenticator.copy().finalize()
      if buf:
        authenticator.update(buf)
        yield buf
        yield authenticator.finalize()
      else: # pragma: no cover
        pass
    for chunk in signingIterator():
      write(encryptor.update(padder.update(chunk)))
    write(encryptor.update(padder.finalize()))
    write(encryptor.finalize())
    return True

  @classmethod
  def restoreBackup(
    cls,
    db_class,
    db_path,
    read,
    key_pem,
    csr_pem,
    db_kw=(),
    kw=(),
  ):
    """
    Restore backup, revoke certificate corresponding to private key and sign
    its renewal.
    """
    magic = read(len(_BACKUP_MAGIC))
    if magic != _BACKUP_MAGIC:
      raise ValueError('Invalid backup magic string')
    header_len, = struct.unpack(
      '<I',
      read(struct.calcsize('<I')),
    )
    header = json.loads(utils.toUnicode(read(header_len)))
    symetric_cipher_name = header['cipher']['name']
    try:
      HMAC_PAYLOAD_SIZE = cls.__backup_format_dict[symetric_cipher_name]
    except KeyError:
      raise ValueError('Unrecognised symetric cipher')
    private_key = utils.load_privatekey(key_pem)
    key_id = hexlify(x509.SubjectKeyIdentifier.from_public_key(
      private_key.public_key(),
    ).digest)
    symetric_key_list = [
      x for x in header['key_list'] if utils.toBytes(x['id']) == key_id
    ]
    if not symetric_key_list:
      raise ValueError(
        'Given private key is not a good candidate for restoring this backup',
      )
    symetric_key_entry, = symetric_key_list
    if symetric_key_entry['cipher']['name'] != 'rsa_oaep_sha1_mgf1_sha1':
      raise ValueError('Unrecognised asymetric cipher')
    both_keys = private_key.decrypt(
      unhexlify(symetric_key_entry['key']),
      OAEP(
        mgf=MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None,
      ),
    )
    if len(both_keys) != 64:
      raise ValueError('Invalid key length')
    decryptor = Cipher(
      algorithms.AES(both_keys[32:]),
      modes.CBC(unhexlify(header['cipher']['parameter'])),
      backend=_cryptography_backend,
    ).decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    authenticator = hmac.HMAC(
      both_keys[:32],
      hashes.SHA256(),
      backend=_cryptography_backend,
    )
    # Each block has its signature
    HMAC_SIGNED_SIZE = HMAC_PAYLOAD_SIZE + 32
    CHUNK_SIZE = HMAC_SIGNED_SIZE
    def restorator():
      """
      Iterate over backup payload, decyphering by small chunks.
      """
      while True:
        chunk = read(CHUNK_SIZE)
        if chunk:
          yield unpadder.update(decryptor.update(chunk))
        else:
          yield unpadder.update(decryptor.finalize()) + unpadder.finalize()
          break
    def verificator():
      """
      Iterate over decrypted payload, verifying HMAC on each chunk.
      """
      buf = b''
      for clear in restorator():
        buf += clear
        while len(buf) >= HMAC_SIGNED_SIZE:
          signed = buf[:HMAC_SIGNED_SIZE]
          buf = buf[HMAC_SIGNED_SIZE:]
          chunk = signed[:-32]
          authenticator.update(chunk)
          authenticator.copy().verify(signed[-32:])
          yield chunk
      if buf:
        chunk = buf[:-32]
        authenticator.update(chunk)
        authenticator.verify(buf[-32:])
        yield chunk
      else: # pragma: no cover
        pass

    db_class.restore(db_path=db_path, restorator=verificator())

    # Now that the database is restored, use a CertificateAuthority to
    # renew & revoke given private key.
    self = cls(storage=db_class(db_path=db_path, **dict(db_kw)), **dict(kw))
    # pylint: disable=protected-access
    crt_pem = self._storage.getCertificateByKeyIdentifier(key_id)
    # pylint: enable=protected-access
    new_crt_pem = self.renew(crt_pem, csr_pem)
    self.revoke(crt_pem)
    return new_crt_pem
