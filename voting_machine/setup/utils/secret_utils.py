import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def get_secret(secret_key):
    client = get_secret_client()
    retrieved_secret = client.get_secret(secret_key)
    return retrieved_secret.value


def get_secret_client(keyVaultName=None):
    if not keyVaultName:
        keyVaultName = os.environ["KEY_VAULT_NAME"]
    KVUri = f"https://{keyVaultName}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    return client


def set_secret(secret_key, secret_val):
    client = get_secret_client()
    client.set_secret(secret_key, secret_val)
    retrieved_secret = client.get_secret(secret_key)
    if retrieved_secret == secret_val:
        return True
    return False
