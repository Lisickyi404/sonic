import pygame
import random
from sprites import *

def collide(Sprite1, Sprite2):
    if ((Sprite1.x <  Sprite2.x  < Sprite1.x + Sprite1.width
        and   Sprite1.y < Sprite2.y < Sprite1.y + Sprite1.height)
        or   (Sprite1.x < Sprite2.x + Sprite2.width  < Sprite1.x + Sprite1.width
        and   Sprite1.y < Sprite2.y + Sprite2.height < Sprite1.y + Sprite1.height)
        or   (Sprite2.x < Sprite1.x < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y < Sprite2.y + Sprite2.height)
        or   (Sprite2.x < Sprite1.x + Sprite1.width  < Sprite2.x + Sprite2.width
        and   Sprite2.y < Sprite1.y + Sprite1.height < Sprite2.y + Sprite2.height)):
            return  True
    else:
        return False
WorldWidth = 4000 # ширина игрового мира
WorldHeight = 3000 # высота игрового мира
ScreenWidth = 800 #ширина окна программы
ScreenHeight = 600 #высота окна программы
ztimer = 0
clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
window = pygame.display.set_mode ((ScreenWidth, ScreenHeight))
world = pygame.Surface((WorldWidth, WorldHeight))
world_copy = pygame.Surface((WorldWidth, WorldHeight))
x = 0
y = 0
imgGrass = pygame.image.load(r'images/Grass.jpg')
while y < WorldHeight:
    while x < WorldWidth:
        world_copy.blit(imgGrass,
                   (x, y))
        x += imgGrass.get_width()
    y += imgGrass.get_height()
    x = 0
trees = []
for i in range(20):
    tr = Sprite(random.randint(0,WorldWidth),
                random.randint(0,WorldHeight),
                0,r'images/tree.png')
    trees.append(tr)
    world_copy.blit(tr.image,
                    (tr.x, tr.y))
player = Player(100,700,20, r'images/sonic.png')
player.imgL = pygame.transform.scale(player.imgL,
                                      [
                                          int(player.width*0.2),
                                          int(player.height*0.2)
                                      ])
player.imgR = pygame.transform.scale(player.imgR,
                                      [
                                          int(player.width*0.2),
                                          int(player.height*0.2)
                                      ])
player.width = player.imgL.get_width()
player.height = player.imgL.get_height()
camera = Camera(WorldWidth,WorldHeight,ScreenWidth,ScreenHeight)

zombiki = []
bullets = []
game = True
while game:
    ###Для закрытия проги
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            game = False
    ###

    f1 = pygame.font.Font(None, 35)
    nadpis_fps = f1.render(str(int(clock.get_fps())),
                           True,
                           (0, 0, 0))
    keys = pygame.key.get_pressed()
    player.update(keys)
    camera.update(player)#НЕ ЗАБУДЬТЕ!
    if pygame.mouse.get_pressed()[0]:#если нажимаю на кнопку
        bul = Bullet(
            player.x,
            player.y,
            pygame.mouse.get_pos()[0]-camera.x,
            pygame.mouse.get_pos()[1]-camera.y,
            r'images/bullet.png'
        )
        bullets.append(bul)
    for bul in bullets:
        bul.x +=bul.x_prirost
        bul.y += bul.y_prirost

        if bul.rasst(
                bul.x_nachala,
                bul.y_nachala,
                bul.x,
                bul.y)>bul.begin_rasst:
            bullets.remove(bul)
    ztimer+=1
    if ztimer ==100:
        ztimer = 0
        zombi = Zombi(200, 800, player, r'images/ZOMBI.PNG')
        zombiki.append(zombi)
    for z in zombiki:
        z.update()

    window.fill((255,255,255))
    # world.fill((255,255,255))#Surface - поверхность!
    world.blit(world_copy,
               (0,0))


    world.blit(player.image,
               (player.x,player.y))
    for bul in bullets:
        world.blit(bul.image,
                   (bul.x, bul.y))
    for z in zombiki:
        world.blit(z.image,
                   (z.x, z.y))

    window.blit(world,
                (camera.x,camera.y))

    window.blit(nadpis_fps,
                (0,0))
    clock.tick(60)
    pygame.display.flip()

pygame.quit()