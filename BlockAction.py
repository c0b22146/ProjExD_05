"""

    ProjExD 共同開発
    ・・・

"""
# import module
import sys
import pygame as pg
import random
import numpy as np
import time


class Goal:
    """
    ゴールできます
    """
    def __init__(self, goal_post:list):#ゴールマークの四角を書いています
        goal_post[1] = goal_post[1] * -1 + 540

        self.goal_size = np.array((30, 30))
        self.image = pg.Surface(self.goal_size)
        pg.draw.rect(self.image, (163, 212, 255), (0, 0, *self.goal_size))
        self.rect = self.image.get_rect()
        self.rect[:-2] = goal_post
        return

    def draw(self, screen: pg.Surface) -> None:
        """"""
        screen.blit(self.image, self.rect)#ゴールの四角出現
        return
    
    def do_goal(self, chara_rct: pg.Rect):
        return pg.Rect.contains(self.rect, chara_rct)#四角に四角inしてたらTrue

class Status:#残り時間を表示
    def __init__(self, limit):
        self.font = pg.font.Font(None, 50)
        self.limit = limit

    def draw(self, screen: pg.Surface):
        self.txt = self.font.render(str((self.time_limit)/50), True, (255, 255, 255))
        screen.blit(self.txt, [10, 560])#残り時間表示
    
    def update(self, tmr):#時間を更新。self.time_limitは残り時間
        self.time_limit = self.limit-tmr
        if self.time_limit <= 0:
            return True
        return False


# class objects
class Field:
    """
        class about field
    """
    # setup variables
    field_unit = 5
    base_flore = 530

    def __init__(self, field_rect: tuple[int, int, int, int] = (0, 0, 1000, 100)):
        """"""
        field_rect = np.array(field_rect)
        field_rect[1] = self.base_flore - field_rect[1]
        field_rect = field_rect // 5 * self.field_unit
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
    field_unit = Field.field_unit
    chara_color = np.array((127, 127, 127))
    chara_rect = np.array((20, 500, field_unit*4, field_unit*4))
    down_speed = np.array((0, field_unit))
    move_speed = np.array((field_unit, 0))
    effect_rect = np.array((0, 0, field_unit, field_unit))
    effect_time = 25

    def __init__(self, chara_rect: tuple[int, int, int, int] = chara_rect, effect_freq: int = 2):
        """"""
        self.image = pg.Surface(chara_rect[2:])
        pg.draw.rect(self.image, self.chara_color, (0, 0, *chara_rect[2:]))
        self.rect = self.image.get_rect()
        self.rect[:-2] = chara_rect[:-2]
        # effect image
        self.effect_image = pg.Surface(self.effect_rect[2:])
        pg.draw.rect(self.effect_image, self.chara_color, self.effect_rect)
        self.effects = list()
        self.remove_alpha = 255//self.effect_time
        self.effect_freq = effect_freq
        self.jump_time = 0
        self.jump_poss = False
        return

    def update(self, fields: list) -> None:
        """"""
        # effect process
        #  effect create
        if random.randint(0, self.effect_freq-1) == 0:
            effect = self.effect_image.copy()
            effect_rect = effect.get_rect()
            effect_rect[:-2] = \
                [random.randint(self.rect[i], self.rect[i] + self.rect[i+2] - effect_rect[i+2])
                 for i in range(2)]
            self.effects.append([255, effect, effect_rect])
        #  effect update
        for i in range(len(self.effects)):
            self.effects[i][0] -= self.remove_alpha
            self.effects[i][1].set_alpha(self.effects[i][0])
        if len(self.effects) > 0 > self.effects[0][0]:
            del self.effects[0]

        if self.jump_time <= 0 :
            self.rect[:-2] = np.array(self.rect[:-2]) + self.down_speed
            for field in fields:
                if field.get_rect().colliderect(self.rect):
                    self.rect[:-2] = np.array(self.rect[:-2]) - self.down_speed
                    self.jump_poss = True
        else:
            self.rect[:-2] = np.array(self.rect[:-2]) - self.down_speed
        self.jump_time -= 1

        return
    
    def jump(self):
        if self.jump_poss:
            self.jump_time = 10
            self.jump_poss = False
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
        for effect in self.effects:
            screen.blit(effect[1], effect[2])
        return
    
class Enemy(pg.sprite.Sprite):
    """
        class about Enemy
    """
    enemy_size = np.array((30, 30))
    enemy_down_speed = np.array((0, 5))
    enemy_speed = 5
    
    def __init__(self,x,y):
        """
            敵Surfaceを生成する
        """
        super().__init__()
        self.image = pg.Surface(self.enemy_size)
        pg.draw.rect(self.image, (255, 0, 0), (0, 0, *self.enemy_size))
        self.rect = self.image.get_rect()
        self.rect.center = x,y
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
                will_rect = self.rect.copy()
                will_rect.move_ip(+self.enemy_speed, 0)
                if field.get_rect().colliderect(will_rect):
                    self.rect[:-2] = np.array(self.rect[:-2]) + self.enemy_down_speed
                    self.rect.move_ip(-self.enemy_speed*2, 0)
                    self.enemy_speed *= -1

        return
    
    
    def draw(self, screen: pg.Surface) -> None:
        """
            敵の描画
        """
        screen.blit(self.image, self.rect)
        return


def end(clear: bool, screen: pg.Surface) -> None:
    """
    ゲームの終了処理
    """
    font = pg.font.SysFont(None, 80)
    txtc = font.render("Game Clear!!", True, (255, 0, 0))
    txto = font.render("Game Over!!", True, (0, 0, 255))
    if clear:
        screen.blit(txtc, [320, 250])

    else:
        screen.blit(txto, [320, 250])

    pg.display.update()
    time.sleep(2)
    return


# main function
def main(screen: pg.Surface, screen_size: np.array) -> bool | None:
    """
        main process
    """
    # setup variables
    clock = pg.time.Clock()
    tmr = 0
    time_limit = 50*13

    # setup Surface
    fields: list[Field] = []
    chara = Character()
    timer = Status(time_limit)

    # fields make
    unit = Field.field_unit
    block = unit * 8
    block_list = ((0, 0, 13, 3), (14, 0, 6, 3), (22, 0, 3, 3),
                  (2, 1, 3, 1), (3, 2, 2, 1), (4, 3, 1, 1),
                  (7, 3, 4, 1), (9, 4, 2, 1), (10, 5, 1, 1),
                  (12, 6, 1, 1), (17, 6, 1, 1),
                  (12, 5, 6, 1), (19, 6, 2, 1), (20, 7, 3, 1),
                  (12, 1, 1, 1), (14, 1, 1, 1), (19, 1, 1, 1))
    
    block_list_omake =((2, 4, 1, 1), (0, 5, 1, 1), (2, 6, 1, 1), (0, 7, 1, 1),
                       (2, 8, 1, 1), (0, 9, 1, 1), (2, 10, 1, 1), (0, 11, 1, 1),
                       (2, 12, 1, 1), (0, 13, 1, 1), (2, 14, 22, 1))#これはおまけブロック。
    field_adds = []
    for i in block_list:
        field_adds.append(Field(np.array(i) * block))

    enemys = pg.sprite.Group()
    enemys.add(Enemy(6*block, 1*block))
    enemys.add(Enemy(18*block+20, 1*block))
    enemys.add(Enemy(14*block, 1*block))
        
    for i in block_list_omake:  #おまけ。
        field_adds.append(Field(np.array(i) * block))

    goal = Goal([24 * block + 5, 1 * block])

    # fields setup
    for field_add in field_adds:
        fields.append(field_add)

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
                end(False, screen)
                return

            # reboot process
            if key_pressed[pg.K_DELETE] and key_pressed[pg.KMOD_CTRL]:
                return True

            # player process
        if key_pressed[pg.K_LEFT]:
            chara.move("L", fields)

        if key_pressed[pg.K_RIGHT]:
            chara.move("R", fields)

        for enemy in enemys:
            if pg.sprite.spritecollide(chara, enemys, True):
                if not(chara.rect.bottom <= enemy.rect.top + 5):
                    end(False, screen)
                    return

        if event.type == pg.KEYDOWN and key_pressed[pg.K_UP]:
            chara.jump()

        # update
        chara.update(fields)
        if timer.update(tmr):
            end(False, screen)
            return
        if goal.do_goal(chara.rect):
            end(True, screen)#clear!いえーい
            return
        enemys.update(fields)

        # draw
        screen.fill("white", (0, 0, 1000, 600))
        for field in fields:
            field.draw(screen)
        timer.draw(screen)
        goal.draw(screen)
        chara.draw(screen)
        enemys.draw(screen)
        pg.display.update()

        # tike process
        tmr += 1
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
