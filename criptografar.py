import os
import sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

with open("chave_publica.pem", "rb") as f:
    chave_publica = serialization.load_pem_public_key(f.read())

with open(sys.argv[1], "rb") as f:
    mensagem = f.read()

chave_aes = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)
texto_cifrado = AESGCM(chave_aes).encrypt(nonce, mensagem, None)

chave_cifrada = chave_publica.encrypt(
    chave_aes,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

with open(sys.argv[2], "wb") as f:
    f.write(len(chave_cifrada).to_bytes(2, "big"))
    f.write(chave_cifrada)
    f.write(nonce)
    f.write(texto_cifrado)

print(f"🔒 Arquivo criptografado: {sys.argv[2]}")