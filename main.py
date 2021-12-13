import pygame
import sys
import os
from setting import SCREEN_HEIGHT, SCREEN_WIDTH, MAIN_DIR, SCREEN, CLOCK
from Dino.DinoMain import DinoMain
from DinoShoot.DinoShootMain import DinoShootMain

pygame.display.set_caption("SuperDino")
DINO_JUMP_IMG = pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Dino/DinoJump.png"))
DINO_JUMP_SMALL_IMG = pygame.transform.scale(DINO_JUMP_IMG, (DINO_JUMP_IMG.get_width()//3, DINO_JUMP_IMG.get_height()//3))
GROUND_IMG= pygame.image.load(os.path.join(MAIN_DIR, "Dino/Image/Other/Track.png"))

GAME_ITEMS = ["小恐龙快跑", "小恐龙射击"]

class Menu:
    def __init__(self):
        self.start = 0
        self.start_finish = 0

        self.font = pygame.font.SysFont("SimHei", 30)
        self.text = self.font.render("按回车键开始游戏", True, (0, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        self.dino_rect = DINO_JUMP_IMG.get_rect()
        self.dino_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
        self.jump_speed = 8.5

        self.font_item = pygame.font.SysFont("microsoftyahei", 25)
        self.game_texts = [self.font_item.render(t, True, (0, 0, 0)) for t in GAME_ITEMS]
        self.game_text_rects = [t.get_rect() for t in self.game_texts]
        for i in range(len(self.game_text_rects)):
            self.game_text_rects[i].x = SCREEN_WIDTH // 2
            self.game_text_rects[i].y = SCREEN_HEIGHT // 2 + i * 50 - 15

        self.selected = 1
        self.dino_item_rect = DINO_JUMP_SMALL_IMG.get_rect()
        self.update_dino_item_rect()

    def draw(self):
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(self.text, self.text_rect)
        for i in range(len(self.game_texts)):
            SCREEN.blit(self.game_texts[i], self.game_text_rects[i])
        SCREEN.blit(GROUND_IMG, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 180), (0, 0, 120, 70))
        SCREEN.blit(DINO_JUMP_SMALL_IMG, self.dino_item_rect)

        if self.start != 0:
            self.dino_rect.centery -= self.jump_speed * 2
            self.jump_speed -= 0.8
            if self.jump_speed < -8.5:
                self.jump_speed = 8.5
                self.start = 0
                self.start_finish = 1
                self.dino_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
        SCREEN.blit(DINO_JUMP_IMG, self.dino_rect)

    def menu_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        self.start = 1
                    elif event.key == pygame.K_DOWN and not self.start:
                        self.selected = 1 if self.selected == 2 else 2
                        self.update_dino_item_rect()
                    elif event.key == pygame.K_UP and not self.start:
                        self.selected = 2 if self.selected == 1 else 1
                        self.update_dino_item_rect()

            if self.start_finish:
                self.start = 0
                self.start_finish = 0
                if self.selected == 1:
                    main = DinoMain()
                else:
                    main = DinoShootMain()
                main.main_loop()

            self.draw()
            CLOCK.tick(30)
            pygame.display.update()

    def update_dino_item_rect(self):
        self.dino_item_rect.center = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50 * (self.selected-1))

if __name__ == "__main__":
    menu = Menu()
    menu.menu_loop()

# pyinstaller -F -w -i SuperDino.ico main.py