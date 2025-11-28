import pygame
from src.telas.questoes.questao import Questao
from src.componentes.botao import Botao
from src.componentes.coracao import sprite_coracao
import os

class Quiz(Questao):
    def __init__(self, enunciado, opcoes, resposta_correta):
        super().__init__(enunciado, opcoes, resposta_correta)
        self.feedback = None
        self.locked = False

    
    def tela(self, screen, vidas):
        font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 26)

        sprite_coracao(screen, vidas)

        x, y = 50, 50
        max_width = screen.get_width() - x - 50 
        lines = self.wrap_text(self.enunciado, font, max_width)
        line_height = font.get_linesize()

        for i, line in enumerate(lines):
            enunciado_surf = font.render(line, True, (0, 0, 0))
            screen.blit(enunciado_surf, (x, y + i * line_height))

        cores_botao = ["azul", "vermelho", "verde", "laranja"]
        
        buttons_y = y + len(lines) * line_height + 120

        for i, opcao in enumerate(self.opcoes):
            botao_opcao_image = pygame.image.load(f"src/img/botao/botao_{cores_botao[i]}.png").convert_alpha()
            botao_opcao = Botao(50 + i * 200, buttons_y, botao_opcao_image, opcao, escala=0.5)
            clicked = botao_opcao.draw(screen)
            if clicked and not self.locked:
                if opcao == self.resposta_correta:
                    self.feedback = "correto"
                    print("Resposta correta")
                else:
                    self.feedback = "errado"
                    print("Resposta incorreta")
                self.locked = True

        if self.feedback is not None:
            fb_font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 24)
            fb_color = (34, 139, 34) if self.feedback == "correto" else (178, 34, 34)
            fb_surf = fb_font.render(self.feedback.upper(), True, fb_color)
            fb_x = 50
            fb_y = buttons_y + 80
            screen.blit(fb_surf, (fb_x, fb_y))
            
            if self.feedback == "correto":
                return True
            else:
                return False
            
    def verificar_resposta(self, resposta):
        return super().verificar_resposta(resposta)
