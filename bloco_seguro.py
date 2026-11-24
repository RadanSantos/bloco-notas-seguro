import os
import io
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ==========================================
# FUNÇÕES DE CRIPTOGRAFIA
# ==========================================
def criptografar_dados(dados_bytes, chave_publica):
    chave_aes = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    texto_cifrado = AESGCM(chave_aes).encrypt(nonce, dados_bytes, None)
    chave_cifrada = chave_publica.encrypt(
        chave_aes,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
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
# INTERFACE GRÁFICA
# ==========================================
class BlocoSeguro:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloco de Notas Seguro (Criptografado)")
        self.root.geometry("600x500")
        
        self.arquivos_anexados = []
        
        self.texto = tk.Text(self.root, wrap="word", font=("Arial", 12))
        self.texto.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.lista_anexos = tk.Listbox(self.root, height=4, bg="#f0f0f0")
        self.lista_anexos.pack(padx=10, fill="x")
        
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
        if not os.path.exists("chave_publica.pem"):
            messagebox.showerror("Erro", "Arquivo 'chave_publica.pem' não encontrado na pasta!")
            return
            
        with open("chave_publica.pem", "rb") as f:
            chave_publica = serialization.load_pem_public_key(f.read())

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            texto_digitado = self.texto.get("1.0", "end-1c")
            zf.writestr("mensagem.txt", texto_digitado)
            
            for caminho in self.arquivos_anexados:
                zf.write(caminho, arcname=os.path.basename(caminho))
                
        dados_zip = zip_buffer.getvalue()
        dados_criptografados = criptografar_dados(dados_zip, chave_publica)

        arquivo_saida = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Arquivo Criptografado", "*.enc")])
        if arquivo_saida:
            with open(arquivo_saida, "wb") as f:
                f.write(dados_criptografados)
            messagebox.showinfo("Sucesso", "Arquivo criptografado salvo!\nAnexe este arquivo .enc no seu e-mail.")

    def abrir_cripto(self):
        if not os.path.exists("chave_privada.pem"):
            messagebox.showerror("Erro", "Arquivo 'chave_privada.pem' não encontrado na pasta!")
            return

        # TRAVA DE SEGURANÇA: Verifica se as chaves da pasta são um par válido
        if os.path.exists("chave_privada.pem"):
            with open("chave_publica.pem", "rb") as f_pub, open("chave_privada.pem", "rb") as f_priv:
                pub = serialization.load_pem_public_key(f_pub.read())
                priv = serialization.load_pem_private_key(f_priv.read(), password=None)
                if pub.public_numbers() != priv.public_key().public_numbers():
                    messagebox.showerror("Erro Crítico", "As chaves na pasta não formam um par válido! Gere novas chaves.")
                    return
        # FIM DA TRAVA

        with open("chave_publica.pem", "rb") as f:
            chave_publica = serialization.load_pem_public_key(f.read())
            
        with open("chave_privada.pem", "rb") as f:
            chave_privada = serialization.load_pem_private_key(f.read(), password=None)

        # Abre a janela de busca direto na Área de Trabalho
        arquivo_enc = filedialog.askopenfilename(
            title="Selecione o arquivo .enc", 
            initialdir=os.path.expanduser("~/Desktop"),
            filetypes=[("Arquivo Criptografado", "*.enc"), ("Todos os arquivos", "*.*")]
        )
        
        if not arquivo_enc:
            return

        try:
            with open(arquivo_enc, "rb") as f:
                dados_arquivo = f.read()

            dados_zip = descriptografar_dados(dados_arquivo, chave_privada)
            
            # Cria a pasta na Área de Trabalho automaticamente
            pasta_desktop = os.path.expanduser("~/Desktop")
            pasta_saida = os.path.join(pasta_desktop, "Mensagens_Recebidas")
            
            if not os.path.exists(pasta_saida):
                os.makedirs(pasta_saida)
                
            with zipfile.ZipFile(io.BytesIO(dados_zip)) as zf:
                zf.extractall(pasta_saida)
                
                if "mensagem.txt" in zf.namelist():
                    texto_lido = zf.read("mensagem.txt").decode("utf-8")
                    self.texto.delete("1.0", "end")
                    self.texto.insert("1.0", texto_lido)
                
            messagebox.showinfo("Sucesso", f"Mensagem e anexos extraídos com sucesso para:\n{pasta_saida}")
                
        except Exception as e:
            messagebox.showerror("Erro", "Falha ao descriptografar. Chave privada incorreta ou arquivo corrompido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlocoSeguro(root)
    root.mainloop()