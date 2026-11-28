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

## 🧪 Testes de Qualidade e Segurança (QA)
Para garantir a integridade e a privacidade dos dados, o projeto conta com uma suíte de testes automatizados usando a biblioteca `unittest`.

Os testes cobrem:
- **Fluxo de Ida e Volta:** Verifica se a mensagem criptografada pode ser lida corretamente com a chave certa.
- **Acesso Negado:** Simula uma tentativa de invasão usando uma chave privada falsa (o sistema deve bloquear).
- **Adulteração de Arquivo:** Altera intencionalmente um único bit do arquivo `.enc` para provar que o algoritmo AES-GCM detecta a fraude e impede a leitura.

**Como rodar os testes no seu computador:**
```bash
python test_seguranca.py

## 📄 Licenciamento

Este projeto é distribuído sob **Licença Dupla (Dual Licensing)**:
*   **MIT License:** Para uso livre, permissivo e flexível (ideal para uso pessoal e educacional).
*   **GNU GPLv3:** Para garantir que quaisquer modificações ou derivações deste projeto permaneçam de código aberto.

Você pode escolher a licença que melhor se adequar às suas necessidades. Consulte os arquivos `LICENSE` e `LICENSE-GPL` para mais detalhes.

**⚠️ Aviso Ético:** O autor não compactua com o uso deste software para atividades ilegais, como extorsão ou invasão de privacidade. O uso é de inteira responsabilidade do usuário.