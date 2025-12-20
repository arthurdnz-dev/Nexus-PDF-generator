import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class AppInterface(ctk.CTk):
    def __init__(self, engine):
        super().__init__()
        
        self.engine = engine
        self.lista_caminhos_arquivos = []
        
        self.title("Nexus PDF Generator PRO")
        self.geometry("1100x700")

        # Configuração do Ícone (Caminho absoluto conforme solicitado)
        caminho_icone = r"C:\Users\alkeb\Downloads\Nexus logo.ico"
        if os.path.exists(caminho_icone):
            try:
                self.iconbitmap(caminho_icone)
            except:
                pass
        
        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._configurar_sidebar()
        self._configurar_painel_visualizacao()

    def _configurar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="NEXUS ENGINE", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, padx=20, pady=(30, 40))

        # Botão: Selecionar
        self.btn_origem = ctk.CTkButton(self.sidebar, text="🖼️ Selecionar Imagens", command=self._acao_selecionar_arquivos, height=45)
        self.btn_origem.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Botão: Limpar (Destaque em Laranja Escuro)
        self.btn_limpar = ctk.CTkButton(self.sidebar, text="🗑️ Limpar Lista", command=self._acao_limpar_lista, height=35, fg_color="#A34900", hover_color="#803900")
        self.btn_limpar.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Botão: Destino
        self.btn_destino = ctk.CTkButton(self.sidebar, text="🎯 Pasta de Destino PDF", command=self._acao_selecionar_destino, height=45, fg_color="#3b3b3b")
        self.btn_destino.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.entry_nome = ctk.CTkEntry(self.sidebar, placeholder_text="Nome do PDF final...", height=35)
        self.entry_nome.grid(row=4, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Botão: Gerar
        self.btn_gerar = ctk.CTkButton(self.sidebar, text="GERAR PDF", command=self._acao_gerar_pdf, height=55, fg_color="#2eb85c", hover_color="#1e7d3e", font=ctk.CTkFont(weight="bold"))
        self.btn_gerar.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    def _configurar_painel_visualizacao(self):
        self.container_preview = ctk.CTkFrame(self, fg_color="transparent")
        self.container_preview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.lista_fotos = ctk.CTkScrollableFrame(self.container_preview, label_text="Fotos Selecionadas para o PDF")
        self.lista_fotos.pack(fill="both", expand=True)

    def _acao_limpar_lista(self):
        """Limpa toda a fila de arquivos selecionados."""
        if not self.lista_caminhos_arquivos:
            return
        if messagebox.askyesno("Limpar", "Deseja remover todas as fotos da lista?"):
            self.lista_caminhos_arquivos.clear()
            self._renderizar_miniaturas()

    def _acao_selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(title="Selecione as fotos", filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")])
        if arquivos:
            self.lista_caminhos_arquivos.extend(list(arquivos))
            self._renderizar_miniaturas()

    def _acao_selecionar_destino(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.path_destino = caminho

    def _renderizar_miniaturas(self):
        for widget in self.lista_fotos.winfo_children():
            widget.destroy()
        for caminho_full in self.lista_caminhos_arquivos:
            nome_arquivo = os.path.basename(caminho_full)
            try:
                img_pil = Image.open(caminho_full)
                img_pil.thumbnail((80, 80))
                img_ctk = ctk.CTkImage(img_pil, size=(60, 60))
                card = ctk.CTkFrame(self.lista_fotos, fg_color="#252525", border_color="#333333", border_width=1)
                card.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(card, image=img_ctk, text="").pack(side="left", padx=15, pady=5)
                ctk.CTkLabel(card, text=nome_arquivo, font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
                btn_remover = ctk.CTkButton(card, text="X", width=30, fg_color="#e55353", hover_color="#b03a3a",
                                           command=lambda p=caminho_full: self._remover_item(p))
                btn_remover.pack(side="right", padx=15)
            except: continue

    def _remover_item(self, caminho):
        self.lista_caminhos_arquivos.remove(caminho)
        self._renderizar_miniaturas()

    def _acao_gerar_pdf(self):
        nome = self.entry_nome.get()
        if not self.lista_caminhos_arquivos or not hasattr(self, 'path_destino') or not nome:
            messagebox.showwarning("Campos vazios", "Selecione as imagens, o destino e o nome do arquivo!")
            return
        self.btn_gerar.configure(state="disabled", text="GERANDO...")
        self.engine.processar_lista_arquivos(self.lista_caminhos_arquivos, self.path_destino, nome)

    def notificar_sucesso(self, caminho):
        self.btn_gerar.configure(state="normal", text="GERAR PDF")
        messagebox.showinfo("Sucesso", f"PDF criado com sucesso!\n{caminho}")

    def notificar_erro(self, msg):
        self.btn_gerar.configure(state="normal", text="GERAR PDF")
        messagebox.showerror("Erro", msg)