import pygame
from src.services.user_service import UserService
from src.telas.login.register import RegisterScreen
from src.componentes.botao import Botao


class LoginScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.user_service = UserService()

    def _draw_text(self, text, font, color, x, y):
        surf = font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def run(self) -> bool:
        pygame.key.set_repeat(300, 50)
        font_path = "src/fonts/Grand9K Pixel.ttf"
        try:
            font = pygame.font.Font(font_path, 20)
        except Exception:
            font = pygame.font.SysFont(None, 24)

        email = ""
        senha = ""
        active = 0  # 0 = none, 1 = email, 2 = senha
        error = None

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, None
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    # email box
                    if 250 <= mx <= 750 and 220 <= my <= 260:
                        active = 1
                        error = None  # Limpar erro ao clicar
                    elif 250 <= mx <= 750 and 300 <= my <= 340:
                        active = 2
                        error = None  # Limpar erro ao clicar
                    else:
                        active = 0
                        
                    # login button
                    if 425 <= mx <= 575 and 380 <= my <= 420:
                        if not email or not senha:
                            error = "Preencha email e senha!"
                        else:
                            try:
                                usuario = self.user_service.autenticar(email, senha)
                                if usuario:  # ← VERIFICAÇÃO ADICIONADA
                                    print(f"✅ Login bem-sucedido: {usuario['nome']}")
                                    return True, usuario
                                else:
                                    error = "Email ou senha incorretos!"
                            except Exception as e:
                                error = f"Erro: {str(e)}"
                                print(f"❌ Erro de autenticação: {e}")

                if event.type == pygame.KEYDOWN:
                    if active == 1:
                        if event.key == pygame.K_BACKSPACE:
                            email = email[:-1]
                        elif event.key == pygame.K_TAB:
                            active = 2
                        elif event.key == pygame.K_RETURN:
                            active = 2
                        else:
                            email += event.unicode
                    elif active == 2:
                        if event.key == pygame.K_BACKSPACE:
                            senha = senha[:-1]
                        elif event.key == pygame.K_RETURN:
                            if not email or not senha:
                                error = "Preencha email e senha!"
                            else:
                                try:
                                    usuario = self.user_service.autenticar(email, senha)
                                    if usuario:  # ← VERIFICAÇÃO ADICIONADA
                                        print(f"✅ Login bem-sucedido: {usuario['nome']}")
                                        return True, usuario
                                    else:
                                        error = "Email ou senha incorretos!"
                                except Exception as e:
                                    error = f"Erro: {str(e)}"
                                    print(f"❌ Erro de autenticação: {e}")
                        else:
                            senha += event.unicode

            self.screen.fill((252, 255, 217))
            game_logo = pygame.image.load("src/img/logo.png")
            game_logo = pygame.transform.scale(game_logo, (game_logo.get_width() // 2.5, game_logo.get_height() // 2.5))
           
            logo_rect = game_logo.get_rect(center=(500, 80))
            self.screen.blit(game_logo, logo_rect)
            title_font = pygame.font.Font(font_path, 30) if pygame.font else pygame.font.SysFont(None, 30)
            title_surf = title_font.render("Login", True, (0, 0, 0))
            title_rect = title_surf.get_rect(center=(500, 160))
            self.screen.blit(title_surf, title_rect)

            # Email input
            self._draw_text("Email:", font, (0, 0, 0), 250, 190)
            email_rect = pygame.Rect(250, 220, 500, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), email_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), email_rect, 2 if active == 1 else 1)
            email_surf = font.render(email, True, (0, 0, 0))
            self.screen.blit(email_surf, (email_rect.x + 8, email_rect.y + 8))

            # Senha input
            self._draw_text("Senha:", font, (0, 0, 0), 250, 270)
            senha_rect = pygame.Rect(250, 300, 500, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), senha_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), senha_rect, 2 if active == 2 else 1)
            senha_mask = "*" * len(senha)
            senha_surf = font.render(senha_mask, True, (0, 0, 0))
            self.screen.blit(senha_surf, (senha_rect.x + 8, senha_rect.y + 8))

            # Botão de login
            botao_azul = pygame.image.load("src/img/botao/botao_azul.png").convert_alpha()
            botao_login = Botao(x=425, y=380, imagem=botao_azul, text="Entrar", escala=0.4)
            botao_login.draw(self.screen)

            # Erro
            if error:
                err_surf = font.render(error, True, (200, 30, 30))
                err_rect = err_surf.get_rect(center=(500, 450))
                self.screen.blit(err_surf, err_rect)

            # Link para registro
            link_text = font.render("Não tem uma conta? Criar", True, (20, 100, 200))
            link_rect = link_text.get_rect(topleft=(250, 480))
            self.screen.blit(link_text, link_rect)

            # Click no link de registro
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                if link_rect.collidepoint((mx, my)):
                    pygame.time.wait(200)  # Debounce
                    register = RegisterScreen(self.screen, self.clock)
                    created_user = register.run()
                    
                    # Se usuário foi criado, preencher campos automaticamente
                    if created_user:
                        email = created_user.get('email', '')
                        # Não preencher senha por segurança
                        error = "Conta criada! Digite sua senha para entrar."

            pygame.display.flip()
            self.clock.tick(30)

        return False, None