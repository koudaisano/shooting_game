import pygame
import sys
import random

# --- 定数 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0) # 黒

# --- 背景 ---
background_image = pygame.image.load("C:/Users/PC/shooting_game/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# --- Pygameの初期化 ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("シューティングゲーム")
clock = pygame.time.Clock()


# --- プレイヤー ---
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = (0, 128, 255) # 青
player_x = (SCREEN_WIDTH - PLAYER_WIDTH) / 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
player_speed = 5


# --- 弾 ---
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
BULLET_COLOR = (255, 255, 0) # 黄
bullet_speed = 10
bullets = []


# --- 敵 ---
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_COLOR = (255, 0, 0) # 赤
enemy_speed = 3
enemies = []

# --- スコア ---
score = 0
font = pygame.font.Font(None, 36)


# --- ゲームループ ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + (PLAYER_WIDTH - BULLET_WIDTH) / 2
                bullet_y = player_y
                bullets.append(pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT))

    # --- キー入力の処理 ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # --- 描画 ---
    screen.blit(background_image, (0, 0))

    # --- 弾の移動と描画 ---
    for bullet in bullets:
        bullet.y -= bullet_speed
        pygame.draw.rect(screen, BULLET_COLOR, bullet)

    # --- 画面外に出た弾を削除 ---
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # --- 敵の生成 ---
    if random.randint(1, 100) < 2:
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        enemy_y = 0
        enemies.append(pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT))

    # --- 敵の移動と描画 ---
    for enemy in enemies:
        enemy.y += enemy_speed
        pygame.draw.rect(screen, ENEMY_COLOR, enemy)

    # --- 画面外に出た敵を削除 ---
    enemies = [enemy for enemy in enemies if enemy.y < SCREEN_HEIGHT]

    # --- 当たり判定 ---
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10

    # --- スコアの描画 ---
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    # --- 画面の更新 ---
    pygame.display.flip()

    # --- フレームレートの制御 ---
    clock.tick(60)
