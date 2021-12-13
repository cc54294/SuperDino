import pygame
import random
import sys
from setting import SCREEN_WIDTH, SCREEN_HEIGHT, MAIN_DIR, SCREEN, CLOCK
import os

GAME_SPEED = 20

DINO_JUMP_IMG = pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Dino/DinoJump.png"))
DINO_DEAD_IMG = pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Dino/DinoDead.png"))
DINO_RUN_IMG = [
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Dino/DinoRun1.png")),
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Dino/DinoRun2.png"))
]
DINO_DOWN_IMG = [
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Dino/DinoDuck1.png")),
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Dino/DinoDuck2.png"))
]
GROUND_IMG= pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Other/Track.png"))
CLOUD_IMG = pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Other/Cloud.png"))
TREE_IMG = [
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Coin/LargeCactus1.png")),
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Coin/LargeCactus2.png")),
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Coin/LargeCactus3.png")),
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Coin/SmallCactus1.png")),
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Coin/SmallCactus2.png")),
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Coin/SmallCactus3.png"))
]
BIRD_IMG = [
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Bird/Bird1.png")),
    pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Bird/Bird2.png"))
]
GAME_OVER_IMG = pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Other/GameOver.png"))
RESET_IMG = pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Other/Reset.png"))
JUMP_MUSIC = pygame.mixer.Sound(os.path.join(MAIN_DIR, "Dino/Music/big_jump.ogg"))
MAIN_THEME_MUSIC = os.path.join(MAIN_DIR, "Dino/Music/main_theme.ogg")
DEATH_MUSIC = os.path.join(MAIN_DIR, "Dino/Music/death.wav")

class Ground:
    def __init__(self):
        self.img = GROUND_IMG
        self.x = 0
        self.y = 400
        self.img_width = self.img.get_width()

    def draw(self, is_dead):
        SCREEN.blit(GROUND_IMG, (self.x, self.y))
        SCREEN.blit(GROUND_IMG, (self.x + self.img_width, self.y))
        if not is_dead:
            if self.x <= - self.img_width:
                self.x = 0
            self.x -= GAME_SPEED

class Cloud:
    def __init__(self):
        self.img = CLOUD_IMG
        self.rect = self.img.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(50, 300)

    def draw(self, is_dead):
        SCREEN.blit(self.img, self.rect)
        if not is_dead:
            self.rect.x -= GAME_SPEED * 0.5

class Tree:
    def __init__(self):
        self.img = random.choice(TREE_IMG)
        self.rect = self.img.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = 425 - self.rect.height
        self.mask = pygame.mask.from_surface(self.img.convert_alpha())

    def draw(self, is_dead):
        SCREEN.blit(self.img, self.rect)
        if not is_dead:
            self.rect.x -= GAME_SPEED

class Bird:
    def __init__(self):
        self.img = BIRD_IMG[0]
        self.rect = self.img.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, 400) - self.rect.height
        self.mask = pygame.mask.from_surface(self.img.convert_alpha())
        self.step = 0

    def draw(self, is_dead):
        self.img = BIRD_IMG[self.step // 5]
        rect = self.img.get_rect()
        rect.x = self.rect.x
        rect.y = self.rect.y
        self.rect = rect
        SCREEN.blit(self.img, self.rect)
        if not is_dead:
            self.rect.x -= GAME_SPEED
            self.step = (self.step + 1) % 10

class Dino:
    def __init__(self):
        self.state = 0 # 0 run, 1 down, 2 jumpy, 3 dead
        self.rect = DINO_RUN_IMG[0].get_rect()
        self.rect.x = 88
        self.rect.y = 425 - self.rect.height
        self.mask = pygame.mask.from_surface(DINO_RUN_IMG[0].convert_alpha())
        self.step = 0
        self.jump_speed = 8.5

    def draw(self):
        if self.state == 0:
            img = DINO_RUN_IMG[self.step // 5]
            self.rect = img.get_rect()
            self.mask = pygame.mask.from_surface(img.convert_alpha())
            self.rect.x = 80
            self.rect.y = 425 - self.rect.height
        elif self.state == 1:
            img = DINO_DOWN_IMG[self.step // 5]
            self.rect = img.get_rect()
            self.mask = pygame.mask.from_surface(img.convert_alpha())
            self.rect.x = 80
            self.rect.y = 425 - self.rect.height
        elif self.state == 2:
            img = DINO_JUMP_IMG
            rect = img.get_rect()
            rect.x = 80
            rect.y = self.rect.y - (self.jump_speed * 4)
            self.jump_speed -= 0.8
            if self.jump_speed < -8.5:
                self.jump_speed = 8.5
                self.state = 0
                rect.y = 425 - DINO_RUN_IMG[0].get_height()
                self.mask = pygame.mask.from_surface(DINO_RUN_IMG[0].convert_alpha())
            else:
                self.mask = pygame.mask.from_surface(img.convert_alpha())
            self.rect = rect
        else:
            img = DINO_DEAD_IMG
            rect = img.get_rect()
            rect.x = self.rect.x
            rect.y = min(425 - img.get_height() + 10, self.rect.y)
            self.rect = rect
        SCREEN.blit(img, self.rect)

    def update(self, keys):
        if self.state != 3:
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                if self.state != 2:
                    JUMP_MUSIC.play()
                self.state = 2
            elif keys[pygame.K_DOWN] and self.state != 2:
                self.state = 1
            elif self.state != 2 and not keys[pygame.K_DOWN]:
                self.state = 0
        self.step = (self.step + 1) % 10

class Restart:
    def __init__(self):
        self.game_over_img = GAME_OVER_IMG
        self.reset_img = RESET_IMG
        self.game_over_pos = (
            SCREEN_WIDTH//2-self.game_over_img.get_width()//2,
            SCREEN_HEIGHT//4
        )
        self.reset_pos = (
            SCREEN_WIDTH//2-self.reset_img.get_width()//2,
            SCREEN_HEIGHT//3
        )

    def draw(self, is_dead):
        if is_dead:
            SCREEN.blit(self.game_over_img, self.game_over_pos)
            SCREEN.blit(self.reset_img, self.reset_pos)

class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("SimHei", 20)

    def draw(self, is_dead):
        if not is_dead:
            self.score += 1
            if self.score % 100 == 0:
                global GAME_SPEED
                GAME_SPEED = min(35, GAME_SPEED+1)

        score_str = str(self.score)
        score_str = "0"*max(5-len(score_str), 0) + score_str
        if (self.score // 1000) % 2 == 0:
            text = self.font.render(score_str, True, (0, 0, 0))
        else:
            text = self.font.render(score_str, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.x = SCREEN_WIDTH - text_rect.width - 50
        text_rect.y = 50
        SCREEN.blit(text, text_rect)

class DinoMain:
    def __init__(self):
        self.ground = Ground()
        self.cloud_list = []
        self.tree_and_bird_list = []
        self.dino = Dino()
        self.restart = Restart()
        self.score = Score()
        self.start = True
        self.play_music = 0 # 0 None, 1 Main, 2 Death

    def draw(self):
        if (self.score.score // 1000) % 2 == 0:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0))

        self.ground.draw(self.dino.state==3)
        for cloud in self.cloud_list:
            cloud.draw(self.dino.state==3)
        for obj in self.tree_and_bird_list:
            obj.draw(self.dino.state==3)
        self.dino.draw()
        self.score.draw(self.dino.state==3)
        self.restart.draw(self.dino.state==3)

    def main_loop(self):
        global GAME_SPEED

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return

                if self.dino.state == 3 and event.type == pygame.KEYDOWN:
                    self.ground = Ground()
                    self.cloud_list = []
                    self.tree_and_bird_list = []
                    self.dino = Dino()
                    self.restart = Restart()
                    self.score = Score()
                    self.start = True
                    GAME_SPEED = 20
                    pygame.time.delay(300)

            if self.dino.state != 3 and self.play_music != 1:
                self.play_music = 1
                pygame.mixer.music.load(MAIN_THEME_MUSIC)
                pygame.mixer.music.play()
            elif self.dino.state == 3 and self.play_music != 2:
                self.play_music = 2
                pygame.mixer.music.load(DEATH_MUSIC)
                pygame.mixer.music.play()

            if self.start:
                self.start = False
                continue
            else:
                keys = pygame.key.get_pressed()
                self.dino.update(keys)

            new_cloud_list = []
            for cloud in self.cloud_list:
                if cloud.rect.x >= -cloud.rect.width:
                    new_cloud_list.append(cloud)
                else:
                    del cloud
            self.cloud_list = new_cloud_list
            if not len(self.cloud_list) or self.cloud_list[-1].rect.x <= (SCREEN_WIDTH * 3 // 4):
                if random.random() > 0.8:
                    self.cloud_list.append(Cloud())

            new_tree_and_bird_list = []
            for obj in self.tree_and_bird_list:
                if obj.rect.x >= -obj.rect.width:
                    new_tree_and_bird_list.append(obj)
                else:
                    del obj
            self.tree_and_bird_list = new_tree_and_bird_list
            if not len(self.tree_and_bird_list) or self.tree_and_bird_list[-1].rect.x <= (SCREEN_WIDTH // 3):
                if random.random() > 0.8:
                    if random.random() > 0.7:
                        self.tree_and_bird_list.append(Bird())
                    else:
                        self.tree_and_bird_list.append(Tree())

            for obj in self.tree_and_bird_list:
                offset = (self.dino.rect.x - obj.rect.x, self.dino.rect.y - obj.rect.y)
                if obj.mask.overlap(self.dino.mask, offset):
                    self.dino.state = 3

            self.draw()
            CLOCK.tick(30)
            pygame.display.update()
