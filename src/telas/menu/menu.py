import pygame
from src.componentes.botao import Botao

class MenuTela:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_path = "src/fonts/Grand9K Pixel.ttf"
        
        try:
            self.font = pygame.font.Font(self.font_path, 30)
        except Exception:
            self.font = pygame.font.SysFont(None, 30)
        
    
    def menu_principal(self) -> str:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "sair"

            self.screen.fill((252, 255, 217))
            self.logo_img = pygame.image.load("src/img/logo.png")
            self.logo_img = pygame.transform.scale(self.logo_img, (self.logo_img.get_width() // 2, self.logo_img.get_height() // 2))
            
            logo_rect = self.logo_img.get_rect(center=(500, 80))
            self.screen.blit(self.logo_img, logo_rect)
            
  
            botao_vermelho = pygame.image.load("src/img/botao/botao_vermelho.png").convert_alpha()
            botao_verde = pygame.image.load("src/img/botao/botao_verde.png").convert_alpha()
            botao_azul = pygame.image.load("src/img/botao/botao_azul.png").convert_alpha()

            botao_jogar = Botao( x=410, y=200, imagem=botao_vermelho, text="Jogar", escala=0.5)
            botao_configuracoes = Botao( x=410, y=300, imagem=botao_verde, text="Configurações", escala=0.5)
            botao_sair = Botao( x=410, y=400, imagem=botao_azul, text="Sair", escala=0.5)

            if botao_jogar.draw(self.screen):
                return "jogar"
            if botao_configuracoes.draw(self.screen):
                return "configuracoes"
            if botao_sair.draw(self.screen):
                return "sair"
 
            pygame.display.flip()
            self.clock.tick(60)
    