import sys
import secrets
import hashlib
import binascii

from fido2.hid import CtapHidDevice
from fido2.client import Fido2Client
from fido2.webauthn import PublicKeyCredentialCreationOptions, PublicKeyCredentialRequestOptions

def connect(domain="https://localhost", aaguid=None):
    for dev in CtapHidDevice.list_devices():
        client = Fido2Client(dev, domain)
        if not aaguid or aaguid == client.info.aaguid.hex():
          if "hmac-secret" in client.info.extensions:
            return client

        client.close()
    else:
        print("No Authenticator with the HmacSecret extension found!")
        sys.exit(-1)

def create_credential(client, token, host="localhost", silent=False):
    rp = {"id": host, "name": "TOTP Token"}
    user = {"id": token.encode(), "name": "%s token" % token}

    challenge = secrets.token_bytes(32)

    options = PublicKeyCredentialCreationOptions(
        rp,
        user,
        challenge,
        [{"type": "public-key", "alg": -8}, {"type": "public-key", "alg": -7}],
        extensions={"hmacCreateSecret": True},
        authenticator_selection={"require_resident_key": True},
    )

    if not silent:
      print("Please press security key to create new credential")

    result = client.make_credential(options)

    credential = result.attestation_object.auth_data.credential_data
    credential_id = credential.credential_id

    return credential_id.hex()

def get_secret(client, credential_id, password, host="localhost", silent=False):
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
        extensions={"hmacGetSecret": {"salt1": salt}}
    )

    if not silent:
      print("Please press security key to get assertion")

    response = client.get_assertion(options).get_response(0)

    return response.extension_results["hmacGetSecret"]["output1"]

