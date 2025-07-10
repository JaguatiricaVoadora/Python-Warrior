import pygame
import sys

pygame.init()

# Tela do jogo
BG_IMG = pygame.image.load('Sprites/Background.png')
WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()
SCALE = 1.2  # Fator de escala
SCREEN_WIDTH, SCREEN_HEIGHT = int(WIDTH * SCALE), int(HEIGHT * SCALE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Teste de Jogo¹")

# Superfície para renderização do jogo (tamanho original)
game_surface = pygame.Surface((WIDTH, HEIGHT))

# Relógio
clock = pygame.time.Clock()
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLUE = (50, 50, 225)

# Jogador
player = pygame.Rect(100, 540, 100, 140)
player_vel_y = 0
GRAVITY = 1
JUMP_STRENGTH = -15
on_ground = False

# Carregar frames de corrida e idle
import os
run_frames = []
run_frames_dir = os.path.join('Sprites', 'Run_frames')
for i in range(10):
    frame_path = os.path.join(run_frames_dir, f'frame_{i:03}.png')
    frame = pygame.image.load(frame_path).convert_alpha()
    frame = pygame.transform.scale(frame, (180, 200))
    run_frames.append(frame)

idle_frames = []
idle_frames_dir = os.path.join('Sprites', 'Idle_frames')
for i in range(10):
    frame_path = os.path.join(idle_frames_dir, f'frame_{i:03}.png')
    frame = pygame.image.load(frame_path).convert_alpha()
    frame = pygame.transform.scale(frame, (180, 200))
    idle_frames.append(frame)

jump_frames = []
jump_frames_dir = os.path.join('Sprites', 'Jump_frames')
for i in range(3):
    frame_path = os.path.join(jump_frames_dir, f'frame_{i:03}.png')
    frame = pygame.image.load(frame_path).convert_alpha()
    frame = pygame.transform.scale(frame, (180, 200))
    jump_frames.append(frame)

fall_frames = []
fall_frames_dir = os.path.join('Sprites', 'Fall_frames')
for i in range(3):
    frame_path = os.path.join(fall_frames_dir, f'frame_{i:03}.png')
    frame = pygame.image.load(frame_path).convert_alpha()
    frame = pygame.transform.scale(frame, (180, 200))
    fall_frames.append(frame)

run_frame_index = 0
run_anim_speed = 0.25
run_anim_counter = 0
idle_frame_index = 0
idle_anim_speed = 0.10
idle_anim_counter = 0
jump_frame_index = 0
jump_anim_speed = 0.10
jump_anim_counter = 0
fall_frame_index = 0
fall_anim_speed = 0.10
fall_anim_counter = 0
last_move_direction = 1

# Painel DEV
import pygame.freetype
dev_panel_open = False
show_hitboxes = False

# Chão
import json
with open('ground_rects.json') as f:
    ground_rects_data = json.load(f)
ground_rects = [pygame.Rect(r['x'], r['y'], r['w'], r['h']) for r in ground_rects_data]

# Loop do jogo
while True:
    # ======== CÂMERA ========
    camera_x = player.x - WIDTH // 2

    # Desenhar fundo
    game_surface.fill((0, 0, 0))  # Limpar a superfície do jogo
    min_bg = (player.x - WIDTH) // WIDTH
    max_bg = (player.x + WIDTH // 2) // WIDTH + 2
    for i in range(min_bg, max_bg):
        bg_x = i * WIDTH - camera_x
        game_surface.blit(BG_IMG, (bg_x, 0))

    # Fechar jogo e painel DEV
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                dev_panel_open = not dev_panel_open
            if dev_panel_open and event.key == pygame.K_h:
                show_hitboxes = not show_hitboxes

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT]:
        player.x -= 5
        moving = True
        last_move_direction = -1
    if keys[pygame.K_RIGHT]:
        player.x += 5
        moving = True
        last_move_direction = 1
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = JUMP_STRENGTH

    # Atualizar animação
    if not on_ground:
        if player_vel_y > 0:
            fall_anim_counter += fall_anim_speed
            if fall_anim_counter >= 1:
                fall_frame_index = (fall_frame_index + 1) % len(fall_frames)
                fall_anim_counter = 0
        else:
            jump_anim_counter += jump_anim_speed
            if jump_anim_counter >= 1:
                jump_frame_index = (jump_frame_index + 1) % len(jump_frames)
                jump_anim_counter = 0
    elif moving:
        run_anim_counter += run_anim_speed
        if run_anim_counter >= 1:
            run_frame_index = (run_frame_index + 1) % len(run_frames)
            run_anim_counter = 0
    else:
        idle_anim_counter += idle_anim_speed
        if idle_anim_counter >= 1:
            idle_frame_index = (idle_frame_index + 1) % len(idle_frames)
            idle_anim_counter = 0

    # Aplicar gravidade
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # Colisão com o chão infinito
    on_ground = False
    player_x_mod = player.x % WIDTH
    offset_base = player.x - player_x_mod
    for rect in ground_rects:
        test_rect = rect.move(offset_base, 0)
        if player.colliderect(test_rect):
            player.bottom = test_rect.top
            player_vel_y = 0
            on_ground = True
            break

    # ======== DESENHO COM OFFSET DA CÂMERA ========
    player_draw_pos = player.move(-camera_x, 0)
    # Desenhar o frame correto
    if not on_ground:
        if player_vel_y > 0:
            frame = fall_frames[fall_frame_index]
        else:
            frame = jump_frames[jump_frame_index]
    elif moving:
        frame = run_frames[run_frame_index]
    else:
        frame = idle_frames[idle_frame_index]
    frame_flipped = pygame.transform.flip(frame, last_move_direction == -1, False)
    sprite_x = player_draw_pos.x
    sprite_y = player_draw_pos.y + player_draw_pos.height - frame_flipped.get_height()
    game_surface.blit(frame_flipped, (sprite_x, sprite_y))

    # Painel DEV
    if dev_panel_open:
        panel_rect = pygame.Rect(30, 30, 250, 80)
        pygame.draw.rect(game_surface, (30, 30, 30), panel_rect)
        pygame.draw.rect(game_surface, (200, 200, 0), panel_rect, 2)
        font = pygame.freetype.SysFont(None, 22)
        font.render_to(game_surface, (45, 45), 'Painel DEV', (255,255,0))
        font.render_to(game_surface, (45, 70), f'[H] Mostrar Hitboxes: {"ON" if show_hitboxes else "OFF"}', (180,255,180) if show_hitboxes else (255,180,180))

    # Mostrar hitboxes
    if show_hitboxes:
        # Player (centralizar hitbox no sprite)
        hitbox_offset_x = (frame_flipped.get_width() - player.width) // 2
        hitbox_rect = player_draw_pos.move(hitbox_offset_x, 0)
        pygame.draw.rect(game_surface, (255,0,0), hitbox_rect, 2)
        # Chão
        for rect in ground_rects:
            test_rect = rect.move(offset_base, 0)
            draw_rect = test_rect.move(-camera_x, 0)
            pygame.draw.rect(game_surface, (0,255,0), draw_rect, 2)
    
    # Redimensionar a superfície do jogo para a tela
    scaled_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_surface, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)
