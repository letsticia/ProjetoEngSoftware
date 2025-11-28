import pygame

def sprite_coracao(screen, vidas):

    img_coracao = pygame.image.load("src/img/coracao.png").convert_alpha()
    img_coracao = pygame.transform.scale(img_coracao, (30, 30))

    for i in range(vidas):
        screen.blit(img_coracao, (800 + i * 40, 10))