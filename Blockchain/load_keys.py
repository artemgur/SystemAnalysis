from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


def load_private_key(filename: str):
    with open(filename, 'rb') as file:
        file_contents = file.read()
    return load_pem_private_key(file_contents, password=None)


def load_public_key(filename: str):
    with open(filename, 'rb') as file:
        file_contents = file.read()
    return load_pem_public_key(file_contents)
