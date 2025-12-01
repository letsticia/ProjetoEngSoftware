import pygame
from src.services.user_service import UserService
from src.componentes.botao import Botao


class RegisterScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.user_service = UserService()

    def _draw_text(self, text, font, color, x, y):
        surf = font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def run(self):
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
         
            link_font = pygame.font.Font(font_path, 16) if pygame.font else pygame.font.SysFont(None, 16)
            link_text = link_font.render("Já tem uma conta? conecte-se aqui", True, (20, 100, 200))
            link_rect = link_text.get_rect(topleft=(250, 530))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    # Click areas for each input (coords match drawn rects)
                    if 250 <= mx <= 750 and 120 <= my <= 160:
                        active = 1
                        error = None  # Limpa erro ao clicar
                    elif 250 <= mx <= 750 and 190 <= my <= 230:
                        active = 2
                        error = None
                    elif 250 <= mx <= 750 and 260 <= my <= 300:
                        active = 3
                        error = None
                    elif 250 <= mx <= 750 and 330 <= my <= 370:
                        active = 4
                        error = None
                    elif 250 <= mx <= 750 and 400 <= my <= 440:
                        active = 5
                        error = None
                    else:
                        active = 0

                   
                    if 410 <= mx <= 600 and 470 <= my <= 510:
                        # Validações de campos vazios
                        if not nome.strip():
                            error = "Nome é obrigatório"
                        elif not email.strip():
                            error = "Email é obrigatório"
                        elif not senha:
                            error = "Senha é obrigatória"
                        elif not matricula.strip():
                            error = "Matrícula é obrigatória"
                        elif not id_turma.strip():
                            error = "ID da Turma é obrigatório"
                        else:
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

                                usuario_criado = self.user_service.criar_aluno(payload_usuario, payload_aluno)
                                success = "Usuário criado com sucesso!"
                                
                                # Aguarda 1 segundo para o usuário ver a mensagem
                                self.screen.fill((252, 255, 217))
                                title_font = pygame.font.Font(font_path, 30)
                                title_surf = title_font.render("Criar Conta (Aluno)", True, (0, 0, 0))
                                title_rect = title_surf.get_rect(center=(500, 80))
                                self.screen.blit(title_surf, title_rect)
                                
                                success_font = pygame.font.Font(font_path, 24)
                                success_surf = success_font.render(success, True, (30, 120, 30))
                                success_rect = success_surf.get_rect(center=(500, 300))
                                self.screen.blit(success_surf, success_rect)
                                
                                pygame.display.flip()
                                pygame.time.wait(1500)
                                
                                return usuario_criado
                                
                            except Exception as e:
                                error_msg = str(e)
                                # Traduzir erros comuns
                                if "duplicate key" in error_msg and "email" in error_msg:
                                    error = "Este email já está cadastrado"
                                elif "Validação falhou" in error_msg:
                                    error = error_msg.replace("Validação falhou: ", "")
                                elif "Erro ao criar aluno" in error_msg:
                                    error = error_msg.replace("Erro ao criar aluno: ", "")
                                else:
                                    error = error_msg
                                print("Erro no registro:", error)
               
                    if link_rect.collidepoint((mx, my)):
                        return None

                if event.type == pygame.KEYDOWN:
                    if active == 1:
                        if event.key == pygame.K_BACKSPACE:
                            nome = nome[:-1]
                        elif event.key == pygame.K_TAB:
                            active = 2
                        else:
                            nome += event.unicode
                    elif active == 2:
                        if event.key == pygame.K_BACKSPACE:
                            email = email[:-1]
                        elif event.key == pygame.K_TAB:
                            active = 3
                        else:
                            email += event.unicode
                    elif active == 3:
                        if event.key == pygame.K_BACKSPACE:
                            senha = senha[:-1]
                        elif event.key == pygame.K_TAB:
                            active = 4
                        else:
                            senha += event.unicode
                    elif active == 4:
                        if event.key == pygame.K_BACKSPACE:
                            matricula = matricula[:-1]
                        elif event.key == pygame.K_TAB:
                            active = 5
                        else:
                            matricula += event.unicode
                    elif active == 5:
                        if event.key == pygame.K_BACKSPACE:
                            id_turma = id_turma[:-1]
                        elif event.key == pygame.K_RETURN:
                            # Enter para submeter
                            if nome and email and senha and matricula and id_turma:
                                pygame.event.post(pygame.event.Event(
                                    pygame.MOUSEBUTTONDOWN, 
                                    {'pos': (500, 490), 'button': 1}
                                ))
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

          
            
            botao_verde = pygame.image.load("src/img/botao/botao_verde.png").convert_alpha()
            botao_registrar = Botao(x=410, y=460, imagem=botao_verde, text="Criar Conta", escala=0.4)
            botao_registrar.draw(self.screen)


            link_font = pygame.font.Font(font_path, 16) if pygame.font else pygame.font.SysFont(None, 16)
            link_text = link_font.render("Já tem uma conta? conecte-se aqui", True, (20, 100, 200))
            link_rect = link_text.get_rect(topleft=(250, 530))
            self.screen.blit(link_text, link_rect)

            if error:
                # Quebrar texto longo em múltiplas linhas
                error_lines = []
                if len(error) > 60:
                    words = error.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 60:
                            current_line += word + " "
                        else:
                            error_lines.append(current_line)
                            current_line = word + " "
                    error_lines.append(current_line)
                else:
                    error_lines = [error]
                
                y_offset = 560
                for line in error_lines:
                    error_surf = font.render(line.strip(), True, (200, 30, 30))
                    self.screen.blit(error_surf, (250, y_offset))
                    y_offset += 25

            pygame.display.flip()
            self.clock.tick(30)

        return None