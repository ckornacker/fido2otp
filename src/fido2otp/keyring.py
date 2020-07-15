import sys
import secretstorage

def get_collection(name):
    connection = secretstorage.dbus_init()
    collections = secretstorage.get_all_collections(connection)

    collection = next((collection for collection in collections if collection.get_label() == name), None)

    if collection == None:
      print('keyring "%s" not found, creating...' % name)
      collection = secretstorage.create_collection(connection, name)

    collection.unlock()

    return collection

def set_secret(name, credential_id, token, password, aaguid, collection):
    collection = get_collection(collection)

    items = collection.get_all_items()
    secret = next((item for item in items if item.get_label() == name), None)

    attributes = {"id":credential_id, "token":token, "aaguid":aaguid}

    if secret:
      secret.set_attributes(attributes)
      secret.set_secret(password)
    else:
      collection.create_item(name, attributes, password)

def get_secret(name, collection):
    collection = get_collection(collection)

    if collection.is_locked():
      print('error: keyring "%" is locked' % collection)
      sys.exit(-1)

    items = collection.get_all_items()
    secret = next((item for item in items if item.get_label() == name), None)

    if not secret:
      print('error: secret "%s" not found' % name)
      sys.exit(-1)

    return secret
