

import pygame
from time import sleep
from src.telas.salas.sala import Sala
from src.telas.login.login import LoginScreen
from src.telas.menu.menu import MenuTela

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()


login = LoginScreen(screen, clock)
autenticated = login.run()
if not autenticated:
    pygame.quit()
    raise SystemExit("Autenticação necessária para conectar.")

menu = MenuTela(screen)
escolha_menu = menu.menu_principal()
if escolha_menu == "sair":
    running = False
elif escolha_menu == "jogar":
    running = True


todas_salas = [
    Sala("Variáveis", 0, screen, clock),
    Sala("Estruturas Condicionais", 1, screen, clock),
    Sala("Laços de Repetição", 2, screen, clock),
    Sala("Funções", 3, screen, clock)
]

vidas = 3
sala = todas_salas[0]
questoes = sala.embaralha_questoes()

numero_fase = 0
sala_started = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((252, 255, 217))
    
   
    if numero_fase == 0 and not sala_started:
        sala.tela_sala()
        sala_started = True

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
        sala_started = False

pygame.quit()