import pygame
import time
from src.componentes.botao import Botao


class GameOverTela:
    def __init__(self, screen, clock, sala):
        self.screen = screen
        self.clock = clock
        self.sala = sala
        self.font_path = "src/fonts/Grand9K Pixel.ttf"
        
        # Mensagens de estudo baseadas na sala
        self.mensagens_estudo = {
            0: "Revise o conceito de Variáveis:\nTipos de dados, declaração e atribuição.",
            1: "Revise Estruturas Condicionais:\nif, else, elif e operadores lógicos.",
            2: "Revise Laços de Repetição:\nfor, while e controle de fluxo.",
            3: "Revise o conceito de Vetores:\nArrays, listas e manipulação de dados."
        }
        
        try:
            self.font_grande = pygame.font.Font(self.font_path, 40)
            self.font_media = pygame.font.Font(self.font_path, 24)
            self.font_pequena = pygame.font.Font(self.font_path, 18)
        except Exception:
            self.font_grande = pygame.font.SysFont(None, 40)
            self.font_media = pygame.font.SysFont(None, 24)
            self.font_pequena = pygame.font.SysFont(None, 18)

    def get_mensagem_estudo(self):
        """Retorna a mensagem de estudo baseada na sala atual"""
        numero = self.sala.numero_sala
        return self.mensagens_estudo.get(numero, "Continue estudando programação!")

    def tela_gameover(self, duration=3.0):
        """Exibe a tela de Game Over com imagem e mensagem de estudo"""
        try:
            # Carrega a imagem de game over (você pode trocar o caminho depois)
            gameover_img = pygame.image.load("src/img/gameover.png").convert_alpha()
            # Redimensiona a imagem (ajuste os valores conforme necessário)
            largura_desejada = 600  # largura em pixels
            proporcao = largura_desejada / gameover_img.get_width()
            altura_desejada = int(gameover_img.get_height() * proporcao)
            gameover_img = pygame.transform.scale(gameover_img, (largura_desejada, altura_desejada))
            gameover_pos = ((self.screen.get_width() - gameover_img.get_width()) // 2, 30)
        except Exception as e:
            print("Erro ao carregar imagem de game over:", e)
            gameover_img = None
            gameover_pos = (0, 0)

        # Efeito de fade in
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((252, 255, 217))

        for alpha in range(0, 255, 8):
            overlay.set_alpha(alpha)
            self.screen.fill((252, 255, 217))
            if gameover_img:
                self.screen.blit(gameover_img, gameover_pos)
            self.screen.blit(overlay, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

        # Fade out
        for alpha in range(255, -1, -8):
            overlay.set_alpha(alpha)
            self.screen.fill((252, 255, 217))
            if gameover_img:
                self.screen.blit(gameover_img, gameover_pos)
            self.screen.blit(overlay, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

        # Exibe a tela com a mensagem de estudo
        botao_vermelho = pygame.image.load("src/img/botao/botao_vermelho.png").convert_alpha()
        botao_voltar = Botao(x=410, y=550, imagem=botao_vermelho, text="Voltar ao Menu", escala=0.5)

        mensagem = self.get_mensagem_estudo()
        sala_nome = self.sala.nome_sala

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit("Usuário saiu do jogo.")

            self.screen.fill((252, 255, 217))

            # Desenha a imagem de game over
            if gameover_img:
                self.screen.blit(gameover_img, gameover_pos)

            # Texto da sala onde parou
            texto_sala = self.font_media.render(f"Você parou na sala: {sala_nome}", True, (80, 80, 80))
            texto_sala_rect = texto_sala.get_rect(center=(self.screen.get_width() // 2, 350))
            self.screen.blit(texto_sala, texto_sala_rect)

            # Mensagem de estudo (pode ter múltiplas linhas)
            y_offset = 400
            for linha in mensagem.split('\n'):
                texto_linha = self.font_pequena.render(linha, True, (60, 60, 60))
                texto_linha_rect = texto_linha.get_rect(center=(self.screen.get_width() // 2, y_offset))
                self.screen.blit(texto_linha, texto_linha_rect)
                y_offset += 30

            # Botão de voltar ao menu
            if botao_voltar.draw(self.screen):
                return True  # Sinaliza para voltar ao menu

            pygame.display.flip()
            self.clock.tick(60)

        return False
