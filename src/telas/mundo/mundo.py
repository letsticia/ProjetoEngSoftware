import pygame
import math
import random

LARGURA_TELA = 800
ALTURA_TELA = 600
COR_FUNDO_BITSTART = (252, 255, 217) # Bege Claro


class Robo:
    """Classe que representa o robô controlável pelo jogador com animação de caminhada"""
    
    def __init__(self, x, y, screen):
        self.screen = screen
        self.x = x
        self.y = y
        self.velocidade = 3
        self.largura = 40
        self.altura = 50
        
        # Sistema de animação
        self.frame_atual = 0
        self.tempo_frame = 0
        self.velocidade_animacao = 10
        self.andando = False
        self.direcao = 1  # 1 = direita, -1 = esquerda
        
        # Tentativa de carregar imagem
        try:
            # OBS: Esta linha precisa do arquivo src/img/robo.png
            self.imagem = pygame.image.load("src/img/robo.png").convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem, (self.largura, self.altura))
            self.usar_imagem = True
        except:
            self.usar_imagem = False
        
    def desenhar_robo_pixelart(self):
        """Desenha um robô estilo pixel art com animação - estilo BitStart"""
        
        bob_offset = 0
        if self.andando:
            bob_offset = abs(math.sin(self.frame_atual * 0.5)) * 2
        
        base_y = self.y + bob_offset
        
        
        COR_CORPO_PRINCIPAL = (100, 180, 255)  # Azul
        COR_CORPO_ESCURA = (60, 120, 200)
        COR_OLHOS = (0, 255, 200)
        COR_ANTENA = (255, 140, 80)
        COR_BORDA = (40, 40, 60)
        
       
        shadow_surface = pygame.Surface((self.largura, 6))
        shadow_surface.set_alpha(60)
        shadow_surface.fill((0, 0, 0))
        self.screen.blit(shadow_surface, (self.x, base_y + self.altura))
        
        
        corpo_rect = pygame.Rect(self.x + 5, base_y + 20, self.largura - 10, self.altura - 25)
        pygame.draw.rect(self.screen, COR_BORDA, corpo_rect.inflate(4, 4))
        pygame.draw.rect(self.screen, COR_CORPO_PRINCIPAL, corpo_rect)
        
        
        pygame.draw.rect(self.screen, COR_CORPO_ESCURA, 
                         pygame.Rect(self.x + 12, base_y + 28, 16, 14))
        
        
        cabeca_rect = pygame.Rect(self.x + 8, base_y + 8, 24, 16)
        pygame.draw.rect(self.screen, COR_BORDA, cabeca_rect.inflate(3, 3))
        pygame.draw.rect(self.screen, COR_CORPO_PRINCIPAL, cabeca_rect)
        
        
        piscar = (pygame.time.get_ticks() // 2500) % 15 == 0
        
        if not piscar:
            pygame.draw.rect(self.screen, COR_OLHOS, (self.x + 13, base_y + 14, 5, 5))
            pygame.draw.rect(self.screen, COR_OLHOS, (self.x + 22, base_y + 14, 5, 5))
            # Brilho
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x + 14, base_y + 15, 2, 2))
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x + 23, base_y + 15, 2, 2))
        else:
            pygame.draw.line(self.screen, COR_BORDA, 
                             (self.x + 13, base_y + 16), (self.x + 17, base_y + 16), 2)
            pygame.draw.line(self.screen, COR_BORDA, 
                             (self.x + 22, base_y + 16), (self.x + 26, base_y + 16), 2)
        
        
        antena_x = self.x + 20
        pygame.draw.line(self.screen, (150, 150, 160), 
                         (antena_x, base_y + 8), (antena_x, base_y - 2), 2)
        
        
        luz_cor = COR_ANTENA if (pygame.time.get_ticks() // 600) % 2 == 0 else (255, 200, 100)
        pygame.draw.circle(self.screen, luz_cor, (antena_x, base_y - 4), 4)
        pygame.draw.circle(self.screen, (255, 255, 255), (antena_x - 1, base_y - 5), 2)
        
        
        roda_offset = math.sin(self.frame_atual * 0.3) * 2 if self.andando else 0
        
        
        pygame.draw.rect(self.screen, COR_CORPO_ESCURA, 
                         (self.x + 8, base_y + self.altura - 7 + roda_offset, 8, 6))
        
        
        pygame.draw.rect(self.screen, COR_CORPO_ESCURA, 
                         (self.x + 24, base_y + self.altura - 7 - roda_offset, 8, 6))
        
        
        if self.andando:
            for i in range(2):
                offset = i * 6
                alpha = 100 - (i * 50)
                particula = pygame.Surface((3, 3))
                particula.set_alpha(alpha)
                particula.fill(COR_CORPO_PRINCIPAL)
                self.screen.blit(particula, 
                                 (self.x + 20 - (offset * self.direcao), base_y + self.altura - 8))
    
    def desenhar(self):
        if self.usar_imagem:
            imagem_draw = self.imagem
            if self.direcao == -1:
                imagem_draw = pygame.transform.flip(self.imagem, True, False)
            self.screen.blit(imagem_draw, (self.x, self.y))
        else:
            self.desenhar_robo_pixelart()
    
    def mover(self, teclas, limite_x, limite_y):
        moveu = False
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade
            self.direcao = -1
            moveu = True
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade
            self.direcao = 1
            moveu = True
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.velocidade
            moveu = True
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.velocidade
            moveu = True
        
        self.andando = moveu
        if moveu:
            self.tempo_frame += 1
            if self.tempo_frame >= self.velocidade_animacao:
                self.frame_atual += 1
                self.tempo_frame = 0
        else:
            self.frame_atual = 0
        
        
        self.x = max(0, min(self.x, limite_x - self.largura))
        self.y = max(100, min(self.y, limite_y - self.altura))
    
    def get_rect(self):
        
        return pygame.Rect(self.x + 5, self.y + 20, self.largura - 10, self.altura - 25)



class PortaSala:
    """Porta de sala estilo BitStart - vista de cima"""
    
    def __init__(self, x, y, numero, nome, desbloqueada=False):
        self.x = x
        self.y = y
        self.numero = numero
        self.nome = nome
        self.desbloqueada = desbloqueada
        self.largura = 100
        self.altura = 80
        self.hover_scale = 0
        
        
        cores_salas = [
            (255, 165, 80),   # Laranja - SALA 0 (Variáveis)
            (100, 200, 120),  # Verde - SALA 1 (Condicionais)
            (100, 180, 255),  # Azul - SALA 2 (Loops)
            (255, 140, 180),  # Rosa - SALA 3 (Funções)
            (200, 180, 100),  # Amarelo - SALA 4 (Arrays)
        ]
        self.cor_principal = cores_salas[numero % len(cores_salas)]
        self.cor_bloqueada = (160, 160, 170)
        self.cor_borda = (60, 60, 80)
        
    def desenhar(self, screen, font, font_pequena, robo_colidindo=False):
        cor = self.cor_principal if self.desbloqueada else self.cor_bloqueada
        
        
        if robo_colidindo and self.desbloqueada:
            self.hover_scale = min(self.hover_scale + 0.8, 6)
        else:
            self.hover_scale = max(self.hover_scale - 0.8, 0)
        
        x_draw = int(self.x - self.hover_scale / 2)
        y_draw = int(self.y - self.hover_scale / 2)
        w_draw = int(self.largura + self.hover_scale)
        h_draw = int(self.altura + self.hover_scale)
        
        
        shadow_rect = pygame.Rect(x_draw + 4, y_draw + 4, w_draw, h_draw)
        shadow_surface = pygame.Surface((w_draw, h_draw))
        shadow_surface.set_alpha(40)
        shadow_surface.fill((0, 0, 0))
        screen.blit(shadow_surface, shadow_rect)
        
        
        pygame.draw.rect(screen, self.cor_borda, 
                         (x_draw - 3, y_draw - 3, w_draw + 6, h_draw + 6), 
                         border_radius=8)
        
        
        pygame.draw.rect(screen, cor, (x_draw, y_draw, w_draw, h_draw), border_radius=6)
        
        
        pygame.draw.rect(screen, (255, 255, 255), 
                         (x_draw + 3, y_draw + 3, w_draw - 6, h_draw - 6), 
                         3, border_radius=5)
        
        
        texto_num = font.render(f"{self.numero}", True, (255, 255, 255))
        texto_rect = texto_num.get_rect(center=(x_draw + w_draw // 2, y_draw + 20))
        
        
        texto_sombra = font.render(f"{self.numero}", True, self.cor_borda)
        sombra_rect = texto_sombra.get_rect(center=(x_draw + w_draw // 2 + 2, y_draw + 22))
        screen.blit(texto_sombra, sombra_rect)
        screen.blit(texto_num, texto_rect)
        
        
        nome_curto = self.nome.split()[0][:8]  # Primeira palavra, max 8 chars
        texto_nome = font_pequena.render(nome_curto, True, (255, 255, 255))
        nome_rect = texto_nome.get_rect(center=(x_draw + w_draw // 2, y_draw + h_draw - 18))
        screen.blit(texto_nome, nome_rect)
        
        
        if not self.desbloqueada:
           
            lock_x = x_draw + w_draw // 2
            lock_y = y_draw + h_draw // 2 + 5
            pygame.draw.rect(screen, (100, 100, 110), (lock_x - 6, lock_y, 12, 10))
            pygame.draw.arc(screen, (100, 100, 110), 
                          (lock_x - 5, lock_y - 8, 10, 10), 0, math.pi, 3)
        
        
        if robo_colidindo and self.desbloqueada:
            brilho = pygame.Surface((w_draw, h_draw))
            brilho.set_alpha(40)
            brilho.fill((255, 255, 255))
            screen.blit(brilho, (x_draw, y_draw))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)




class NaveBackground:
    """Desenha a nave espacial vista de cima - formato orgânico com compartimentos para as salas"""
    
    def __init__(self, screen):
        self.screen = screen
        self.largura_tela = screen.get_width()
        self.altura_tela = screen.get_height()
        self.centro_x = self.largura_tela // 2
        self.centro_y = self.altura_tela // 2
        self.raio_nave_interno = 140  # Reduzido para as portas ficarem dentro
        
        # Paleta de cores - tons de azul/cinza metálico
        self.cor_casco_escuro = (50, 65, 85)          # Casco externo
        self.cor_casco_medio = (70, 90, 115)          # Casco médio
        self.cor_interior = (95, 120, 145)            # Interior da nave
        self.cor_interior_claro = (115, 140, 165)     # Áreas claras
        self.cor_compartimento = (60, 80, 105)        # Compartimentos das salas
        self.cor_lobby = (75, 95, 120)                # Área do lobby
        self.cor_borda = (35, 45, 60)                 # Contornos
        self.cor_detalhes_escuros = (45, 60, 80)      # Detalhes
        
        # Dimensões
        self.lobby_size = 100
        self.lobby_rect = pygame.Rect(
            self.centro_x - self.lobby_size // 2, 
            self.centro_y - self.lobby_size // 2, 
            self.lobby_size, self.lobby_size
        )

    def desenhar_geometria(self):
        """Desenha a nave espacial com formato orgânico"""
        
        self.screen.fill(COR_FUNDO_BITSTART)
        
        corpo_principal = [
            (self.centro_x, self.centro_y - 200),           # Ponta superior (nariz)
            (self.centro_x + 80, self.centro_y - 150),      # Lado direito superior
            (self.centro_x + 140, self.centro_y - 50),      # Lado direito meio-superior
            (self.centro_x + 160, self.centro_y + 50),      # Lado direito meio
            (self.centro_x + 120, self.centro_y + 120),     # Lado direito inferior
            (self.centro_x + 60, self.centro_y + 180),      # Direita base
            (self.centro_x, self.centro_y + 210),           # Centro base (traseira)
            (self.centro_x - 60, self.centro_y + 180),      # Esquerda base
            (self.centro_x - 120, self.centro_y + 120),     # Lado esquerdo inferior
            (self.centro_x - 160, self.centro_y + 50),      # Lado esquerdo meio
            (self.centro_x - 140, self.centro_y - 50),      # Lado esquerdo meio-superior
            (self.centro_x - 80, self.centro_y - 150),      # Lado esquerdo superior
        ]
        
        corpo_sombra = [(x + 5, y + 5) for x, y in corpo_principal]
        shadow_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(shadow_surface, (0, 0, 0, 60), corpo_sombra)
        self.screen.blit(shadow_surface, (0, 0))
        
        
        pygame.draw.polygon(self.screen, self.cor_borda, corpo_principal)
        
        corpo_interno = [
            (self.centro_x, self.centro_y - 194),
            (self.centro_x + 76, self.centro_y - 146),
            (self.centro_x + 135, self.centro_y - 48),
            (self.centro_x + 154, self.centro_y + 48),
            (self.centro_x + 116, self.centro_y + 117),
            (self.centro_x + 58, self.centro_y + 175),
            (self.centro_x, self.centro_y + 204),
            (self.centro_x - 58, self.centro_y + 175),
            (self.centro_x - 116, self.centro_y + 117),
            (self.centro_x - 154, self.centro_y + 48),
            (self.centro_x - 135, self.centro_y - 48),
            (self.centro_x - 76, self.centro_y - 146),
        ]
        pygame.draw.polygon(self.screen, self.cor_interior, corpo_interno)
        
        
        num_salas = 5
        raio_compartimento = 70
        
        for i in range(num_salas):
            angulo = (i * 2 * math.pi / num_salas) - math.pi / 2
            
            
            comp_x = self.centro_x + self.raio_nave_interno * math.cos(angulo)
            comp_y = self.centro_y + self.raio_nave_interno * math.sin(angulo)
            
            
            pygame.draw.circle(self.screen, self.cor_detalhes_escuros, 
                             (int(comp_x), int(comp_y)), raio_compartimento + 3)
            
           
            pygame.draw.circle(self.screen, self.cor_compartimento, 
                             (int(comp_x), int(comp_y)), raio_compartimento)
            
           
            pygame.draw.circle(self.screen, self.cor_detalhes_escuros, 
                             (int(comp_x), int(comp_y)), raio_compartimento - 15, 2)
        
       
        cockpit = [
            (self.centro_x, self.centro_y - 194),
            (self.centro_x + 45, self.centro_y - 130),
            (self.centro_x, self.centro_y - 90),
            (self.centro_x - 45, self.centro_y - 130),
        ]
        pygame.draw.polygon(self.screen, self.cor_casco_escuro, cockpit)
        pygame.draw.polygon(self.screen, self.cor_borda, cockpit, 2)
        
        
        janela_cockpit = [
            (self.centro_x, self.centro_y - 180),
            (self.centro_x + 25, self.centro_y - 145),
            (self.centro_x, self.centro_y - 120),
            (self.centro_x - 25, self.centro_y - 145),
        ]
        pygame.draw.polygon(self.screen, (40, 50, 70), janela_cockpit)
        
        
        prop_dir_x = self.centro_x + 50
        prop_dir_y = self.centro_y + 190
        pygame.draw.ellipse(self.screen, self.cor_borda,
                           (prop_dir_x - 22, prop_dir_y - 15, 44, 30))
        pygame.draw.ellipse(self.screen, self.cor_casco_escuro,
                           (prop_dir_x - 20, prop_dir_y - 13, 40, 26))
       
        pygame.draw.ellipse(self.screen, (80, 140, 220),
                           (prop_dir_x - 12, prop_dir_y - 8, 24, 16))
        pygame.draw.ellipse(self.screen, (120, 180, 255),
                           (prop_dir_x - 8, prop_dir_y - 5, 16, 10))
        

        prop_esq_x = self.centro_x - 50
        prop_esq_y = self.centro_y + 190
        pygame.draw.ellipse(self.screen, self.cor_borda,
                           (prop_esq_x - 22, prop_esq_y - 15, 44, 30))
        pygame.draw.ellipse(self.screen, self.cor_casco_escuro,
                           (prop_esq_x - 20, prop_esq_y - 13, 40, 26))
 
        pygame.draw.ellipse(self.screen, (80, 140, 220),
                           (prop_esq_x - 12, prop_esq_y - 8, 24, 16))
        pygame.draw.ellipse(self.screen, (120, 180, 255),
                           (prop_esq_x - 8, prop_esq_y - 5, 16, 10))
        
     
        prop_center_y = self.centro_y + 200
        pygame.draw.ellipse(self.screen, self.cor_borda,
                           (self.centro_x - 16, prop_center_y - 10, 32, 20))
        pygame.draw.ellipse(self.screen, self.cor_casco_escuro,
                           (self.centro_x - 14, prop_center_y - 8, 28, 16))
        pygame.draw.ellipse(self.screen, (80, 140, 220),
                           (self.centro_x - 8, prop_center_y - 5, 16, 10))
        
       
        

        pygame.draw.line(self.screen, self.cor_detalhes_escuros,
                        (self.centro_x, self.centro_y - 170),
                        (self.centro_x, self.centro_y + 150), 2)
        
      
        for i in range(4):
            y_offset = -80 + (i * 60)
        
            pygame.draw.rect(self.screen, self.cor_detalhes_escuros,
                           (self.centro_x + 80, self.centro_y + y_offset, 30, 20), 
                           border_radius=4)
           
            pygame.draw.rect(self.screen, self.cor_detalhes_escuros,
                           (self.centro_x - 110, self.centro_y + y_offset, 30, 20), 
                           border_radius=4)
        

        
   
        pygame.draw.rect(self.screen, self.cor_borda, 
                        self.lobby_rect.inflate(8, 8), border_radius=12)
        
  
        pygame.draw.rect(self.screen, self.cor_lobby, 
                        self.lobby_rect, border_radius=10)
        
   
        grid_size = 20
        for x in range(self.lobby_rect.left + grid_size, 
                      self.lobby_rect.right, grid_size):
            pygame.draw.line(self.screen, self.cor_detalhes_escuros,
                           (x, self.lobby_rect.top + 5),
                           (x, self.lobby_rect.bottom - 5), 1)
        for y in range(self.lobby_rect.top + grid_size, 
                      self.lobby_rect.bottom, grid_size):
            pygame.draw.line(self.screen, self.cor_detalhes_escuros,
                           (self.lobby_rect.left + 5, y),
                           (self.lobby_rect.right - 5, y), 1)
        
 
        pygame.draw.circle(self.screen, self.cor_detalhes_escuros,
                          (self.centro_x, self.centro_y), 15, 2)

    def desenhar_linhas_conexao(self, portas):
        """Desenha as linhas conectando o lobby às salas"""
        for porta in portas:
            if porta.desbloqueada:
                cor_linha = porta.cor_principal
                porta_centro_x = porta.x + porta.largura // 2
                porta_centro_y = porta.y + porta.altura // 2
                
                linha_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                
                # Linha de conexão (corredor)
                pygame.draw.line(linha_surface, (*self.cor_borda, 120), 
                                (self.centro_x, self.centro_y), 
                                (porta_centro_x, porta_centro_y), 10)
                pygame.draw.line(linha_surface, (*cor_linha, 150), 
                                (self.centro_x, self.centro_y), 
                                (porta_centro_x, porta_centro_y), 6)
                
                self.screen.blit(linha_surface, (0, 0))

class MundoTela:
    """Tela do mundo - Estilo BitStart com nave vista de cima"""
    
    def __init__(self, screen, clock, usuario, progresso_salas):
        self.screen = screen
        self.clock = clock
        self.usuario = usuario
        self.progresso_salas = progresso_salas  # [score_1, score_2, score_3, score_4]
        self.font_path = "src/fonts/Grand9K Pixel.ttf"
        
        # NOVO: Inicializa o background da nave
        self.nave_bg = NaveBackground(screen)

        # Carrega fontes
        try:
            
            self.font_grande = pygame.font.Font(self.font_path, 42)
            self.font_media = pygame.font.Font(self.font_path, 32)
            self.font_pequena = pygame.font.Font(self.font_path, 16)
        except:
            self.font_grande = pygame.font.SysFont(None, 42)
            self.font_media = pygame.font.SysFont(None, 32)
            self.font_pequena = pygame.font.SysFont(None, 16)
        
     
        largura_tela = screen.get_width()
        altura_tela = screen.get_height()
        

        self.robo = Robo(largura_tela // 2 - 20, altura_tela // 2 + 10, screen) 
        
     
        centro_x = self.nave_bg.centro_x
        centro_y = self.nave_bg.centro_y
        raio = self.nave_bg.raio_nave_interno
        
        self.portas = []
        num_salas = 5
        for i in range(num_salas):
            
            angulo = (i * 2 * math.pi / num_salas) - math.pi / 2 
            x = centro_x + raio * math.cos(angulo) - 50
            y = centro_y + raio * math.sin(angulo) - 40
            
            # Nomes das salas - última é Menu
            nomes = ["Variáveis", "Condicionais", "Loops", "Vetores", "Menu"]
            
            # Lógica de desbloqueio baseada no progresso
            # Sala 0 sempre desbloqueada
            # Salas 1-3 desbloqueadas se a anterior tem score >= 2
            # Sala 4 (Menu) sempre desbloqueada
            if i == 0 or i == 4:  # Primeira sala e Menu sempre desbloqueados
                desbloqueada = True
            elif i <= 3:  # Salas de conteúdo
                desbloqueada = progresso_salas[i - 1] >= 2  # Desbloqueia se anterior tem pelo menos 2 acertos
            else:
                desbloqueada = True
            
            self.portas.append(
                PortaSala(int(x), int(y), i, nomes[i], desbloqueada)
            )
        
        self.mensagem = ""
        self.mensagem_timer = 0
        self.mensagem_cor = (80, 80, 80)
        self.grid_pontos = [] # Removido para interior mais limpo
    
    def desenhar_nave(self):
        """Desenha a nave usando a classe NaveBackground e adiciona o texto LOBBY."""
        
       
        self.nave_bg.desenhar_geometria()
        
       
        self.nave_bg.desenhar_linhas_conexao(self.portas)

        centro_x = self.nave_bg.centro_x
        centro_y = self.nave_bg.centro_y
        
        
        lobby_texto = self.font_media.render("LOBBY", True, (255, 255, 255))
        lobby_rect_text = lobby_texto.get_rect(center=(centro_x, centro_y))
        
       
        lobby_sombra = self.font_media.render("LOBBY", True, (60, 70, 100))
        sombra_rect = lobby_sombra.get_rect(center=(centro_x + 2, centro_y + 2))
        self.screen.blit(lobby_sombra, sombra_rect)
        self.screen.blit(lobby_texto, lobby_rect_text)
    
    def desenhar_hud(self):
        """HUD superior estilo BitStart com logo"""
       
        barra_altura = 100
        pygame.draw.rect(self.screen, COR_FUNDO_BITSTART, (0, 0, self.screen.get_width(), barra_altura))
        pygame.draw.rect(self.screen, (100, 200, 120), 
                         (0, barra_altura - 4, self.screen.get_width(), 4))
        
       
        try:
           
            logo_img = pygame.image.load("src/img/logo.png")
            logo_img = pygame.transform.scale(logo_img, (logo_img.get_width() // 3, logo_img.get_height() // 3))
            logo_rect = logo_img.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(logo_img, logo_rect)
        except:
           
            titulo_bit = self.font_grande.render("Bit", True, (100, 200, 120))
            titulo_start = self.font_grande.render("Start", True, (255, 165, 80))
            self.screen.blit(titulo_bit, (self.screen.get_width() // 2 - 80, 25))
            self.screen.blit(titulo_start, (self.screen.get_width() // 2 - 10, 25))
    
    def atualizar_salas_desbloqueadas(self, progresso_salas):
        """Atualiza o desbloqueio das salas baseado no progresso do BD"""
        self.progresso_salas = progresso_salas
        for i, porta in enumerate(self.portas):
            if i == 0 or i == 4:  # Primeira sala e Menu sempre desbloqueados
                porta.desbloqueada = True
            elif i <= 3:  # Salas de conteúdo
                porta.desbloqueada = progresso_salas[i - 1] >= 2  # Requer pelo menos 2 acertos
    
    def verificar_colisao(self):
        robo_rect = self.robo.get_rect()
        for porta in self.portas:
            if robo_rect.colliderect(porta.get_rect()):
                return porta
        return None
    
    def mostrar_mensagem(self, texto, duracao=120, cor=(255, 100, 100)):
        self.mensagem = texto
        self.mensagem_timer = duracao
        self.mensagem_cor = cor
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit("Usuário saiu do jogo.")
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        porta = self.verificar_colisao()
                        if porta:
                            if porta.desbloqueada:
                                # Sala 4 é o Menu - retorna -1 para voltar ao menu
                                if porta.numero == 4:
                                    return -1
                                return porta.numero
                            else:
                                self.mostrar_mensagem("⚠ Sala bloqueada! Faça 2+ acertos na anterior", 150)
            
            # Movimento
            teclas = pygame.key.get_pressed()
            self.robo.mover(teclas, self.screen.get_width(), self.screen.get_height())
            
            porta_colisao = self.verificar_colisao()
            
            
            self.desenhar_nave()
            
           
            for porta in self.portas:
                porta.desenhar(self.screen, self.font_media, self.font_pequena, 
                               robo_colidindo=(porta == porta_colisao))
            
           
            self.robo.desenhar()
            
        
            self.desenhar_hud()
            
        
            barra_y = self.screen.get_height() - 70
            pygame.draw.rect(self.screen, (255, 255, 255), 
                             (0, barra_y, self.screen.get_width(), 70))
            pygame.draw.rect(self.screen, (100, 200, 120), 
                             (0, barra_y, self.screen.get_width(), 3))
            
          
            if porta_colisao:
                if porta_colisao.desbloqueada:
                    # Mensagem diferente para porta Menu
                    if porta_colisao.numero == 4:
                        instrucao = self.font_pequena.render(
                            "Pressione ENTER para voltar ao Menu", True, (255, 165, 80))
                    else:
                        instrucao = self.font_pequena.render(
                            "Pressione ENTER para entrar na sala", True, (100, 200, 120))
                else:
                    instrucao = self.font_pequena.render(
                        "BLOQUEADA - Faça 2+ acertos na sala anterior", True, (255, 100, 100))
                
            
                if (pygame.time.get_ticks() // 400) % 2 == 0:
                    instrucao_rect = instrucao.get_rect(
                        center=(self.screen.get_width() // 2, barra_y + 35))
                    self.screen.blit(instrucao, instrucao_rect)
            else:
                instrucao = self.font_pequena.render(
                    "Setas: Mover  |  Enter: Entrar/Selecionar", True, (120, 120, 120))
                instrucao_rect = instrucao.get_rect(
                    center=(self.screen.get_width() // 2, barra_y + 35))
                self.screen.blit(instrucao, instrucao_rect)
            
         
            if self.mensagem_timer > 0:
                msg_surface = self.font_pequena.render(self.mensagem, True, self.mensagem_cor)
                msg_rect = msg_surface.get_rect(center=(self.screen.get_width() // 2, 
                                                         self.screen.get_height() // 2 - 150))
                
                padding = 15
                fundo_rect = pygame.Rect(msg_rect.x - padding, msg_rect.y - padding,
                                         msg_rect.width + padding * 2, msg_rect.height + padding * 2)
                pygame.draw.rect(self.screen, (255, 255, 255), fundo_rect, border_radius=8)
                pygame.draw.rect(self.screen, self.mensagem_cor, fundo_rect, 3, border_radius=8)
                
                self.screen.blit(msg_surface, msg_rect)
                self.mensagem_timer -= 1
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return None