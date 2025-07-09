import pygame
import json
import os

# Caminho da imagem de fundo
BG_PATH = os.path.join('..', 'Sprites', 'Background.png')

pygame.init()
bg_img = pygame.image.load(BG_PATH)
screen = pygame.display.set_mode(bg_img.get_size())
pygame.display.set_caption('Selecione as áreas do chão - Clique e arraste')

selecting = False
start_pos = None
current_rect = None
ground_rects = []

font = pygame.font.SysFont(None, 24)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selecting = True
                start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and selecting:
                selecting = False
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))
                if rect.width > 5 and rect.height > 5:
                    ground_rects.append(rect)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # Salva os retângulos em um arquivo JSON
                data = [dict(x=r.x, y=r.y, w=r.width, h=r.height) for r in ground_rects]
                with open('../ground_rects.json', 'w') as f:
                    json.dump(data, f, indent=2)
                print('Retângulos salvos em ../ground_rects.json')
            elif event.key == pygame.K_c:
                # Limpa as seleções
                ground_rects.clear()
                print('Seleções limpas.')

    screen.blit(bg_img, (0, 0))

    # Desenha os retângulos já selecionados
    for r in ground_rects:
        pygame.draw.rect(screen, (0,255,0), r, 2)

    # Desenha o retângulo atual
    if selecting and start_pos:
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = start_pos
        x2, y2 = mouse_pos
        temp_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(screen, (255,0,0), temp_rect, 2)

    # Instruções
    instr1 = font.render('Clique e arraste para marcar o chão. S = salvar, C = limpar, Fechar = sair.', True, (0,0,0))
    screen.blit(instr1, (10, 10))
    instr2 = font.render(f'Total de retângulos: {len(ground_rects)}', True, (0,0,0))
    screen.blit(instr2, (10, 35))

    pygame.display.flip()
