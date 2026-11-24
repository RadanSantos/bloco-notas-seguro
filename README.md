# 🔐 Bloco de Notas Seguro (Criptografia RSA + AES)

Este projeto é uma aplicação desktop desenvolvida em Python que permite criptografar mensagens de texto, fotos e vídeos curtos. A segurança é baseada em criptografia híbrida (AES-256-GCM e RSA-2048), garantindo que apenas o destinatário (dono da chave privada) consiga abrir o conteúdo.

## 🚀 Funcionalidades
- Interface gráfica amigável (Tkinter) estilo bloco de notas.
- Criptografia híbrida de alta segurança.
- Suporte para anexos (compactação em ZIP em memória antes da criptografia).

- Geração automatizada de chaves públicas e privadas.

## 🛠️ Tecnologias Utilizadas
- **Python 3**
- **Tkinter** (Interface Gráfica)
- **Cryptography** (Biblioteca de segurança)
- **Zipfile & Io** (Manipulação de arquivos em memória)

## ⚙️ Como executar
1. Clone o repositório.
2. Instale as dependências: `pip install cryptography`
3. Gere suas chaves: `python gerar_chaves.py`
4. Execute o app: `python bloco_seguro.py`

## 🧠 Desafios Técnicos Superados
Durante o desenvolvimento, enfrentei e resolvi os seguintes problemas:
- **Criptografia Híbrida:** Como o RSA não consegue criptografar arquivos grandes (como fotos), implementei a arquitetura onde o RSA criptografa apenas uma chave AES, e o AES criptografa o arquivo em si.
- **Manipulação em Memória:** Para não deixar rastros no disco rígido, utilizei `io.BytesIO` e `zipfile` para compactar as fotos e o texto na memória RAM antes de criptografar.
- **Erros de SSL no Pip:** Tive que contornar bloqueios de certificados de segurança da minha rede durante a instalação da biblioteca `cryptography`.
- **Gerenciamento de Chaves:** Compreensão prática da diferença entre chaves públicas (compartilháveis) e privadas (segredo absoluto).