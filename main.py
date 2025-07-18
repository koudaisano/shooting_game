import pygame
import sys
import random

# --- 定数 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- Pygameの初期化 ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("シューティングゲーム")
clock = pygame.time.Clock()

# --- 画像の読み込み (エラー処理付き) ---
try:
    player_img = pygame.image.load("C:/Users/PC/shooting_game/player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (50, 50))
except pygame.error:
    print("Warning: player.png not found or failed to load. Using a solid color.")
    player_img = None

try:
    enemy_img = pygame.image.load("C:/Users/PC/shooting_game/enemy.png").convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (50, 50))
except pygame.error:
    print("Warning: enemy.png not found or failed to load. Using a solid color.")
    enemy_img = None

try:
    background_image = pygame.image.load("C:/Users/PC/shooting_game/background.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    print("Warning: background.jpg not found or failed to load. Using a solid color.")
    background_image = None

# --- 色 ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 128, 255) # 青 (フォールバック用)
ENEMY_COLOR = (255, 0, 0) # 赤 (フォールバック用)
BULLET_COLOR = (255, 255, 0) # 黄
ENEMY_BULLET_COLOR = (255, 100, 100) # 赤みがかった白
BUTTON_COLOR = (0, 200, 0)
BUTTON_TEXT_COLOR = WHITE

# --- フォント ---
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# --- ゲームオブジェクトの初期値を設定する関数 ---
def reset_game():
    global player_rect, bullets, enemies, enemy_bullets, score, start_time, game_state
    player_rect = pygame.Rect((SCREEN_WIDTH - 50) / 2, SCREEN_HEIGHT - 60, 50, 50)
    bullets = []
    enemies = []
    enemy_bullets = []
    score = 0
    start_time = pygame.time.get_ticks()
    game_state = "playing"

# --- ボタンを描画する関数 ---
def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)

# --- グローバル変数の初期化 ---
player_rect = None
bullets = None
enemies = None
enemy_bullets = None
score = None
start_time = None
game_state = "start" # 初期状態はスタート画面

# --- ゲームループ ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "start":
                if play_button.collidepoint(event.pos):
                    reset_game()
            elif game_state == "game_over":
                if retry_button.collidepoint(event.pos):
                    reset_game()
            elif game_state == "clear":
                if retry_button.collidepoint(event.pos):
                    reset_game()

        if game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_x = player_rect.x + (player_rect.width - 5) / 2
                    bullet_y = player_rect.y
                    bullets.append(pygame.Rect(bullet_x, bullet_y, 5, 15))

    # --- ゲームの状態に応じた処理 ---
    if game_state == "start":
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)
        title_text = big_font.render("Earth Defense Force", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH/2 - title_text.get_width()/2, SCREEN_HEIGHT/3))
        play_button = draw_button("Play", SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT/2, 150, 50, BUTTON_COLOR, BUTTON_TEXT_COLOR)

    elif game_state == "playing":
        # --- 時間制限 ---
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = 60 - elapsed_time
        if remaining_time <= 0:
            game_state = "clear" # ゲームクリア！

        # --- キー入力 ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += 5
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= 5
        if keys[pygame.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
            player_rect.y += 5

        # --- 敵の生成と移動 ---
        min_enemies = 5 if remaining_time <= 10 else 3
        while len(enemies) < min_enemies:
            enemy_rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), 0, 50, 50)
            enemies.append({'rect': enemy_rect, 'speed_x': random.choice([-2, 2]), 'speed_y': 2})
        
        for enemy in enemies:
            enemy['rect'].x += enemy['speed_x']
            enemy['rect'].y += enemy['speed_y']
            if enemy['rect'].left < 0 or enemy['rect'].right > SCREEN_WIDTH:
                enemy['speed_x'] *= -1
            if random.randint(1, 200) < 2:
                enemy_bullets.append(pygame.Rect(enemy['rect'].x + 22, enemy['rect'].y + 50, 5, 15))

        # --- 弾の移動 ---
        for bullet in bullets:
            bullet.y -= 10
        for eb in enemy_bullets:
            eb.y += 5

        # --- オブジェクトの削除 ---
        bullets = [b for b in bullets if b.bottom > 0]
        enemies = [e for e in enemies if e['rect'].top < SCREEN_HEIGHT]
        enemy_bullets = [eb for eb in enemy_bullets if eb.top < SCREEN_HEIGHT]

        # --- 当たり判定 ---
        for bullet in list(bullets):
            for enemy in list(enemies):
                if bullet.colliderect(enemy['rect']):
                    if bullet in bullets: bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
        for enemy in enemies:
            if player_rect.colliderect(enemy['rect']):
                game_state = "game_over"
        for eb in enemy_bullets:
            if player_rect.colliderect(eb):
                game_state = "game_over"

        # --- 描画 ---
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)
        if player_img:
            screen.blit(player_img, player_rect)
        else:
            pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        for bullet in bullets:
            pygame.draw.rect(screen, BULLET_COLOR, bullet)
        for enemy in enemies:
            if enemy_img:
                screen.blit(enemy_img, enemy['rect'])
            else:
                pygame.draw.rect(screen, ENEMY_COLOR, enemy['rect'])
        for eb in enemy_bullets:
            pygame.draw.rect(screen, ENEMY_BULLET_COLOR, eb)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        time_text = font.render(f"Time: {int(remaining_time)}", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 150, 10))

    elif game_state == "game_over":
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)
        game_over_text = big_font.render("GAME OVER", True, WHITE)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH/2 - game_over_text.get_width()/2, SCREEN_HEIGHT/3))
        screen.blit(final_score_text, (SCREEN_WIDTH/2 - final_score_text.get_width()/2, SCREEN_HEIGHT/2))
        retry_button = draw_button("Retry", SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT/2 + 70, 150, 50, BUTTON_COLOR, BUTTON_TEXT_COLOR)

    elif game_state == "clear":
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)
        clear_text = big_font.render("CLEAR!", True, WHITE)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(clear_text, (SCREEN_WIDTH/2 - clear_text.get_width()/2, SCREEN_HEIGHT/3))
        screen.blit(final_score_text, (SCREEN_WIDTH/2 - final_score_text.get_width()/2, SCREEN_HEIGHT/2))
        retry_button = draw_button("Retry", SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT/2 + 70, 150, 50, BUTTON_COLOR, BUTTON_TEXT_COLOR)

    pygame.display.flip()
    clock.tick(60)
