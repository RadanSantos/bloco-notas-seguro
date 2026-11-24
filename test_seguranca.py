import unittest
import os
import io
from bloco_seguro import criptografar_dados, descriptografar_dados
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.exceptions import InvalidTag

class TestSeguranca(unittest.TestCase):

    def setUp(self):
        # Cria um par de chaves para o teste
        self.chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.chave_publica = self.chave_privada.public_key()
        self.mensagem_original = b"Esta e uma mensagem super secreta para teste!"

    def test_ida_e_volta(self):
        """Testa se a mensagem criptografada pode ser descriptografada corretamente."""
        enc = criptografar_dados(self.mensagem_original, self.chave_publica)
        dec = descriptografar_dados(enc, self.chave_privada)
        self.assertEqual(self.mensagem_original, dec)

    def test_chave_errada(self):
        """Testa se o sistema bloqueia a leitura com uma chave privada diferente."""
        enc = criptografar_dados(self.mensagem_original, self.chave_publica)
        chave_falsa = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        
        # O sistema deve lançar um erro (ValueError) ao tentar abrir
        with self.assertRaises(ValueError):
            descriptografar_dados(enc, chave_falsa)

    def test_adulteracao(self):
        """Testa se a criptografia detecta se alguém alterou o arquivo."""
        enc = criptografar_dados(self.mensagem_original, self.chave_publica)
        
        # Adultera o último byte do arquivo (onde fica o texto criptografado)
        enc_adulterado = bytearray(enc)
        enc_adulterado[-1] = enc_adulterado[-1] ^ 0xFF 
        
        # O sistema deve recusar o arquivo alterado
        with self.assertRaises(Exception): 
            descriptografar_dados(bytes(enc_adulterado), self.chave_privada)

if __name__ == '__main__':
    unittest.main()