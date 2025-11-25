

import pygame
from time import sleep
from src.telas.salas.sala import Sala

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()


todas_salas = [
    Sala("Variáveis", 0),
    Sala("Estruturas Condicionais", 1),
    Sala("Laços de Repetição", 2),
    Sala("Funções", 3)
]

vidas = 3
sala = todas_salas[0]
questoes = sala.embaralha_questoes()

running = True
numero_fase = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((252, 255, 217))
    
    resposta = questoes[numero_fase].tela(screen, vidas)
   
    pygame.display.flip()
    clock.tick(60)

    if resposta == True:
        print("Usuário acertou a questão!")
        numero_fase += 1
        sleep(0.3)
    elif resposta == False:
        print("Usuário errou a questão!")
        numero_fase += 1
        vidas -= 1
        sleep(0.3)

    if vidas == 0:
        print("Game Over!")
        running = False
    
    if numero_fase >= len(questoes):
        print("Parabéns! Você completou todas as questões da sala.")


        sala = todas_salas[sala.numero_sala + 1]
        questoes = sala.embaralha_questoes()
        numero_fase = 0


pygame.quit()