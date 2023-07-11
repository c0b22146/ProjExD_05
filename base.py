"""

    ProjExD 共同開発
    ・・・

"""
# import module
import sys
import pygame as pg
import random
import numpy as np


# class objects
class Field:
    """
        class about field
    """
    # setup variables

    def __init__(self, field_rect: tuple[int, int, int, int] = (0, 530, 1000, 100)):
        """"""
        self.field = pg.Surface(field_rect[2:])
        pg.draw.rect(self.field, "black", (0, 0, *field_rect[2:]))
        self.rect = self.field.get_rect()
        self.rect[:-2] = field_rect[:-2]
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
    chara_rect = np.array((20, 500, 20, 20))
    down_speed = np.array((0, 5))
    move_speed = np.array((5, 0))

    def __init__(self, chara_rect: tuple[int, int, int, int] = chara_rect):
        """"""
        self.image = pg.Surface(chara_rect[2:])
        pg.draw.rect(self.image, (127, 127, 127), (0, 0, *chara_rect[2:]))
        self.rect = self.image.get_rect()
        self.rect[:-2] = chara_rect[:-2]
        return

    def update(self, fields: list) -> None:
        """"""
        self.rect[:-2] = np.array(self.rect[:-2]) + self.down_speed
        for field in fields:
            if field.get_rect().colliderect(self.rect):
                self.rect[:-2] = np.array(self.rect[:-2]) - self.down_speed
        return

    def move(self, LR: str, fields: list) -> None:
        """"""
        move: np.array = np.array((0, 0))
        if LR == "L":
            move = self.move_speed * -1
        elif LR == "R":
            move = self.move_speed
        self.rect[:-2] = self.rect[:-2] + move
        for field in fields:
            if field.get_rect().colliderect(self.rect):
                self.rect[:-2] = np.array(self.rect[:-2]) - move
        return

    def draw(self, screen: pg.Surface) -> None:
        """"""
        screen.blit(self.image, self.rect)
        return


def end(clear: bool) -> None:
    """"""
    print("end")
    return


# main function
def main(screen: pg.Surface, screen_size: np.array) -> bool | None:
    """
        main process
    """
    # setup variables
    clock = pg.time.Clock()

    # setup Surface
    fields: list[Field] = [Field()]
    chara = Character()

    # fields make
    wall_width = 20
    fields.append(Field((0, 0, wall_width, screen_size[1])))
    fields.append(Field((win_size[0]-wall_width, 0, wall_width, screen_size[1])))

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
            chara.move("L", fields)

        if key_pressed[pg.K_RIGHT]:
            chara.move("R", fields)

        # update
        chara.update(fields)

        # draw
        screen.fill("white", (0, 0, 1000, 600))
        for field in fields:
            field.draw(screen)
        chara.draw(screen)
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
        reboot = main(master, win_size)

        # end process
        if reboot is None:
            reboot = False
        pg.quit()

    sys.exit()
