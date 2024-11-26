import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0, -5), pg.K_DOWN:(0,5),
                 pg.K_LEFT:(-5, 0), pg.K_RIGHT:(5, 0)}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル(横方向判定結果，縦方向判定結果)
    画面内ならTrue，画面外なら  False
    """
    yoko, tate = True, True
    if rct.left < 0 or rct.right > WIDTH :  # 横方向の判定
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:  # 縦方向の判定
        tate = False
    return yoko, tate


def gameover(screen :pg.Surface) -> None :
    """
    ゲームオーバー時に，半透明の黒い画面上に
    「Game Over」と表示し，
    泣いているこうかとん画像を貼り付ける関数
    引数：スクリーンのサーフェス
    戻り値：なし
    """
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)  # fig/8.png の画像を0.9倍する
    bg_black = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(bg_black, (0, 0, 0),(0, 0, WIDTH, HEIGHT))
    bg_black.set_alpha(120)
    screen.blit(bg_black, [0, 0])

    font = pg.font.Font(None, 50)
    txt = font.render("Game Over", True, (255, 255, 255))
    screen.blit(txt, [WIDTH//2 - 100, HEIGHT // 2])
    screen.blit(kk_img, [WIDTH/2 - 150, HEIGHT // 2])
    screen.blit(kk_img, [WIDTH/2 + 100, HEIGHT // 2])
    pg.display.update()
    time.sleep(10)
    return None


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    10段階の爆弾のの大きさ，
    加速度を準備する関数
    引数：なし
    戻り値：加速度のリストととサーフェスを格納したリスト
    """
    accs = [a for a in range(1, 11)]  # 加速度のリスト
    bb_imgs = []  # サーフェスを格納するリスト
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))  
        pg.draw.circle(bb_img,(255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, accs  # 加速度のリストととサーフェスを格納したリストを返す


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    飛ぶ方向に従ってこうかとん画像を切り替える関数
    引数：こうかとんの移動量(タプル)
    戻り値：こうかとんのサーフェス
    """
    kk_imgs = {(0,0) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),  # 静止時
               (0,5) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9),  # 下
               (0,-5) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),  # 左
               (5,0) : pg.transform.rotozoom(pg.image.load("fig/3.png"), , 0.9),  # 右
               (5,5) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),  # 右下
               (5,-5) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),  # 右上
               (-5,0) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),  # 左
               (-5,5) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),  # 左下
               (-5,-5) : pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # 左上
              }
    
    


def calc_orientation(org: pg.Rect, dst: pg.Rect,
                     current_xy: tuple[float,float]) -> tuple[float, float]:
    pass

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の赤い半径10の円
    pg.draw.circle(bb_img,(255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5  # 爆弾の単位時間当たりの移動量
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()
    avx = vx*bb_accs[min(tmr//500, 9)]  # 加速度のリスト
    bb_img = bb_imgs[min(tmr//500, 9)]  # サーフェスのリスト

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        # こうかとんが爆弾と衝突したらゲームオーバー
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return 
        screen.blit(bg_img, [0, 0]) 
        
        bb_img = bb_imgs[min(tmr//500, 9)]
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in DELTA.items():
            if key_lst[k] :
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        yoko, tate =  check_bound(bb_rct) 
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        # kk_img = get_kk_img((0, 0))
        # kk_img = get_kk_img(tuple(sum_mv))
        kk_rct.move_ip(sum_mv)
        bb_rct.move_ip(avx, avy)
        if check_bound(kk_rct) != (True, True) :  # 画面外に出ていたら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
