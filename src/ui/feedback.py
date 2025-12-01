import pygame
import textwrap
from src.componentes.botao import Botao  # novo: usa o botão padrão do jogo

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
    btn_escala = 0.6

    # carrega imagem do botão laranja e calcula largura/posicionamento centralizado
    botao_img = pygame.image.load("src/img/botao/botao_laranja.png").convert_alpha()
    largura_scaled = int(botao_img.get_width() * btn_escala)
    btn_x = w // 2 - largura_scaled // 2
    # coloca o botão abaixo do texto (considera número de linhas já calculadas)
    total_lines = 1 + len(answer_lines) + len(expl_lines)
    btn_y = h // 3 + 10 + total_lines * (body_font.get_linesize() + 6) + 30

    botao_prosseguir = Botao(btn_x, btn_y, botao_img, btn_text, escala=btn_escala)

    # cores
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

        now = pygame.time.get_ticks()
        if timeout > 0 and now - start >= timeout:
            running = False

        # desenha overlay e textos (prefixo, resposta, explicação)
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

        # desenha botão usando a classe padrão e detecta clique
        clicked = botao_prosseguir.draw(screen)
        if clicked:
            running = False

        # dica acessibilidade quando timeout == 0 (mantida)
        if timeout == 0:
            hint = hint_font.render("Clique em PROSSEGUIR para continuar...", True, (200, 200, 200))
            screen.blit(hint, (w // 2 - hint.get_width() // 2, btn_y + 150))

        pygame.display.flip()
        clock.tick(30)
