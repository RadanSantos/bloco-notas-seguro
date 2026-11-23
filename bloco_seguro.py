import os
import io
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ==========================================
# FUNÇÕES DE CRIPTOGRAFIA (Nos bastidores)
# ==========================================
def criptografar_dados(dados_bytes, chave_publica):
    chave_aes = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    texto_cifrado = AESGCM(chave_aes).encrypt(nonce, dados_bytes, None)
    chave_cifrada = chave_publica.encrypt(
        chave_aes,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    # Junta tudo: [tamanho da chave][chave][nonce][dados]
    return len(chave_cifrada).to_bytes(2, "big") + chave_cifrada + nonce + texto_cifrado

def descriptografar_dados(dados_arquivo, chave_privada):
    tam_chave = int.from_bytes(dados_arquivo[:2], "big")
    chave_cifrada = dados_arquivo[2:2 + tam_chave]
    nonce = dados_arquivo[2 + tam_chave:2 + tam_chave + 12]
    texto_cifrado = dados_arquivo[2 + tam_chave + 12:]
    
    chave_aes = chave_privada.decrypt(
        chave_cifrada,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return AESGCM(chave_aes).decrypt(nonce, texto_cifrado, None)

# ==========================================
# INTERFACE GRÁFICA (O Bloco de Notas)
# ==========================================
class BlocoSeguro:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloco de Notas Seguro (Criptografado)")
        self.root.geometry("600x500")
        
        self.arquivos_anexados = []
        
        # Área de Texto
        self.texto = tk.Text(self.root, wrap="word", font=("Arial", 12))
        self.texto.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Lista de Anexos
        self.lista_anexos = tk.Listbox(self.root, height=4, bg="#f0f0f0")
        self.lista_anexos.pack(padx=10, fill="x")
        
        # Botões
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=10)
        
        tk.Button(frame_botoes, text="Anexar Foto/Vídeo", command=self.anexar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="🔒 Salvar e Criptografar", command=self.salvar_cripto, bg="lightblue").pack(side="left", padx=5)
        tk.Button(frame_botoes, text="🔓 Abrir e Descriptografar", command=self.abrir_cripto, bg="lightgreen").pack(side="left", padx=5)

    def anexar(self):
        arquivos = filedialog.askopenfilenames(title="Selecione fotos ou vídeos pequenos")
        for arq in arquivos:
            self.arquivos_anexados.append(arq)
            self.lista_anexos.insert("end", os.path.basename(arq))

    def salvar_cripto(self):
        # 1. Verifica se a chave pública existe
        if not os.path.exists("chave_publica.pem"):
            messagebox.showerror("Erro", "Arquivo 'chave_publica.pem' não encontrado na pasta!")
            return
            
        with open("chave_publica.pem", "rb") as f:
            chave_publica = serialization.load_pem_public_key(f.read())

        # 2. Cria um arquivo ZIP na memória para juntar texto e arquivos
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            # Adiciona o texto
            texto_digitado = self.texto.get("1.0", "end-1c")
            zf.writestr("mensagem.txt", texto_digitado)
            
            # Adiciona as fotos/vídeos
            for caminho in self.arquivos_anexados:
                zf.write(caminho, arcname=os.path.basename(caminho))
                
        dados_zip = zip_buffer.getvalue()

        # 3. Criptografa o ZIP
        dados_criptografados = criptografar_dados(dados_zip, chave_publica)

        # 4. Pede para salvar o arquivo final
        arquivo_saida = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Arquivo Criptografado", "*.enc")])
        if arquivo_saida:
            with open(arquivo_saida, "wb") as f:
                f.write(dados_criptografados)
            messagebox.showinfo("Sucesso", "Arquivo criptografado salvo!\nAnexe este arquivo .enc no seu e-mail.")

    def abrir_cripto(self):
        # 1. Verifica se a chave privada existe
        if not os.path.exists("chave_privada.pem"):
            messagebox.showerror("Erro", "Arquivo 'chave_privada.pem' não encontrado na pasta!")
            return
            
        with open("chave_privada.pem", "rb") as f:
            chave_privada = serialization.load_pem_private_key(f.read(), password=None)

        # 2. Pede o arquivo .enc
        arquivo_enc = filedialog.askopenfilename(title="Selecione o arquivo .enc", filetypes=[("Arquivo Criptografado", "*.enc")])
        if not arquivo_enc:
            return

        try:
            with open(arquivo_enc, "rb") as f:
                dados_arquivo = f.read()

            # 3. Descriptografa e abre o ZIP na memória
            dados_zip = descriptografar_dados(dados_arquivo, chave_privada)
            
            # 4. Pergunta onde salvar a pasta com os arquivos extraídos
            pasta_saida = filedialog.askdirectory(title="Escolha a pasta para extrair o conteúdo")
            if pasta_saida:
                with zipfile.ZipFile(io.BytesIO(dados_zip)) as zf:
                    zf.extractall(pasta_saida)
                    
                # Lê o texto para mostrar na tela
                if "mensagem.txt" in zf.namelist():
                    texto_lido = zf.read("mensagem.txt").decode("utf-8")
                    self.texto.delete("1.0", "end")
                    self.texto.insert("1.0", texto_lido)
                    
                messagebox.showinfo("Sucesso", f"Mensagem e anexos extraídos para:\n{pasta_saida}")
                
        except Exception as e:
            messagebox.showerror("Erro", "Falha ao descriptografar. Chave privada incorreta ou arquivo corrompido.")

# Inicia o aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = BlocoSeguro(root)
    root.mainloop()