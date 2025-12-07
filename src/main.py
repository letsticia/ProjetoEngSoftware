

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
    Sala("Vetores", 3, screen, clock)
]

# Função auxiliar para buscar progresso do BD
def get_progresso_usuario():
    progresso = supabase.client.table("resultados").select("*").eq("id_aluno", usuario['id_usuario']).execute()
    if progresso.data == []:
        supabase.client.table("resultados").insert({"id_aluno": usuario['id_usuario'], "score_1": 0, "score_2": 0, "score_3": 0, "score_4": 0}).execute()
        return [0, 0, 0, 0]
    else:
        dados = progresso.data[0]
        return [dados['score_1'], dados['score_2'], dados['score_3'], dados['score_4']]

# Controle de progresso do jogador
progresso_salas = get_progresso_usuario()
mundo = MundoTela(screen, clock, usuario, progresso_salas)

while running:
    # Mostra a tela do mundo para escolher a sala
    sala_escolhida = mundo.run()
    
    if sala_escolhida == -1:
        # Usuário entrou na porta Menu, volta ao menu
        running = menu.menu_principal()
        if running:
            progresso_salas = get_progresso_usuario()  # Atualiza progresso
            mundo = MundoTela(screen, clock, usuario, progresso_salas)
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
            score_anterior = supabase.client.table("resultados").select(f"score_{sala.numero_sala + 1}").eq("id_aluno", usuario['id_usuario']).execute()
            score_anterior_value = score_anterior.data[0][f"score_{sala.numero_sala + 1}"]
            if questoes_certas > score_anterior_value:
                supabase.client.table("resultados").update({f"score_{sala.numero_sala + 1}": questoes_certas}).eq("id_aluno", usuario['id_usuario']).execute()
            
            # Mostra a tela de Game Over
            gameover = GameOverTela(screen, clock, sala)
            voltar_menu = gameover.tela_gameover()
            
            if voltar_menu:
                # Volta ao menu principal
                running = menu.menu_principal()
                if running:
                    progresso_salas = get_progresso_usuario()  # Atualiza progresso
                    mundo = MundoTela(screen, clock, usuario, progresso_salas)
            else:
                running = False
            jogando_sala = False
        
        if numero_fase >= len(questoes):
            print("Parabéns! Você completou todas as questões da sala.")
            
            score_anterior = supabase.client.table("resultados").select(f"score_{sala.numero_sala + 1}").eq("id_aluno", usuario['id_usuario']).execute()
            score_anterior_value = score_anterior.data[0][f"score_{sala.numero_sala + 1}"]
            if questoes_certas > score_anterior_value:
                supabase.client.table("resultados").update({f"score_{sala.numero_sala + 1}": questoes_certas}).eq("id_aluno", usuario['id_usuario']).execute()
            
            # Atualiza o progresso e recria o mundo com salas desbloqueadas
            progresso_salas = get_progresso_usuario()
            mundo.atualizar_salas_desbloqueadas(progresso_salas)
            
            jogando_sala = False
            
            # Verifica se completou todas as salas
            if all(score > 0 for score in progresso_salas):
                print("Parabéns! Você completou todas as salas do jogo!")
                # Aqui você pode adicionar uma tela de vitória

pygame.quit()