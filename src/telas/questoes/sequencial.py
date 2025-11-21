import pygame
from src.componentes.botao import Botao
from src.telas.questoes.questao import Questao
import os

class Sequencial(Questao):
    def __init__(self, enunciado, opcoes, resposta_correta):
        super().__init__(enunciado, opcoes, resposta_correta)
       
        self.selected = []
        self.feedback = None  # 
        self.locked = False  
    
    def tela_sequencial(self, screen):
        font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 26)

        x, y = 50, 50
        max_width = screen.get_width() - x - 50 
        lines = self.wrap_text(self.enunciado, font, max_width)
        line_height = font.get_linesize()

        for i, line in enumerate(lines):
            enunciado_surf = font.render(line, True, (0, 0, 0))
            screen.blit(enunciado_surf, (x, y + i * line_height))

        cores_botao = ["azul", "vermelho", "verde", "laranja"]
        
        buttons_y = y + len(lines) * line_height + 220

        for i, opcao in enumerate(self.opcoes):
            botao_opcao_image = pygame.image.load(f"src/img/botao/botao_{cores_botao[i]}.png").convert_alpha()
            botao_opcao = Botao(50 + i * 200, buttons_y, botao_opcao_image, opcao, escala=0.5)
            clicked = botao_opcao.draw(screen)
            if clicked and not self.locked:
               
                if opcao not in self.selected:
                    self.selected.append(opcao)
              
                if len(self.selected) == len(self.opcoes):
                    
                    try:
                        expected = list(self.resposta_correta)
                    except Exception:
                        expected = [self.resposta_correta]
                    if self.selected == expected:
                        self.feedback = "correto"
                        print("Resposta correta")
                    else:
                        self.feedback = "errado"
                        print("Resposta incorreta")
                    self.locked = True

       
        resposta_x = 50
        resposta_y = buttons_y - 120
        label_font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 22)
      
        label_surf = label_font.render("Resposta:   ", True, (255, 165, 0))

        screen.blit(label_surf, (resposta_x, resposta_y))

   
        selected_text = " ".join(self.selected)
        selected_font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 22)
        selected_surf = selected_font.render(selected_text, True, (10, 10, 10))
        screen.blit(selected_surf, (resposta_x + 120, resposta_y))

      
        if self.feedback is not None:
            fb_color = (34, 139, 34) if self.feedback == "correto" else (178, 34, 34)
            fb_surf = label_font.render(self.feedback.upper(), True, fb_color)
            screen.blit(fb_surf, (resposta_x, resposta_y + 40))
        
            if self.feedback == "correto":
                return True
            else:
                return False
        
    def verificar_resposta(self, resposta):
        return super().verificar_resposta(resposta)


pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
questao = Sequencial(
    "Coloque as palavras na ordem correta para formar uma frase em Python:",
    ["mundo", "Olá", "!"],
    ["Olá", "mundo", "!"]
)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((252, 255, 217))
    
    questao.tela_sequencial(screen)
   
    pygame.display.flip()
    clock.tick(60)
pygame.quit()