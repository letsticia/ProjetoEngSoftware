import pygame
from src.componentes.botao import Botao
from src.telas.questoes.questao import Questao
from src.db.supabase_class import SupabaseClient
import os

class Sequencial(Questao):
    def __init__(self, enunciado, opcoes, resposta_correta):
        super().__init__(enunciado, opcoes, resposta_correta)
       
        self.selected = []
        self.feedback = None 
        self.locked = False
    
    def tela(self, screen, vidas):
        font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 26)
        img_coracao = pygame.image.load("src/img/coracao.png").convert_alpha()
        img_coracao = pygame.transform.scale(img_coracao, (30, 30))
        for i in range(vidas):
            screen.blit(img_coracao, (800 + i * 40, 10))

        x, y = 50, 50
        max_width = screen.get_width() - x - 50 
        lines = self.wrap_text(self.enunciado, font, max_width)
        line_height = font.get_linesize()

        for i, line in enumerate(lines):
            enunciado_surf = font.render(line, True, (0, 0, 0))
            screen.blit(enunciado_surf, (x, y + i * line_height))

        cores_botao = ["azul", "vermelho", "verde", "laranja"]
        
        buttons_y = y + len(lines) * line_height + 320

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
        resposta_y = buttons_y - 220
        label_font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 22)
      
        label_surf = label_font.render("Resposta:   ", True, (255, 165, 0))

        screen.blit(label_surf, (resposta_x, resposta_y))

   
        selected_font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 22)
        
        for idx, item in enumerate(self.selected):
            sel_surf = selected_font.render(item, True, (10, 10, 10))
            line_y = resposta_y + idx * (selected_font.get_linesize() + 4)
            screen.blit(sel_surf, (resposta_x + 120, line_y))

      
        if self.feedback is not None:
            fb_color = (34, 139, 34) if self.feedback == "correto" else (178, 34, 34)
            fb_surf = label_font.render(self.feedback.upper(), True, fb_color)
            screen.blit(fb_surf, (resposta_x + 500, resposta_y))
        
            if self.feedback == "correto":
                return True
            else:
                return False
        
    def verificar_resposta(self, resposta):
        return super().verificar_resposta(resposta)

