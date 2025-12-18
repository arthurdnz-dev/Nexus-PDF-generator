import os
import threading
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class PDFGeneratorEngine:
    """
    Classe de nível sênior para processamento de arquivos.
    Gerencia a conversão de imagens e a escrita do buffer do PDF.
    """
    
    def __init__(self, callback_sucesso=None, callback_erro=None):
        # Callbacks permitem que o motor avise à interface quando terminou,
        # sem que o motor precise 'conhecer' a interface (Desacoplamento).
        self.callback_sucesso = callback_sucesso
        self.callback_erro = callback_erro
        self.formatos_aceitos = ('.jpg', '.jpeg', '.png', '.bmp')

    def processar_lista_arquivos(self, lista_arquivos, pasta_destino, nome_arquivo):
        """
        Inicia a geração do PDF a partir de uma lista específica de arquivos.
        Executado em uma Thread separada para não congelar a UI.
        """
        job = threading.Thread(
            target=self._gerar_pdf_da_lista,
            args=(lista_arquivos, pasta_destino, nome_arquivo),
            daemon=True
        )
        job.start()

    def _gerar_pdf_da_lista(self, caminhos_imagens, destino, nome):
        """Método privado que executa a lógica pesada de I/O e conversão."""
        try:
            # Garante que a pasta de destino exista
            if not os.path.exists(destino):
                os.makedirs(destino, exist_ok=True)

            caminho_final = os.path.join(destino, f"{nome}.pdf")
            
            # Inicializa o Canvas do ReportLab (A folha em branco)
            pdf = canvas.Canvas(caminho_final, pagesize=A4)
            largura_a4, altura_a4 = A4

            if not caminhos_imagens:
                raise Exception("Nenhuma imagem selecionada para o processamento.")

            for caminho_img in caminhos_imagens:
                if not os.path.exists(caminho_img):
                    continue
                
                # Processamento de Imagem com Pillow (PIL)
                with Image.open(caminho_img) as img:
                    # Converte para RGB (Removendo transparências que quebram o PDF)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Cálculo de Aspect Ratio (Redimensionamento Proporcional)
                    # Deixamos uma margem de 40 pixels nas bordas
                    largura_max = largura_a4 - 80
                    altura_max = altura_a4 - 80
                    
                    img.thumbnail((largura_max, altura_max), Image.Resampling.LANCZOS)
                    largura_img, altura_img = img.size
                    
                    # Centralização Matemática na Página A4
                    x_centrado = (largura_a4 - largura_img) / 2
                    y_centrado = (altura_a4 - altura_img) / 2
                    
                    # Desenha a imagem no PDF e finaliza a página atual
                    pdf.drawImage(caminho_img, x_centrado, y_centrado, width=largura_img, height=altura_img)
                    pdf.showPage() 

            pdf.save() # Escreve o arquivo no disco

            # Comunicação de sucesso via callback
            if self.callback_sucesso:
                self.callback_sucesso(caminho_final)

        except Exception as e:
            # Comunicação de erro via callback
            if self.callback_erro:
                self.callback_erro(str(e))