
import pygame
import random
from src.utils.utils import questao_sequencial, questao_quiz
from src.componentes.coracao import sprite_coracao
import time
class Sala:

    def __init__(self, nome_sala, numero_sala, screen, clock):
        self.nome_sala = nome_sala
        self.numero_sala = numero_sala
        self.screen = screen
        self.clock = clock
        
    
    def embaralha_questoes(self):
        indices_sequenciais = [self.numero_sala * 3 + i for i in range(3)]
        indices_quiz = [self.numero_sala * 2 + i for i in range(2)]
        
        questoes_sala = []
        for idx in indices_sequenciais:
            questoes_sala.append(questao_sequencial(idx))
        for idx in indices_quiz:
            questoes_sala.append(questao_quiz(idx))
        
        random.shuffle(questoes_sala)

        return questoes_sala
    
      
    def tela_sala(self, duration=2.0):
        try:
            image_path = f"src/img/fases/{self.numero_sala}.png"
            transition_img = pygame.image.load(image_path).convert_alpha()
            transition_img_pos = ((self.screen.get_width() - transition_img.get_width()) // 2,
                                  100)
            overlay = pygame.Surface(self.screen.get_size())
            overlay.fill((252, 255, 217))

            for alpha in range(0, 255, 8):
                overlay.set_alpha(alpha)
                self.screen.blit(transition_img, transition_img_pos)
                self.screen.blit(overlay, (0, 0))
                pygame.display.update()
                self.clock.tick(60)

            for alpha in range(255, -1, -8):
                overlay.set_alpha(alpha)
                self.screen.blit(transition_img, transition_img_pos)
            
                pygame.display.update()
                self.clock.tick(60)

            start_time = time.time()
            while time.time() - start_time < duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                self.screen.blit(transition_img, transition_img_pos)
                pygame.display.update()
                self.clock.tick(60)
        except Exception as e:
            print("Erro ao carregar a imagem de transição:", e)
            pass

        
    