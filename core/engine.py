import os
import threading
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class PDFGeneratorEngine:
    """
    Classe de nível sênior para processamento de arquivos.
    Gerencia a conversão de imagens em grade (4 por página).
    """
    
    def __init__(self, callback_sucesso=None, callback_erro=None):
        self.callback_sucesso = callback_sucesso
        self.callback_erro = callback_erro
        self.formatos_aceitos = ('.jpg', '.jpeg', '.png', '.bmp')

    def processar_lista_arquivos(self, lista_arquivos, pasta_destino, nome_arquivo):
        """Inicia a geração em Thread para não travar a UI."""
        job = threading.Thread(
            target=self._gerar_pdf_em_grade,
            args=(lista_arquivos, pasta_destino, nome_arquivo),
            daemon=True
        )
        job.start()

    def _gerar_pdf_em_grade(self, caminhos_imagens, destino, nome):
        """Lógica de posicionamento 2x2 para reduzir o peso do PDF."""
        try:
            if not os.path.exists(destino):
                os.makedirs(destino, exist_ok=True)

            caminho_final = os.path.join(destino, f"{nome}.pdf")
            pdf = canvas.Canvas(caminho_final, pagesize=A4)
            largura_a4, altura_a4 = A4

            # Definições da Grade
            margem = 40
            espacamento = 20
            largura_box = (largura_a4 - (2 * margem) - espacamento) / 2
            altura_box = (altura_a4 - (2 * margem) - espacamento) / 2

            for i, caminho_img in enumerate(caminhos_imagens):
                if not os.path.exists(caminho_img):
                    continue
                
                # Cálculo de posição (0=top-left, 1=top-right, 2=bottom-left, 3=bottom-right)
                pos = i % 4
                coluna = pos % 2
                linha = 1 - (pos // 2) # 1 é topo, 0 é base no ReportLab

                x_base = margem + (coluna * (largura_box + espacamento))
                y_base = margem + (linha * (altura_box + espacamento))

                with Image.open(caminho_img) as img:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    img.thumbnail((largura_box, altura_box), Image.Resampling.LANCZOS)
                    w_img, h_img = img.size
                    
                    # Centralização no box
                    x_final = x_base + (largura_box - w_img) / 2
                    y_final = y_base + (altura_box - h_img) / 2
                    
                    pdf.drawImage(caminho_img, x_final, y_final, width=w_img, height=h_img)

                # Fecha a página a cada 4 fotos ou no final da lista
                if (i + 1) % 4 == 0 or (i + 1) == len(caminhos_imagens):
                    pdf.showPage() 

            pdf.save()

            if self.callback_sucesso:
                self.callback_sucesso(caminho_final)

        except Exception as e:
            if self.callback_erro:
                self.callback_erro(str(e))