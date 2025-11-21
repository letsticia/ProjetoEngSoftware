import pygame 

class Botao:
    def __init__(self, x, y, imagem, text, escala=1):
        self.text = text
        self.escala = escala
        self.largura = int(imagem.get_width() * escala)
        self.altura = int(imagem.get_height() * escala)
        self.imagem = pygame.transform.scale(imagem, (self.largura, self.altura))
        self.rect = self.imagem.get_rect()
        self.rect.topleft = (x, y)
        self.cliked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.cliked == False:
                self.cliked = True
                action = True
            if not pygame.mouse.get_pressed()[0]:
                self.cliked = False

        font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", int(16 * (self.escala+0.3)))
        font.set_bold(True)
        text_surf = font.render(self.text, True, (255,255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        screen.blit(self.imagem, self.rect)
        screen.blit(text_surf, text_rect)
        return action
    
