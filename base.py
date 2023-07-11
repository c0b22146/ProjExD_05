"""

    ProjExD 共同開発
    ・・・

"""
# import module
import sys
import pygame as pg
import random
import numpy as np
from pygame.sprite import AbstractGroup


# class objects
class Field:
    """
        class about field
    """
    # setup variables

    def __init__(self):
        """"""
        rect_s = (1000, 100)
        self.field = pg.Surface(rect_s)
        pg.draw.rect(self.field, "black", (0, 0, *rect_s))
        self.rect = self.field.get_rect()
        self.rect[:-2] = [0, 530]
        return

    def draw(self, screen: pg.Surface) -> None:
        """"""
        screen.blit(self.field, self.rect)
        return

    def get_rect(self) -> pg.Rect:
        """"""
        return self.rect


class Character:
    """
        class about character
    """
    # setup variables
    delta = {}
    chara_size = np.array((20, 20))
    down_speed = np.array((0, 3))
    move_speed = np.array((5, 0))

    def __init__(self):
        """"""
        self.image = pg.Surface(self.chara_size)
        pg.draw.rect(self.image, (127, 127, 127), (0, 0, *self.chara_size))
        self.rect = self.image.get_rect()
        self.rect[:-2] = [10, 500]
        return

    def update(self, fields: list) -> None:
        """"""
        self.rect[:-2] = np.array(self.rect[:-2]) + self.down_speed
        for field in fields:
            if field.get_rect().colliderect(self.rect):
                self.rect[:-2] = np.array(self.rect[:-2]) - self.down_speed
        return

    def move(self, LR: str) -> None:
        """"""
        move: np.array = np.array((0, 0))
        if LR == "L":
            move = self.move_speed * -1
        elif LR == "R":
            move = self.move_speed
        self.rect[:-2] = self.rect[:-2] + move
        return

    def draw(self, screen: pg.Surface) -> None:
        """"""
        screen.blit(self.image, self.rect)
        return
    
class Enemy(pg.sprite.Sprite):
    """
        class about Enemy
    """
    enemy_size = np.array((30, 30))
    enemy_down_speed = np.array((0, 7))
    
    def __init__(self):
        """
            敵Surfaceを生成する
        """
        super().__init__()
        self.image = pg.Surface(self.enemy_size)
        pg.draw.rect(self.image, (255, 0, 0), (0, 0, *self.enemy_size))
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(200,980), 0
        self.enemy_speed = 0
        while -3 <= self.enemy_speed and self.enemy_speed <= 3:
            self.enemy_speed = random.randint(-7,7)
        return
    
    def update(self, fields: list) -> None:
        """
            敵の位置を更新する
        """
        self.rect[:-2] = np.array(self.rect[:-2]) + self.enemy_down_speed
        for field in fields:
            if field.get_rect().colliderect(self.rect):
                self.rect[:-2] = np.array(self.rect[:-2]) - self.enemy_down_speed
                self.rect.move_ip(+self.enemy_speed, 0)
        if self.rect.left < 0 or 1000 < self.rect.right:
            self.enemy_speed *= -1
        return
    
    
    def draw(self, screen: pg.Surface) -> None:
        """
            敵の描画
        """
        screen.blit(self.image, self.rect)
        return


def end(clear: bool) -> None:
    """"""
    print("end")
    return


# main function
def main(screen: pg.Surface) -> bool | None:
    """
        main process
    """
    # setup variables
    clock = pg.time.Clock()

    # setup Surface
    fields: list[Field] = [Field()]
    chara = Character()
    enemy_num = 4
    enemys = pg.sprite.Group()
    enemys.add(Enemy() for _ in range(enemy_num))

    # main loop process
    done = False
    while not done:
        # event process
        key_pressed = pg.key.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()

        for event in pg.event.get():
            # quit process
            if event.type == pg.QUIT:
                return

            # reboot process
            if key_pressed[pg.K_DELETE] and key_pressed[pg.KMOD_CTRL]:
                return True

            # player process
        if key_pressed[pg.K_LEFT]:
            chara.move("L")

        if key_pressed[pg.K_RIGHT]:
            chara.move("R")

        if len(pg.sprite.spritecollide(chara, enemys, True)) != 0:
            end(False)


        # update
        chara.update(fields)
        enemys.update(fields)

        # draw
        screen.fill("white", (0, 0, 1000, 600))
        for field in fields:
            field.draw(screen)
        chara.draw(screen)
        enemys.draw(screen)
        pg.display.update()

        # tike process
        clock.tick(50)
    return


# start and end process
if __name__ == '__main__':
    # setup window variables
    game_name = "Action!!"
    version = "1.1.0"

    win_size = np.array((1000, 600))

    # boot main
    reboot = True
    while reboot:
        # start process
        pg.init()
        pg.display.set_caption(f"{game_name} ver.{version}")
        master = pg.display.set_mode(win_size)

        # main
        reboot = main(master)

        # end process
        if reboot is None:
            reboot = False
        pg.quit()

    sys.exit()
