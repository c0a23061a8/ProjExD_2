import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5),pg.K_DOWN:(0,5),
                 pg.K_LEFT:(-5,0),pg.K_RIGHT:(5,0),}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
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
    return yoko,tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  
    bb_img = pg.Surface((20, 20))  # 爆弾用の赤い半径10の円
    pg.draw.circle(bb_img,(255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    vx, vy = 5, 5  # 爆弾の単位時間当たりの移動量
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        # こうかとんが爆弾と衝突したらゲームオーバー
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            return 
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,tpl in DELTA.items():
            if key_lst[k] :
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        yoko,tate =  check_bound(bb_rct) 
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        kk_rct.move_ip(sum_mv)
        bb_rct.move_ip(vx,vy)
        if check_bound(kk_rct) != (True,True) :  # 画面外に出ていたら
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
    
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
