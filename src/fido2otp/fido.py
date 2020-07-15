import sys
import secrets
import hashlib
import binascii

from fido2.hid import CtapHidDevice
from fido2.client import Fido2Client
from fido2.extensions import HmacSecretExtension
from fido2.webauthn import PublicKeyCredentialCreationOptions, PublicKeyCredentialRequestOptions

def connect(domain="https://localhost", aaguid=None):
    for dev in CtapHidDevice.list_devices():
        client = Fido2Client(dev, domain)
        if not aaguid or aaguid == client.info.aaguid.hex():
          if HmacSecretExtension.NAME in client.info.extensions:
            return client

        client.close()
    else:
        print("No Authenticator with the HmacSecret extension found!")
        sys.exit(-1)

def create_credential(client, token, host="localhost", silent=False):
    rp = {"id": host, "name": "TOTP Token"}
    user = {"id": token.encode(), "name": "%s token" % token}

    challenge = secrets.token_bytes(32)

    hmac_ext = HmacSecretExtension(client.ctap2)

    options = PublicKeyCredentialCreationOptions(
        rp,
        user,
        challenge,
        [{"type": "public-key", "alg": -8}, {"type": "public-key", "alg": -7}],
        extensions=hmac_ext.create_dict(),
        authenticator_selection={"require_resident_key": True},
    )

    if not silent:
      print("Please press security key to create new credential")

    attestation_object, client_data = client.make_credential(options)

    credential = attestation_object.auth_data.credential_data
    credential_id = credential.credential_id

    return credential_id.hex()

def get_secret(client, credential_id, password, host="localhost", silent=False):
    hmac_ext = HmacSecretExtension(client.ctap2)
    credential_id = binascii.a2b_hex(credential_id)

    allow_list = [{"type": "public-key", "id": credential_id}]

    challenge = secrets.token_bytes(32)

    h = hashlib.sha256()
    h.update(password)
    salt = h.digest()

    options = PublicKeyCredentialRequestOptions(
        challenge,
        30000,
        host,
        allow_list,
        extensions=hmac_ext.get_dict(salt)
    )

    if not silent:
      print("Please press security key to get assertion")

    assertions, client_data = client.get_assertion(options)

    assertion = assertions[0]
    response = hmac_ext.results_for(assertion.auth_data)[0]

    return response

