#main.py

import sys
import os
from ui.main_window import AppInterface
from core.engine import PDFGeneratorEngine

class NexusController:
    """
    Classe Controller de nível Sênior.
    Faz a ponte entre a lógica de negócio (Core) e a visualização (UI).
    """
    def __init__(self):
        # 1. Inicializa o motor com as funções de retorno (callbacks)
        # Passamos as funções que serão chamadas quando o PDF estiver pronto
        self.engine = PDFGeneratorEngine(
            callback_sucesso=self._comunicar_sucesso,
            callback_erro=self._comunicar_erro
        )

        # 2. Inicializa a interface gráfica passando a instância do motor
        self.app = AppInterface(engine=self.engine)

    def _comunicar_sucesso(self, caminho_final):
        """
        Trata o retorno positivo do motor.
        O uso do 'after' é obrigatório para que a UI (Thread Principal) 
        receba a informação da Thread de processamento com segurança.
        """
        self.app.after(0, lambda: self.app.notificar_sucesso(caminho_final))

    def _comunicar_erro(self, mensagem):
        """Trata o retorno de erro de forma segura para a interface."""
        self.app.after(0, lambda: self.app.notificar_erro(mensagem))

    def iniciar(self):
        """Lança a aplicação e centraliza na tela do usuário."""
        # Garante que o ícone e caminhos relativos funcionem independente de onde o terminal abra
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        os.chdir(diretorio_atual)

        print("Nexus PDF Engine: Inicializando interface...")
        
        # Centralização Dinâmica
        self.app.update_idletasks()
        largura = self.app.winfo_width()
        altura = self.app.winfo_height()
        x = (self.app.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.app.winfo_screenheight() // 2) - (altura // 2)
        self.app.geometry(f"+{x}+{y}")

        # Loop principal (Mantém a janela aberta)
        self.app.mainloop()

if __name__ == "__main__":
    # Ponto de entrada oficial do sistema
    service = NexusController()
    service.iniciar()