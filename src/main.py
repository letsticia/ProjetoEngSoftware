

import pygame
from time import sleep
from src.telas.salas.sala import Sala
from src.telas.login.login import LoginScreen
from src.telas.menu.menu import MenuTela
from src.telas.progresso.progresso import ProgressoTela
from src.telas.gameover.gameover import GameOverTela
from src.telas.mundo.mundo import MundoTela
from src.db.supabase_class import SupabaseClient

supabase = SupabaseClient()
pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()


login = LoginScreen(screen, clock)
autenticated, usuario = login.run()
if not autenticated:
    pygame.quit()
    raise SystemExit("Autenticação necessária para conectar.")


menu = MenuTela(screen, usuario)

running = menu.menu_principal()

todas_salas = [
    Sala("Variáveis", 0, screen, clock),
    Sala("Estruturas Condicionais", 1, screen, clock),
    Sala("Laços de Repetição", 2, screen, clock),
    Sala("Funções", 3, screen, clock)
]

# Controle de progresso do jogador
sala_atual_index = 0  # Última sala desbloqueada
mundo = MundoTela(screen, clock, usuario, sala_atual_index)

while running:
    # Mostra a tela do mundo para escolher a sala
    sala_escolhida = mundo.run()
    
    if sala_escolhida == -1:
        # Usuário apertou ESC, volta ao menu
        running = menu.menu_principal()
        if running:
            mundo = MundoTela(screen, clock, usuario, sala_atual_index)
        continue
    
    if sala_escolhida is None:
        running = False
        continue
    
    # Configura a sala escolhida
    sala = todas_salas[sala_escolhida]
    questoes = sala.embaralha_questoes()
    vidas = 3
    numero_fase = 0
    questoes_certas = 0
    
    # Mostra a tela de transição da sala
    sala.tela_sala()
    
    # Loop das questões da sala
    jogando_sala = True
    while jogando_sala:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando_sala = False
                running = False

        screen.fill((252, 255, 217))
        
        resposta = questoes[numero_fase].tela(screen, vidas)
        
        pygame.display.flip() 
        clock.tick(60)
        
        if resposta == True:
            print("Usuário acertou a questão!")
            numero_fase += 1
            questoes_certas += 1
            sleep(0.3)
        elif resposta == False:
            print("Usuário errou a questão!")
            numero_fase += 1
            vidas -= 1
            sleep(0.3)

        if vidas == 0:
            print("Game Over!")
            supabase.client.table("resultados").update({f"score_{sala.numero_sala + 1}": questoes_certas}).eq("id_aluno", usuario['id_usuario']).execute()
            
            # Mostra a tela de Game Over
            gameover = GameOverTela(screen, clock, sala)
            voltar_menu = gameover.tela_gameover()
            
            if voltar_menu:
                # Volta ao menu principal
                running = menu.menu_principal()
                if running:
                    mundo = MundoTela(screen, clock, usuario, sala_atual_index)
            else:
                running = False
            jogando_sala = False
        
        if numero_fase >= len(questoes):
            print("Parabéns! Você completou todas as questões da sala.")
            
            supabase.client.table("resultados").update({f"score_{sala.numero_sala + 1}": questoes_certas}).eq("id_aluno", usuario['id_usuario']).execute()
            
            # Desbloqueia a próxima sala
            if sala.numero_sala >= sala_atual_index:
                sala_atual_index = sala.numero_sala + 1
                mundo.atualizar_salas_desbloqueadas(sala.numero_sala)
            
            jogando_sala = False
            
            # Verifica se completou todas as salas
            if sala_atual_index >= len(todas_salas):
                print("Parabéns! Você completou todas as salas do jogo!")
                # Aqui você pode adicionar uma tela de vitória

pygame.quit()