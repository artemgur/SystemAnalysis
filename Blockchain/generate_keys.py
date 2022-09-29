import sys

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption


def generate_keys(filename_private: str, filename_public: str):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key_bytes = private_key.private_bytes(encoding=Encoding.PEM, format=PrivateFormat.PKCS8,
                                                  encryption_algorithm=NoEncryption())
    with open(filename_private, 'wb') as file:
        file.write(private_key_bytes)

    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
    with open(filename_public, 'wb') as file:
        file.write(public_key_bytes)


if __name__ == '__main__':
    generate_keys(sys.argv[1], sys.argv[2])
