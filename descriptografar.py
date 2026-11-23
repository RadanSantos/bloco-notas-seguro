import sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

with open("chave_privada.pem", "rb") as f:
    chave_privada = serialization.load_pem_private_key(f.read(), password=None)

with open(sys.argv[1], "rb") as f:
    dados = f.read()

tam_chave = int.from_bytes(dados[:2], "big")
chave_cifrada = dados[2:2 + tam_chave]
nonce = dados[2 + tam_chave:2 + tam_chave + 12]
texto_cifrado = dados[2 + tam_chave + 12:]

chave_aes = chave_privada.decrypt(
    chave_cifrada,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

mensagem = AESGCM(chave_aes).decrypt(nonce, texto_cifrado, None)

with open(sys.argv[2], "wb") as f:
    f.write(mensagem)

print(f"🔓 Mensagem salva em: {sys.argv[2]}")