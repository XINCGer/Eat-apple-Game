import itertools, sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *

def calc_velocity(direction, vel=1.0):
    velocity = Point(0,0)
    if direction == 0: #上
        velocity.y = -vel
    elif direction == 2: #右
        velocity.x = vel
    elif direction == 4: #下
        velocity.y = vel
    elif direction == 6: #左
        velocity.x = -vel
    return velocity

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("吃苹果")
font = pygame.font.Font(None, 36)
timer = pygame.time.Clock()

#创建精灵组
player_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

#初始化玩家精灵组
player = MySprite()
player.load("farmer walk.png", 96, 96, 8)
player.position = 80, 80
player.direction = 4
player_group.add(player)

#初始化food精灵组

for n in range(1,50):
    food = MySprite();
    food.load("food_low.png", 35, 35, 1)
    food.position = random.randint(0,780),random.randint(0,580)
    food_group.add(food)

game_over = False
player_moving = False
player_health = 0


while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()
    elif keys[K_UP] or keys[K_w]:
        player.direction = 0
        player_moving = True
    elif keys[K_RIGHT] or keys[K_d]:
        player.direction = 2
        player_moving = True
    elif keys[K_DOWN] or keys[K_s]:
        player.direction = 4
        player_moving = True
    elif keys[K_LEFT] or keys[K_a]:
        player.direction = 6
        player_moving = True
    else:
        player_moving = False


    if not game_over:
        #根据角色的不同方向，使用不同的动画帧
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns-1
        if player.frame < player.first_frame:
            player.frame = player.first_frame

        if not player_moving:
            #当停止按键（即人物停止移动的时候），停止更新动画帧
            player.frame = player.first_frame = player.last_frame
        else: 
            player.velocity = calc_velocity(player.direction, 1.5)
            player.velocity.x *= 1.5
            player.velocity.y *= 1.5

        #更新玩家精灵组
        player_group.update(ticks, 50)

        #移动玩家
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0: player.X = 0
            elif player.X > 700: player.X = 700
            if player.Y < 0: player.Y = 0
            elif player.Y > 500: player.Y = 500

        #检测玩家是否与食物冲突，是否吃到果实
        attacker = None
        attacker = pygame.sprite.spritecollideany(player, food_group)
        if attacker != None:
            if pygame.sprite.collide_circle_ratio(0.65)(player,attacker):
                player_health +=2;
                food_group.remove(attacker);
        if player_health > 100: player_health = 100
        #更新食物精灵组
        food_group.update(ticks, 50)

        if len(food_group) == 0:
            game_over = True
    #清屏
    screen.fill((50,50,100))

    #绘制精灵
    food_group.draw(screen)
    player_group.draw(screen)

    #绘制玩家血量条
    pygame.draw.rect(screen, (50,150,50,180), Rect(300,570,player_health*2,25))
    pygame.draw.rect(screen, (100,200,100,180), Rect(300,570,200,25), 2)

    if game_over:
        print_text(font, 300, 100, "G A M E   O V E R")
    
    pygame.display.update()
    

