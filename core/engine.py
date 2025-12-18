#arquivo engine.py

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

    def processar_em_background(self, pasta_origem, pasta_destino, nome_arquivo):
        """
        Inicia a geração em uma Thread separada.
        Isso impede que a interface do usuário 'congele' durante o processamento.
        """
        job = threading.Thread(
            target=self._gerar_pdf,
            args=(pasta_origem, pasta_destino, nome_arquivo),
            daemon=True
        )
        job.start()

    def _gerar_pdf(self, origem, destino, nome):
        """Método privado que executa a lógica pesada de I/O e conversão."""
        try:
            # Validação de Segurança
            if not os.path.exists(origem):
                raise FileNotFoundError(f"Diretório não encontrado: {origem}")

            caminho_final = os.path.join(destino, f"{nome}.pdf")
            
            # Inicializa o Canvas do ReportLab (A folha em branco)
            pdf = canvas.Canvas(caminho_final, pagesize=A4)
            largura_a4, altura_a4 = A4

            # Listagem e Filtragem (Apenas imagens válidas)
            arquivos = [f for f in os.listdir(origem) if f.lower().endswith(self.formatos_aceitos)]
            arquivos.sort() # Garante ordem alfabética no PDF

            if not arquivos:
                raise Exception("A pasta selecionada não contém imagens suportadas.")

            for arquivo in arquivos:
                caminho_img = os.path.join(origem, arquivo)
                
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

            if self.callback_sucesso:
                self.callback_sucesso(caminho_final)

        except Exception as e:
            if self.callback_erro:
                self.callback_erro(str(e))