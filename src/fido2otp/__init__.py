import sys
import click
import pyotp
import getpass

from fido2otp import fido
from fido2otp import crypt
from fido2otp import keyring

@click.group()
def cli():
  pass

@cli.command()
@click.argument('name')
@click.argument('token')
@click.option('--force', '-f', is_flag=True, default=False, help='Force replace existing token')
@click.option('--silent', '-s', is_flag=True, default=False, help='Quiet mode. No key press notification')
@click.option('--collection', '-c', default='fido2otp', help='Keyring to store the secret in')
@click.option('--aaguid', '-a', help='Target security key AAGUID')
def push(name, token, force, silent, collection, aaguid=None):
    password = getpass.getpass(prompt='Password: ')
    if not password or len(password) < 8:
      print("error: password too short")
      sys.exit(-1)

    if keyring.get_secret(name, collection) and not force:
      print("error: secret already exists")
      sys.exit(-1)

    client = fido.connect(aaguid=aaguid)
    credential_id = fido.create_credential(client, name, silent=silent)
    key = fido.get_secret(client, credential_id, password.encode(), silent=silent)

    encrypted = crypt.encrypt(token, key)

    keyring.set_secret(name, credential_id, encrypted, password, client.info.aaguid.hex(), collection)

@cli.command()
@click.argument('name')
@click.option('--silent', '-s', is_flag=True, default=False, help='Quiet mode')
@click.option('--collection', '-c', default='fido2otp', help='Keyring to load the secret from')
def get(name, collection, silent):
    secret = keyring.get_secret(name, collection)

    if not secret:
      print("error: secret %s not found", name)
      sys.exit(-1)

    attributes = secret.get_attributes()

    credential_id = attributes["id"]
    aaguid = attributes["aaguid"]
    client = fido.connect(aaguid=aaguid)

    key = fido.get_secret(client, credential_id, secret.get_secret(), silent=silent)

    totp = pyotp.TOTP(crypt.decrypt(attributes["token"], key))
    print(totp.now())

