from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

print("1. Gerando chaves...")
privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
publica = privada.public_key()

print("2. Criptografando...")
chave_aes = AESGCM.generate_key(bit_length=256)
chave_cifrada = publica.encrypt(
    chave_aes,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

print("3. Descriptografando...")
chave_recuperada = privada.decrypt(
    chave_cifrada,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

if chave_aes == chave_recuperada:
    print("✅ SUCESSO! A biblioteca está funcionando perfeitamente.")
else:
    print("❌ FALHA! A biblioteca está corrompida.")