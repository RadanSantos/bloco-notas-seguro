from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)

with open("chave_privada.pem", "wb") as f:
    f.write(privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("chave_publica.pem", "wb") as f:
    f.write(privada.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("✅ Chaves geradas com sucesso.")