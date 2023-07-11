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
class test:
    pass


# main function
def main() -> bool | None:
    """
        main process
    """
    # setup variables

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
    return


# start and end process
if __name__ == '__main__':
    # setup window variables
    game_name = "Action!!"
    version = "1.1.0"

    win_size = (1000, 600)

    # boot main
    reboot = True
    while reboot:
        # start process
        pg.init()
        pg.display.set_caption(f"{game_name} ver.{version}")
        pg.display.set_mode(win_size)

        # main
        reboot = main()

        # end process
        if reboot is None:
            reboot = False
        pg.quit()

    sys.exit()
