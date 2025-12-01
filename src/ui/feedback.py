import pygame
import textwrap

def show_incorrect_feedback(screen, correct_answer_text, explanation=None, timeout=3000):
    """
    Exibe overlay com a resposta correta e explicação.
    - screen: superfície Pygame
    - correct_answer_text: texto a mostrar como resposta correta
    - explanation: texto opcional
    - timeout: milissegundos; se 0 aguarda clique no botão ou tecla para fechar
    """
    pygame.font.init()
    clock = pygame.time.Clock()
    w, h = screen.get_size()

    overlay = pygame.Surface((w, h), flags=pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) 

    title_font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 48) if pygame.font.get_init() else pygame.font.SysFont(None, 48)
    body_font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 26) if pygame.font.get_init() else pygame.font.SysFont(None, 26)
    hint_font = pygame.font.SysFont(None, 20)
    btn_font = pygame.font.Font("src/fonts/Grand9K Pixel.ttf", 22) if pygame.font.get_init() else pygame.font.SysFont(None, 22)

  
    answer_lines = textwrap.wrap(str(correct_answer_text), width=60) if correct_answer_text is not None else []
    expl_lines = textwrap.wrap(explanation, width=60) if explanation else []

    btn_text = "PROSSEGUIR"
    btn_padding_x, btn_padding_y = 20, 10
    btn_surf = btn_font.render(btn_text, True, (255, 255, 255))
    btn_w = btn_surf.get_width() + btn_padding_x * 2
    btn_h = btn_surf.get_height() + btn_padding_y * 2
    btn_x = w // 2 - btn_w // 2
    total_lines = 1 + len(answer_lines) + len(expl_lines)
    btn_y = h // 3 + 10 + total_lines * (body_font.get_linesize() + 6) + 30
    btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

    blue_color = (30, 144, 255)
    white_color = (240, 240, 240)

    start = pygame.time.get_ticks()
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if ev.type == pygame.KEYDOWN:
                running = False
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                if btn_rect.collidepoint(mx, my):
                    running = False

        now = pygame.time.get_ticks()
        if timeout > 0 and now - start >= timeout:
            running = False

        # desenha overlay
        screen.blit(overlay, (0, 0))

        title_surf = title_font.render("Você errou", True, (255, 200, 50))
        screen.blit(title_surf, (w // 2 - title_surf.get_width() // 2, h // 3 - 60))

        y = h // 3 + 10

        prefix = "Resposta correta:"
        prefix_surf = body_font.render(prefix, True, white_color)
        screen.blit(prefix_surf, (w // 2 - prefix_surf.get_width() // 2, y))
        y += body_font.get_linesize() + 6

        for line in answer_lines:
            surf = body_font.render(line, True, blue_color)
            screen.blit(surf, (w // 2 - surf.get_width() // 2, y))
            y += body_font.get_linesize() + 6

        for line in expl_lines:
            surf = body_font.render(line, True, white_color)
            screen.blit(surf, (w // 2 - surf.get_width() // 2, y))
            y += body_font.get_linesize() + 6

        # desenha botão
        mouse_pos = pygame.mouse.get_pos()
        hovered = btn_rect.collidepoint(mouse_pos)
        btn_color = (255, 140, 0) if hovered else (200, 100, 0)
        pygame.draw.rect(screen, btn_color, btn_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), btn_rect, 2, border_radius=6)
        screen.blit(btn_surf, (btn_rect.x + btn_padding_x, btn_rect.y + btn_padding_y))

        if timeout == 0:
            hint = hint_font.render("Clique em PROSSEGUIR para continuar...", True, (200, 200, 200))
            screen.blit(hint, (w // 2 - hint.get_width() // 2, btn_rect.y + btn_h + 12))

        pygame.display.flip()
        clock.tick(30)
