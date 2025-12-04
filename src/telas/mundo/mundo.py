import pygame
import math
import random


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
            self.imagem = pygame.image.load("src/img/robo.png").convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem, (self.largura, self.altura))
            self.usar_imagem = True
        except:
            self.usar_imagem = False
        
    def desenhar_robo_pixelart(self):
        """Desenha um robô estilo pixel art com animação - estilo BitStart"""
        # Offset de bobbing ao caminhar
        bob_offset = 0
        if self.andando:
            bob_offset = abs(math.sin(self.frame_atual * 0.5)) * 2
        
        base_y = self.y + bob_offset
        
        # Cores do robô - seguindo paleta BitStart
        COR_CORPO_PRINCIPAL = (100, 180, 255)  # Azul
        COR_CORPO_ESCURA = (60, 120, 200)
        COR_OLHOS = (0, 255, 200)
        COR_ANTENA = (255, 140, 80)
        COR_BORDA = (40, 40, 60)
        
        # Sombra simples
        shadow_surface = pygame.Surface((self.largura, 6))
        shadow_surface.set_alpha(60)
        shadow_surface.fill((0, 0, 0))
        self.screen.blit(shadow_surface, (self.x, base_y + self.altura))
        
        # Corpo principal
        corpo_rect = pygame.Rect(self.x + 5, base_y + 20, self.largura - 10, self.altura - 25)
        pygame.draw.rect(self.screen, COR_BORDA, corpo_rect.inflate(4, 4))
        pygame.draw.rect(self.screen, COR_CORPO_PRINCIPAL, corpo_rect)
        
        # Detalhe interno do corpo
        pygame.draw.rect(self.screen, COR_CORPO_ESCURA, 
                        pygame.Rect(self.x + 12, base_y + 28, 16, 14))
        
        # Cabeça
        cabeca_rect = pygame.Rect(self.x + 8, base_y + 8, 24, 16)
        pygame.draw.rect(self.screen, COR_BORDA, cabeca_rect.inflate(3, 3))
        pygame.draw.rect(self.screen, COR_CORPO_PRINCIPAL, cabeca_rect)
        
        # Olhos
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
        
        # Antena
        antena_x = self.x + 20
        pygame.draw.line(self.screen, (150, 150, 160), 
                        (antena_x, base_y + 8), (antena_x, base_y - 2), 2)
        
        # Luz da antena piscante
        luz_cor = COR_ANTENA if (pygame.time.get_ticks() // 600) % 2 == 0 else (255, 200, 100)
        pygame.draw.circle(self.screen, luz_cor, (antena_x, base_y - 4), 4)
        pygame.draw.circle(self.screen, (255, 255, 255), (antena_x - 1, base_y - 5), 2)
        
        # Rodas/pernas
        roda_offset = math.sin(self.frame_atual * 0.3) * 2 if self.andando else 0
        
        # Perna esquerda
        pygame.draw.rect(self.screen, COR_CORPO_ESCURA, 
                        (self.x + 8, base_y + self.altura - 7 + roda_offset, 8, 6))
        
        # Perna direita
        pygame.draw.rect(self.screen, COR_CORPO_ESCURA, 
                        (self.x + 24, base_y + self.altura - 7 - roda_offset, 8, 6))
        
        # Partículas de movimento
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
        
        # Limita movimento
        self.x = max(0, min(self.x, limite_x - self.largura))
        self.y = max(100, min(self.y, limite_y - self.altura))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)


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
        
        # Cores por sala (rotacionando entre as cores do BitStart)
        cores_salas = [
            (255, 165, 80),   # Laranja - SALA 0
            (100, 200, 120),  # Verde - SALA 1
            (100, 180, 255),  # Azul - SALA 2
            (255, 140, 180),  # Rosa - SALA 3
            (200, 180, 100),  # Amarelo - SALA 4
        ]
        self.cor_principal = cores_salas[numero % len(cores_salas)]
        self.cor_bloqueada = (160, 160, 170)
        self.cor_borda = (60, 60, 80)
        
    def desenhar(self, screen, font, font_pequena, robo_colidindo=False):
        cor = self.cor_principal if self.desbloqueada else self.cor_bloqueada
        
        # Hover effect
        if robo_colidindo and self.desbloqueada:
            self.hover_scale = min(self.hover_scale + 0.8, 6)
        else:
            self.hover_scale = max(self.hover_scale - 0.8, 0)
        
        x_draw = int(self.x - self.hover_scale / 2)
        y_draw = int(self.y - self.hover_scale / 2)
        w_draw = int(self.largura + self.hover_scale)
        h_draw = int(self.altura + self.hover_scale)
        
        # Sombra
        shadow_rect = pygame.Rect(x_draw + 4, y_draw + 4, w_draw, h_draw)
        shadow_surface = pygame.Surface((w_draw, h_draw))
        shadow_surface.set_alpha(40)
        shadow_surface.fill((0, 0, 0))
        screen.blit(shadow_surface, shadow_rect)
        
        # Borda grossa estilo pixel art
        pygame.draw.rect(screen, self.cor_borda, 
                        (x_draw - 3, y_draw - 3, w_draw + 6, h_draw + 6), 
                        border_radius=8)
        
        # Corpo da porta
        pygame.draw.rect(screen, cor, (x_draw, y_draw, w_draw, h_draw), border_radius=6)
        
        # Borda interna clara
        pygame.draw.rect(screen, (255, 255, 255), 
                        (x_draw + 3, y_draw + 3, w_draw - 6, h_draw - 6), 
                        3, border_radius=5)
        
        # Número da sala
        texto_num = font.render(f"{self.numero}", True, (255, 255, 255))
        texto_rect = texto_num.get_rect(center=(x_draw + w_draw // 2, y_draw + 20))
        
        # Sombra do número
        texto_sombra = font.render(f"{self.numero}", True, self.cor_borda)
        sombra_rect = texto_sombra.get_rect(center=(x_draw + w_draw // 2 + 2, y_draw + 22))
        screen.blit(texto_sombra, sombra_rect)
        screen.blit(texto_num, texto_rect)
        
        # Nome da sala (resumido)
        nome_curto = self.nome.split()[0][:8]  # Primeira palavra, max 8 chars
        texto_nome = font_pequena.render(nome_curto, True, (255, 255, 255))
        nome_rect = texto_nome.get_rect(center=(x_draw + w_draw // 2, y_draw + h_draw - 18))
        screen.blit(texto_nome, nome_rect)
        
        # Ícone de status
        if not self.desbloqueada:
            # Cadeado simples
            lock_x = x_draw + w_draw // 2
            lock_y = y_draw + h_draw // 2 + 5
            pygame.draw.rect(screen, (100, 100, 110), (lock_x - 6, lock_y, 12, 10))
            pygame.draw.arc(screen, (100, 100, 110), 
                          (lock_x - 5, lock_y - 8, 10, 10), 0, 3.14159, 3)
        
        # Efeito de brilho no hover
        if robo_colidindo and self.desbloqueada:
            brilho = pygame.Surface((w_draw, h_draw))
            brilho.set_alpha(40)
            brilho.fill((255, 255, 255))
            screen.blit(brilho, (x_draw, y_draw))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)


class MundoTela:
    """Tela do mundo - Estilo BitStart com nave vista de cima"""
    
    def __init__(self, screen, clock, usuario, sala_atual=0):
        self.screen = screen
        self.clock = clock
        self.usuario = usuario
        self.sala_atual = sala_atual
        self.font_path = "src/fonts/Grand9K Pixel.ttf"
        
        # Carrega fontes
        try:
            self.font_grande = pygame.font.Font(self.font_path, 42)
            self.font_media = pygame.font.Font(self.font_path, 32)
            self.font_pequena = pygame.font.Font(self.font_path, 16)
        except:
            self.font_grande = pygame.font.SysFont(None, 42)
            self.font_media = pygame.font.SysFont(None, 32)
            self.font_pequena = pygame.font.SysFont(None, 16)
        
        # Cria o robô
        largura_tela = screen.get_width()
        altura_tela = screen.get_height()
        self.robo = Robo(largura_tela // 2 - 20, altura_tela // 2 + 80, screen)
        
        # Layout da nave em formato circular ao redor do lobby
        centro_x = largura_tela // 2
        centro_y = altura_tela // 2
        raio = 180
        
        self.portas = []
        num_salas = 5
        for i in range(num_salas):
            angulo = (i * 2 * math.pi / num_salas) - math.pi / 2  # Começa no topo
            x = centro_x + raio * math.cos(angulo) - 50
            y = centro_y + raio * math.sin(angulo) - 40
            
            nomes = ["Variáveis", "Condicionais", "Loops", "Funções", "Arrays"]
            self.portas.append(
                PortaSala(int(x), int(y), i, nomes[i], i == 0 or sala_atual >= i)
            )
        
        self.mensagem = ""
        self.mensagem_timer = 0
        self.mensagem_cor = (80, 80, 80)
        
        # Decorações da nave (pontos no grid)
        self.grid_pontos = []
        for i in range(20):
            self.grid_pontos.append({
                'x': random.randint(50, largura_tela - 50),
                'y': random.randint(150, altura_tela - 100),
                'size': random.choice([1, 2]),
                'cor': random.choice([(180, 200, 220), (200, 180, 200)])
            })
    
    def desenhar_nave(self):
        """Desenha a nave vista de cima - estilo lobby central"""
        centro_x = self.screen.get_width() // 2
        centro_y = self.screen.get_height() // 2
        
        # Grid de fundo sutil
        cor_grid = (220, 230, 240)
        for x in range(0, self.screen.get_width(), 40):
            pygame.draw.line(self.screen, cor_grid, (x, 100), (x, self.screen.get_height() - 80), 1)
        for y in range(100, self.screen.get_height() - 80, 40):
            pygame.draw.line(self.screen, cor_grid, (0, y), (self.screen.get_width(), y), 1)
        
        # Pontos decorativos
        for ponto in self.grid_pontos:
            pygame.draw.circle(self.screen, ponto['cor'], (ponto['x'], ponto['y']), ponto['size'])
        
        # Lobby central (área escura)
        lobby_size = 160
        lobby_rect = pygame.Rect(centro_x - lobby_size // 2, centro_y - lobby_size // 2, 
                                lobby_size, lobby_size)
        
        # Sombra do lobby
        shadow_rect = lobby_rect.inflate(8, 8)
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height))
        shadow_surface.set_alpha(30)
        shadow_surface.fill((0, 0, 0))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Borda do lobby
        pygame.draw.rect(self.screen, (80, 90, 120), lobby_rect.inflate(10, 10), border_radius=15)
        pygame.draw.rect(self.screen, (120, 140, 180), lobby_rect, border_radius=12)
        
        # Texto LOBBY
        lobby_texto = self.font_media.render("LOBBY", True, (255, 255, 255))
        lobby_rect_text = lobby_texto.get_rect(center=(centro_x, centro_y))
        
        # Sombra do texto
        lobby_sombra = self.font_media.render("LOBBY", True, (60, 70, 100))
        sombra_rect = lobby_sombra.get_rect(center=(centro_x + 2, centro_y + 2))
        self.screen.blit(lobby_sombra, sombra_rect)
        self.screen.blit(lobby_texto, lobby_rect_text)
        
        # Linhas conectando lobby às salas
        for porta in self.portas:
            if porta.desbloqueada:
                cor_linha = porta.cor_principal
                porta_centro_x = porta.x + porta.largura // 2
                porta_centro_y = porta.y + porta.altura // 2
                
                # Linha com transparência
                linha_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                pygame.draw.line(linha_surface, (*cor_linha, 100), 
                               (centro_x, centro_y), 
                               (porta_centro_x, porta_centro_y), 3)
                self.screen.blit(linha_surface, (0, 0))
    
    def desenhar_hud(self):
        """HUD superior estilo BitStart com logo"""
        # Barra superior
        barra_altura = 100
        pygame.draw.rect(self.screen, (252, 255, 217), (0, 0, self.screen.get_width(), barra_altura))
        pygame.draw.rect(self.screen, (100, 200, 120), 
                        (0, barra_altura - 4, self.screen.get_width(), 4))
        
        # Carrega e desenha a logo (igual ao menu)
        try:
            logo_img = pygame.image.load("src/img/logo.png")
            logo_img = pygame.transform.scale(logo_img, (logo_img.get_width() // 3, logo_img.get_height() // 3))
            logo_rect = logo_img.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(logo_img, logo_rect)
        except:
            # Fallback se não carregar a imagem
            titulo_bit = self.font_grande.render("Bit", True, (100, 200, 120))
            titulo_start = self.font_grande.render("Start", True, (255, 165, 80))
            self.screen.blit(titulo_bit, (self.screen.get_width() // 2 - 80, 25))
            self.screen.blit(titulo_start, (self.screen.get_width() // 2 - 10, 25))
    
    def atualizar_salas_desbloqueadas(self, sala_completada):
        self.sala_atual = sala_completada + 1
        for i, porta in enumerate(self.portas):
            porta.desbloqueada = i <= self.sala_atual
    
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
                                return porta.numero
                            else:
                                self.mostrar_mensagem("⚠ Sala bloqueada! Complete a anterior", 150)
                    
                    if event.key == pygame.K_ESCAPE:
                        return -1
            
            # Movimento
            teclas = pygame.key.get_pressed()
            self.robo.mover(teclas, self.screen.get_width(), self.screen.get_height())
            
            porta_colisao = self.verificar_colisao()
            
            # Desenha tudo
            self.screen.fill((252, 255, 217))  # Fundo bege do BitStart
            
            self.desenhar_nave()
            
            # Desenha portas
            for porta in self.portas:
                porta.desenhar(self.screen, self.font_media, self.font_pequena, 
                             robo_colidindo=(porta == porta_colisao))
            
            # Desenha robô
            self.robo.desenhar()
            
            # HUD
            self.desenhar_hud()
            
            # Barra inferior
            barra_y = self.screen.get_height() - 70
            pygame.draw.rect(self.screen, (255, 255, 255), 
                           (0, barra_y, self.screen.get_width(), 70))
            pygame.draw.rect(self.screen, (100, 200, 120), 
                           (0, barra_y, self.screen.get_width(), 3))
            
            # Instruções
            if porta_colisao:
                if porta_colisao.desbloqueada:
                    instrucao = self.font_pequena.render(
                        "Pressione ENTER para entrar na sala", True, (100, 200, 120))
                else:
                    instrucao = self.font_pequena.render(
                        "BLOQUEADA - Complete a sala anterior", True, (255, 100, 100))
                
                # Piscar
                if (pygame.time.get_ticks() // 400) % 2 == 0:
                    instrucao_rect = instrucao.get_rect(
                        center=(self.screen.get_width() // 2, barra_y + 35))
                    self.screen.blit(instrucao, instrucao_rect)
            else:
                instrucao = self.font_pequena.render(
                    "Setas: Mover  |  Enter: Entrar  |  Esc: Menu", True, (120, 120, 120))
                instrucao_rect = instrucao.get_rect(
                    center=(self.screen.get_width() // 2, barra_y + 35))
                self.screen.blit(instrucao, instrucao_rect)
            
            # Mensagem temporária
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