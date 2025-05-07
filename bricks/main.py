import pygame
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("打砖块")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, 24)
        self.current_level = 0
        self.lives = LIVES
        self.score = 0
        self.reset_game()

    def reset_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.active_powerups = {}
        self.load_level()

    def load_level(self):
        self.paddle = Paddle()
        level_config = LEVELS[self.current_level]
        self.ball = Ball(level_config["speed_multiplier"])
        self.all_sprites.add(self.paddle, self.ball)
        
        # 生成砖块
        layout = level_config["layout"]
        start_y = 100
        for row_idx, row in enumerate(layout):
            for col_idx, char in enumerate(row):
                x = 50 + col_idx * (BRICK_WIDTH + BRICK_GAP)
                y = start_y + row_idx * (BRICK_HEIGHT + BRICK_GAP)
                brick = Brick(x, y, char)
                if brick.color_char != " ":
                    self.bricks.add(brick)
                    self.all_sprites.add(brick)

    def show_text(self, text, y, color=(255,255,255)):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y))
        self.screen.blit(text_surface, text_rect)

    def start_screen(self):
        waiting = True
        while waiting:
            self.screen.fill(BG_COLOR)
            self.show_text("Press the spacebar to start", SCREEN_HEIGHT//2)
            self.show_text(f"Level {self.current_level+1} ", SCREEN_HEIGHT//2 - 50)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
        return True

    def game_over(self, win=False):
        self.screen.fill(BG_COLOR)
        if win:
            self.show_text("Cleared successfully！", SCREEN_HEIGHT//2 - 50, (0,255,0))
        else:
            self.show_text("Game over", SCREEN_HEIGHT//2 - 50, (255,0,0))
        self.show_text("Press the SPACEBAR to replay", SCREEN_HEIGHT//2 + 50)
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.current_level = 0
                    self.lives = LIVES
                    self.score = 0
                    return True

    def draw_powerup_timers(self):
        y_offset = 120
        for effect, end_time in self.active_powerups.items():
            remaining = max(0, (end_time - pygame.time.get_ticks()) // 1000)
            text = f"{effect}: {remaining}s"
            text_surf = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surf, (SCREEN_WIDTH - 150, y_offset))
            y_offset += 30

    def run(self):
        running = True
        while running:
            if not self.start_screen():
                break
            
            level_complete = False
            while running and not level_complete:
                # 事件处理
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False
                
                # 更新所有精灵
                self.all_sprites.update()
                
                # 球与挡板碰撞
                if pygame.sprite.collide_rect(self.ball, self.paddle):
                    if self.ball.speed_y > 0:  # 仅在下落时处理
                       self.ball.rect.bottom = self.paddle.rect.top
                    offset = (self.ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
                    self.ball.speed_x = offset * self.ball.base_speed * 2  # 基于基础速度计算
                    self.ball.speed_y *= -1
                
                # 球与砖块碰撞
                brick_hit = pygame.sprite.spritecollideany(self.ball, self.bricks)
                if brick_hit:
                    brick_hit.kill()
                    self.ball.speed_y *= -1
                    self.score += 10
                    
                    # 生成道具
                    if random.random() < POWERUP_CHANCE:
                        powerup = PowerUp(brick_hit.rect.centerx, brick_hit.rect.centery)
                        self.powerups.add(powerup)
                        self.all_sprites.add(powerup)
                
                # 道具碰撞处理
                for powerup in pygame.sprite.spritecollide(self.paddle, self.powerups, True):
                    if powerup.type == "life":
                        self.lives = min(self.lives + 1, LIVES)
                    elif powerup.type == "expand":
                        self.paddle.image = pygame.Surface((int(PADDLE_WIDTH*1.5), PADDLE_HEIGHT))
                        self.paddle.image.fill(PADDLE_COLOR)
                        self.active_powerups["expand"] = pygame.time.get_ticks() + 10000
                    elif powerup.type == "shrink":
                        self.paddle.image = pygame.Surface((int(PADDLE_WIDTH*0.5), PADDLE_HEIGHT))
                        self.paddle.image.fill(PADDLE_COLOR)
                        self.active_powerups["shrink"] = pygame.time.get_ticks() + 10000
                    elif powerup.type == "speed":
                        self.ball.speed_x = self.ball.base_speed * 1.5
                        self.ball.speed_y = -self.ball.base_speed * 1.5
                        self.active_powerups["speed"] = pygame.time.get_ticks() + 8000
                    elif powerup.type == "slow":
                        self.ball.speed_x = self.ball.base_speed * 0.5
                        self.ball.speed_y = -self.ball.base_speed * 0.5 
                        self.active_powerups["slow"] = pygame.time.get_ticks() + 8000
                
                # 道具倒计时检测
                current_time = pygame.time.get_ticks()
                for effect in list(self.active_powerups.keys()):
                    if current_time > self.active_powerups[effect]:
                        if effect == "expand":
                            self.paddle.reset_size()
                        elif effect == "speed":
                            self.ball.reset_speed()
                        elif effect == "slow":
                            self.ball.reset_speed()
                        elif effect == "shrink":
                            self.paddle.reset_size()
                        del self.active_powerups[effect]
                   
                # 失败检测
                if self.ball.rect.bottom >= SCREEN_HEIGHT:
                    self.lives -= 1
                    if self.lives <= 0:
                        running = self.game_over(win=False)
                        break
                    else:
                        self.reset_game()
                        self.start_screen()
                
                # 过关检测
                if len(self.bricks) == 0:
                    self.current_level += 1
                    if self.current_level >= len(LEVELS):
                        running = self.game_over(win=True)
                    else:
                        level_complete = True
                        self.reset_game()
                
                # 渲染
                self.screen.fill(BG_COLOR)
                self.all_sprites.draw(self.screen)
                self.draw_powerup_timers()
                
                # UI显示
                self.show_text(f"scores: {self.score}", 30)
                self.show_text(f"lives: {self.lives}", 60)
                self.show_text(f"level: {self.current_level + 1}/{len(LEVELS)}", 90)
                
                pygame.display.flip()
                self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()