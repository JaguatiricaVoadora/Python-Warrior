# MapTools

Ferramenta para Seleção de Colisões do Chão em Jogos Pygame

## O que é

Esta pasta contém o script `map_ground_selector.py`, que permite selecionar visualmente as áreas de chão (colisão) de um mapa a partir de uma imagem de fundo (ex: `Background.png`). O resultado é um arquivo `ground_rects.json` com os retângulos das áreas sólidas, pronto para ser usado no seu jogo.

## Como usar

1. Coloque sua imagem de fundo (ex: `Background.png`) na pasta `Sprites`.
2. Execute o script `map_ground_selector.py`:

   ```bash
   python MapTools/map_ground_selector.py
   ```

3. Clique e arraste com o mouse para selecionar cada área de chão/plataforma.
4. Pressione `S` para salvar as seleções em `ground_rects.json`.
5. Pressione `C` para limpar todas as seleções (caso queira refazer).
6. Feche a janela para sair.
7. O arquivo `ground_rects.json` será criado na raiz do projeto.

## Como usar o arquivo de colisão (`ground_rects.json`) em seu projeto Pygame

Depois de gerar o arquivo `ground_rects.json` usando este script, você pode utilizá-lo em qualquer projeto Pygame para definir as áreas de colisão do chão. Veja um exemplo básico de como carregar e usar essas colisões em um loop mínimo:

```python
import pygame
import json

pygame.init()
BG_IMG = pygame.image.load('Sprites/Background.png')
WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

with open('ground_rects.json') as f:
    ground_rects_data = json.load(f)
ground_rects = [pygame.Rect(r['x'], r['y'], r['w'], r['h']) for r in ground_rects_data]

player = pygame.Rect(100, 500, 40, 50)
player_vel_y = 0
GRAVITY = 0.8

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # Colisão infinita com o chão
    player_x_mod = player.x % WIDTH
    offset_base = player.x - player_x_mod
    for rect in ground_rects:
        test_rect = rect.move(offset_base, 0)
        if player.colliderect(test_rect):
            player.bottom = test_rect.top
            player_vel_y = 0
            break

    # Fundo infinito
    camera_x = player.x - WIDTH // 2
    min_bg = (player.x - WIDTH // 2) // WIDTH - 1
    max_bg = (player.x + WIDTH // 2) // WIDTH + 2
    for i in range(min_bg, max_bg):
        bg_x = i * WIDTH - camera_x
        screen.blit(BG_IMG, (bg_x, 0))
    pygame.draw.rect(screen, (0, 0, 255), player.move(-camera_x, 0))
    pygame.display.flip()
```

## Como fazer o fundo e o chão infinitos

Para deixar o fundo e o chão infinitos na horizontal:
- Desenhe a imagem de fundo repetidamente, lado a lado, conforme a posição da câmera ou do jogador.
- Repita o teste de colisão dos retângulos do arquivo `ground_rects.json` para cada "tile" da largura da imagem, usando o deslocamento correto (como no exemplo acima).

## Como remover as outlines verdes (opcional)

Durante a seleção das áreas, o script mostra outlines verdes para ajudar na visualização. Isso não afeta o seu jogo final. Caso queira remover as outlines do seletor, basta comentar ou remover a linha:
```python
pygame.draw.rect(screen, (0,255,0), r, 2)
```
No seu jogo, só verá outlines se você mesmo desenhar retângulos de colisão para debug.

---

Qualquer dúvida ou sugestão, fique à vontade para modificar ou pedir melhorias!

---

