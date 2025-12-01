import pygame
from src.componentes.botao import Botao
from src.telas.progresso.progresso import ProgressoTela

class MenuTela:
    def __init__(self, screen, usuario):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_path = "src/fonts/Grand9K Pixel.ttf"
        self.usuario = usuario
        
        try:
            self.font = pygame.font.Font(self.font_path, 30)
        except Exception:
            self.font = pygame.font.SysFont(None, 30)
        
    
    def menu_principal(self) -> str:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit("Usuário saiu do jogo.")

            self.screen.fill((252, 255, 217))
            self.logo_img = pygame.image.load("src/img/logo.png")
            self.logo_img = pygame.transform.scale(self.logo_img, (self.logo_img.get_width() // 2, self.logo_img.get_height() // 2))
            
            logo_rect = self.logo_img.get_rect(center=(500, 80))
            self.screen.blit(self.logo_img, logo_rect)
            
  
            botao_laranja = pygame.image.load("src/img/botao/botao_laranja.png").convert_alpha()
            botao_verde = pygame.image.load("src/img/botao/botao_verde.png").convert_alpha()
            botao_vermelho = pygame.image.load("src/img/botao/botao_vermelho.png").convert_alpha()

            botao_jogar = Botao( x=410, y=200, imagem=botao_laranja, text="Jogar", escala=0.5)
            botao_progresso = Botao( x=410, y=300, imagem=botao_verde, text="Progresso", escala=0.5)
            botao_sair = Botao( x=410, y=400, imagem=botao_vermelho, text="Sair", escala=0.5)
            if botao_jogar.draw(self.screen):
                return True
            if botao_progresso.draw(self.screen):
                progresso_tela = ProgressoTela(self.screen, self.usuario['id_usuario'])
                progresso_surf = progresso_tela.mostrar_progresso()
            if botao_sair.draw(self.screen):
                pygame.quit()
                raise SystemExit("Usuário saiu do jogo.")
 
            pygame.display.flip()
            self.clock.tick(60)
    