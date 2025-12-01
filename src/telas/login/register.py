import pygame
from src.services.user_service import UserService


class RegisterScreen:
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
            font = pygame.font.Font(font_path, 18)
        except Exception:
            font = pygame.font.SysFont(None, 18)

        nome = ""
        email = ""
        senha = ""
        matricula = ""
        id_turma = ""
        active = 0  # 0=none,1=nome,2=email,3=senha,4=matricula,5=id_turma
        error = None
        success = None

        running = True
        while running:
            # Precompute link rect so clicks can be detected in the event loop
            link_font = pygame.font.Font(font_path, 16) if pygame.font else pygame.font.SysFont(None, 16)
            link_text = link_font.render("Já tem uma conta? conecte-se aqui", True, (20, 100, 200))
            link_rect = link_text.get_rect(topleft=(250, 530))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    # Click areas for each input (coords match drawn rects)
                    if 250 <= mx <= 750 and 120 <= my <= 160:
                        active = 1
                    elif 250 <= mx <= 750 and 190 <= my <= 230:
                        active = 2
                    elif 250 <= mx <= 750 and 260 <= my <= 300:
                        active = 3
                    elif 250 <= mx <= 750 and 330 <= my <= 370:
                        active = 4
                    elif 250 <= mx <= 750 and 400 <= my <= 440:
                        active = 5
                    else:
                        active = 0

                   
                    if 400 <= mx <= 600 and 470 <= my <= 510:
                        try:
                            payload_usuario = {
                                "nome": nome,
                                "email": email,
                                "senha": senha,
                                "tipo": "aluno"
                            }
                            payload_aluno = {
                                "matricula": matricula,
                                "id_turma": int(id_turma) if id_turma.isdigit() else None
                            }
                            if payload_aluno["id_turma"] is None:
                                raise ValueError("ID da turma deve ser um número")

                            self.user_service.criar_aluno(payload_usuario, payload_aluno)
                            success = "Usuário criado com sucesso. Fazendo login..."
                          
                            try:
                                self.user_service.autenticar(email, senha)
                                return True
                            except Exception:
                                return True
                        except Exception as e:
                            error = str(e)
               
                    if link_rect.collidepoint((mx, my)):
                        return False

                if event.type == pygame.KEYDOWN:
                    if active == 1:
                        if event.key == pygame.K_BACKSPACE:
                            nome = nome[:-1]
                        else:
                            nome += event.unicode
                    elif active == 2:
                        if event.key == pygame.K_BACKSPACE:
                            email = email[:-1]
                        else:
                            email += event.unicode
                    elif active == 3:
                        if event.key == pygame.K_BACKSPACE:
                            senha = senha[:-1]
                        else:
                            senha += event.unicode
                    elif active == 4:
                        if event.key == pygame.K_BACKSPACE:
                            matricula = matricula[:-1]
                        else:
                            matricula += event.unicode
                    elif active == 5:
                        if event.key == pygame.K_BACKSPACE:
                            id_turma = id_turma[:-1]
                        elif event.key == pygame.K_RETURN:
                            pass
                        else:
                            id_turma += event.unicode

            self.screen.fill((252, 255, 217))

            title_font = pygame.font.Font(font_path, 30) if pygame.font else pygame.font.SysFont(None, 30)
            title_surf = title_font.render("Criar Conta (Aluno)", True, (0, 0, 0))
            title_rect = title_surf.get_rect(center=(500, 80))
            self.screen.blit(title_surf, title_rect)

           
            self._draw_text("Nome:", font, (0, 0, 0), 250, 90)
            nome_rect = pygame.Rect(250, 120, 500, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), nome_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), nome_rect, 2 if active == 1 else 1)
            self.screen.blit(font.render(nome, True, (0, 0, 0)), (nome_rect.x + 8, nome_rect.y + 8))

            self._draw_text("Email:", font, (0, 0, 0), 250, 160)
            email_rect = pygame.Rect(250, 190, 500, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), email_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), email_rect, 2 if active == 2 else 1)
            self.screen.blit(font.render(email, True, (0, 0, 0)), (email_rect.x + 8, email_rect.y + 8))

  
            self._draw_text("Senha:", font, (0, 0, 0), 250, 230)
            senha_rect = pygame.Rect(250, 260, 500, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), senha_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), senha_rect, 2 if active == 3 else 1)
            senha_mask = "*" * len(senha)
            self.screen.blit(font.render(senha_mask, True, (0, 0, 0)), (senha_rect.x + 8, senha_rect.y + 8))

     
            self._draw_text("Matrícula:", font, (0, 0, 0), 250, 300)
            mat_rect = pygame.Rect(250, 330, 500, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), mat_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), mat_rect, 2 if active == 4 else 1)
            self.screen.blit(font.render(matricula, True, (0, 0, 0)), (mat_rect.x + 8, mat_rect.y + 8))

  
            self._draw_text("ID Turma:", font, (0, 0, 0), 250, 370)
            turma_rect = pygame.Rect(250, 400, 500, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), turma_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), turma_rect, 2 if active == 5 else 1)
            self.screen.blit(font.render(id_turma, True, (0, 0, 0)), (turma_rect.x + 8, turma_rect.y + 8))

          
            reg_rect = pygame.Rect(400, 470, 200, 40)
            pygame.draw.rect(self.screen, (34, 139, 34), reg_rect)
            reg_text = font.render("Criar Conta", True, (255, 255, 255))
            self.screen.blit(reg_text, reg_text.get_rect(center=reg_rect.center))

            link_font = pygame.font.Font(font_path, 16) if pygame.font else pygame.font.SysFont(None, 16)
            link_text = link_font.render("Já tem uma conta? conecte-se aqui", True, (20, 100, 200))
            link_rect = link_text.get_rect(topleft=(250, 530))
            self.screen.blit(link_text, link_rect)

            if error:
                self.screen.blit(font.render(str(error), True, (200, 30, 30)), (250, 510))
                print("Erro no registro:", error)
            if success:
                self.screen.blit(font.render(str(success), True, (30, 120, 30)), (250, 510))

            pygame.display.flip()
            self.clock.tick(30)

        return False
