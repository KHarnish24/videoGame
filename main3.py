# content from kids can code: http://kidscancode.org/blog/

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
from random import randint
from math import *
from time import *

'''

The goal of the game is to reach the end of all 5 waves by not getting hit by any enemys

Goals:

create at least 3 enemys with difftent traits

create a power up that the player can activate 

create a wave system

create a gun the player can shoot



'''

# Defining a vector
vec = pg.math.Vector2

# game settings 
WIDTH = 800
HEIGHT = 500
FPS = 30
# player friction
player_fric = -0.2
# time keeping vars
pt = 0
ct=0
# fire rate
rt=1
# death variables
died = False
cd = False

# score 
score = 0

# level

level = 0


# game end

won = False
cw = False

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKBLUE = (26, 17, 112)
PINK = (232, 151, 152)
LIGHTGRAY = (212, 212, 212)
GRAY = (128, 128, 128)
DARKGRAY = (77, 77, 77)
PURPLE = (108, 0, 171)
LIME = (151, 255, 107)
LIGHTORANGE = (255, 215, 163)
ORANGE = (237, 134, 0)



# text drawing
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('calibri')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)




# creates the player class and defines its capabilitys 
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50, 30))
        self.image.fill(DARKBLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, 420)
        self.pos = vec(WIDTH/2, 420)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.canshoot = False
    
    # gets input for controlls
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5             
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.shoot()
            
    # moves the player and the visual rect
    def movement(self):
        self.acc += self.vel * player_fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        self.acc = vec(0,0)
    
    # creates a pellet and is using a timer to only fire every after every 0.5 sec at the base rate
    def shoot(self):
        global ct
        global pt
        ct = pg.time.get_ticks()
        if self.canshoot == True:
            p = Pellet() 
           
            all_projectiles.add(p)
            self.canshoot = False
        elif self.canshoot == False:
            if ct - pt > 500/rt:
                self.canshoot = True
                pt = ct
        
        

        
            
        
            # check to see if player is in bounds

    def boundCheck(self):
        if self.rect.right > 800:
            self.rect.right = 800
            self.vel.x = 0
            self.acc.x = 0
            self.pos = self.rect.center
            self.pos += self.vel + 0.5 * self.acc
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel.x = 0
            self.acc.x = 0
            self.pos = self.rect.center
            self.pos += self.vel + 0.5 * self.acc

# check to see if player should be dead

    def deathCheck(self):
        global died
        hits = pg.sprite.spritecollide(self, all_mobs, False)
        if hits:
            died = True
            

# updates player

    def update(self):
        self.controls()
        self.movement()
        self.boundCheck()
        self.deathCheck()
        

# creates pellet class


class Pellet(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (gun.pos.x, gun.pos.y-10)
        self.pos = vec(gun.pos.x, gun.pos.y-10)
        
        # moves pellet
    
    def update(self):
        self.pos.y -= 15
        self.rect.center = self.pos
        if(self.pos.y <0):
            self.kill()
            
    

        
# creates rect to be a visual gun
class Gun(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((15, 25))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (player.pos.x, player.pos.y-25)
        self.pos = vec(player.pos.x, player.pos.y-25)

        
            # moves gun to player position

    def update(self):
        self.pos = vec(player.pos.x, player.pos.y-25)
        self.rect.center = self.pos


# creates MobA Class

class MobA(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((25, 25))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.center = (randint(25,775),50)
        self.pos = vec(randint(25,775),50)
        self.dir = randint(0,1)
        self.attacking = False
        self.hitBottom = False


        # movement for mob a to keep it in bounds and move randomly on y but still restrainded

    def movement(self):
        if self.dir == 1:
            self.pos.x += 5
            self.rect.center = self.pos
        if self.dir == 0:
            self.pos.x -= 5
            self.rect.center = self.pos
        if self.pos.y > 15 and self.pos.y < 150:
            self.pos.y += randint(-5,5)
            self.rect.center = self.pos
        elif self.pos.y <= 15:
            self.pos.y += randint(1,5)
            self.rect.center = self.pos
        elif self.pos.y >= 150:
            self.pos.y += randint(-5,-1)
            self.rect.center = self.pos
        
# bounces mob off walls

    def bounceCheck(self):
        if self.rect.left <=0:
            self.dir = 1
        if self.rect.right >=800:
            self.dir = 0


# mob swoops down to player to attack

    def attack(self):
        if self.hitBottom == False:
                self.pos.y += 8
                self.rect.center = self.pos
                if self.pos.y >= 440:
                    self.hitBottom = True
        elif self.hitBottom == True:
            self.pos.y -= 8
            self.rect.center = self.pos
            if self.pos.y <= 50:
                    self.attacking = False
                    self.hitBottom = False


# updates and switches between attack and movemnt states

    def update(self):
        global score
        if self.attacking == False:
            self.movement()
            self.bounceCheck()
            ac = randint(1,200)
            if ac == 1:
                self.attacking = True
        if self.attacking == True:
            self.attack()
        hits = pg.sprite.spritecollide(self, all_projectiles, True)
        if hits:
            score = score + 5
            self.kill()
        


# creates Mob b
class MobB(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((120, 35))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (randint(25,775),150)
        self.pos = vec(randint(25,775),150)
        self.dir = randint(0,1)
        self.hp = 3

        # movement is mainly the same
    
    def movement(self):
        if self.dir == 1:
            self.pos.x += 3
            self.rect.center = self.pos
        if self.dir == 0:
            self.pos.x -= 3
            self.rect.center = self.pos

            # bouncing is the same
    
    def bounceCheck(self):
        if self.rect.left <=0:
            self.dir = 1
        if self.rect.right >=800:
            self.dir = 0

            # a health tracker to change colors to tell the player how much health this enemy has left

    def healthTracker(self):
        global score
        hits = pg.sprite.spritecollide(self, all_projectiles, True)
        if hits:
            self.hp -= 1
        if self.hp == 2:
            self.image.fill(RED)
        if self.hp == 1:
            self.image.fill(PINK)
        if self.hp <= 0:
            score = score + 10
            self.kill()

            # the update method

    def update(self):
        self.movement()
        self.bounceCheck()
        self.healthTracker()


# most mobs from here are simular so I will only cover what makes them diffrent

class MobC(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((35, 35))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (randint(25,775),200)
        self.pos = vec(randint(25,775),200)
        self.dir = vec(randint(0,1),randint(0,1))

        # movement is now in all directions so dirrection is now a vector

    def movement(self):
        if self.dir.x == 1:
            self.pos.x += 5
            self.rect.center = self.pos
        if self.dir.x == 0:
            self.pos.x -= 5
            self.rect.center = self.pos
        if self.dir.y == 1:
            self.pos.y += 5
            self.rect.center = self.pos
        if self.dir.y == 0:
            self.pos.y -= 5
            self.rect.center = self.pos

            # bounce now has to check for more directions

    def bounceCheck(self):
        if self.rect.left <=0:
            self.dir.x = 1
        if self.rect.right >=800:
            self.dir.x = 0
        if self.rect.top <=0:
            self.dir.y = 1
        if self.rect.bottom >=500:
            self.dir.y = 0

# simular update to mob a

    def update(self):
        global score
        self.movement()
        self.bounceCheck()
        hits = pg.sprite.spritecollide(self, all_projectiles, True)
        if hits:
            score = score + 10
            self.kill()


            
# Mob D is like Mob A but with the health of mob B

class MobD(Sprite):

    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((60, 60))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (randint(25,775),110)
        self.pos = vec(randint(25,775),110)
        self.dir = randint(0,1)
        self.attacking = False
        self.hitBottom = False
        self.hp = 3

    def movement(self):
        if self.dir == 1:
            self.pos.x += 7
            self.rect.center = self.pos
        if self.dir == 0:
            self.pos.x -= 7
            self.rect.center = self.pos
        if self.pos.y > 75 and self.pos.y < 190:
            self.pos.y += randint(-5,5)
            self.rect.center = self.pos
        elif self.pos.y <= 75:
            self.pos.y += randint(1,5)
            self.rect.center = self.pos
        elif self.pos.y >= 190:
            self.pos.y += randint(-5,-1)
            self.rect.center = self.pos


    def bounceCheck(self):
        if self.rect.left <=0:
            self.dir = 1
        if self.rect.right >=800:
            self.dir = 0

    def attack(self):
        if self.hitBottom == False:
                self.pos.y += 5
                self.rect.center = self.pos
                if self.pos.y >= 450:
                    self.hitBottom = True
        elif self.hitBottom == True:
            self.pos.y -= 5
            self.rect.center = self.pos
            if self.pos.y <= 110:
                    self.attacking = False
                    self.hitBottom = False

    def healthTracker(self):
        global score
        hits = pg.sprite.spritecollide(self, all_projectiles, True)
        if hits:
            self.hp -= 1
        if self.hp == 2:
            self.image.fill(LIME)
        if self.hp == 1:
            self.image.fill(LIGHTORANGE)
        if self.hp <= 0:
            score = score + 15
            self.kill()

    def update(self):
        if self.attacking == False:
            self.movement()
            self.bounceCheck()
            ac = randint(1,300)
            if ac == 1:
                self.attacking = True
        if self.attacking == True:
            self.attack()
        self.healthTracker()



    # Mob E is a Power Up to give the player more shooting speed 


class MobE(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((35, 35))
        self.image.fill(LIGHTGRAY)
        self.rect = self.image.get_rect()
        self.rect.center = (randint(25,775),50)
        self.pos = vec(randint(25,775),50)
        self.dir = randint(0,1)
    



    def movement(self):
        if self.dir == 1:
            self.pos.x += 3
            self.rect.center = self.pos
        if self.dir == 0:
            self.pos.x -= 3
            self.rect.center = self.pos

    def bounceCheck(self):
        if self.rect.left <=0:
            self.dir = 1
        if self.rect.right >=800:
            self.dir = 0


            # gives a randomized flash based on randint to help it stick out

    def flash(self):
        clr = randint(0,2)
        if clr == 0:
            self.image.fill(LIGHTGRAY)
        if clr == 1:
            self.image.fill(ORANGE)
        if clr == 2:
            self.image.fill(BLACK)

            # doubles player shoot speed with rt variable

    def update(self):
        global score
        global rt
        self.movement()
        self.bounceCheck()
        self.flash()
        hits = pg.sprite.spritecollide(self, all_projectiles, True)
        if hits:
            score = score + 5
            rt = rt*2
            self.kill()
         


    



# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()


# create a group for all sprites
all_players = pg.sprite.Group()
all_sprites = pg.sprite.Group()
all_mobs = pg.sprite.Group()
all_projectiles = pg.sprite.Group()


# init player
player = Player()
gun = Gun()





# add items to groups
all_players.add(player)
all_players.add(gun)



# add groups to groups

all_sprites.add(all_projectiles) 
all_sprites.add(all_players)
all_sprites.add(all_mobs)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False

############ Update ##############
# update all sprites


    # create levels 


    # level 1

    if level == 0 and score == 0:
        level = 1
        for x in range(6):
            mA = MobA()
            all_mobs.add(mA)

    # level 2

    if level == 1 and score == 30:
        level = 2
        for x in range(4):
            mA = MobA()
            all_mobs.add(mA)
        for x in range(3):
            mB = MobB()
            all_mobs.add(mB)

    # level 3

    if level == 2 and score == 80:
        level = 3
        for x in range(4):
            mA = MobA()
            all_mobs.add(mA)
        for x in range(2):
            mB = MobB()
            all_mobs.add(mB)
        for x in range(3):
            mC = MobC()
            all_mobs.add(mC)
        mE = MobE()
        all_mobs.add(mE)

    # level 4

    if level == 3 and score == 155:
        level = 4
        for x in range(5):
            mA = MobA()
            all_mobs.add(mA)
        for x in range(3):
            mB = MobB()
            all_mobs.add(mB)
        for x in range(1):
            mC = MobC()
            all_mobs.add(mC)
        for x in range(2):
            mD = MobD()
            all_mobs.add(mD)
        mE = MobE()
        all_mobs.add(mE)

# level 5


    if level == 4 and score == 255:
        level = 5
        for x in range(7):
            mA = MobA()
            all_mobs.add(mA)
        for x in range(6):
            mB = MobB()
            all_mobs.add(mB)
        for x in range(5):
            mC = MobC()
            all_mobs.add(mC)
        for x in range(4):
            mD = MobD()
            all_mobs.add(mD)

    # won game

    if score == 460:
        won = True
        
    
# updateing the objects
    
    
    all_sprites.update()
    all_projectiles.update()
    all_mobs.update()


    ############ Draw ################
    # draw the background screen
    screen.fill(DARKGRAY)
    # draw all sprites
    all_sprites.draw(screen)
    all_projectiles.draw(screen)
    all_mobs.draw(screen)

    # draw text

    draw_text('Score: '+ str(score),20,LIGHTGRAY,40,20)
    draw_text('Level: '+ str(level),20,LIGHTGRAY,40,40)



# shows lost text and ends the game
    if died == True:
        if cd == True:
            pg.time.wait(1000)
            pg.quit()
        draw_text('You Died',200,RED,400,160)
        cd = True


# shows won text and ends the game
    if won == True:
        if cw == True:
            pg.time.wait(2000)
            pg.quit()
        draw_text('You Won',200,GREEN,400,160)
        cw = True

        
        
   
        
    # buffer - after drawing everything, flip display
    
    pg.display.flip()

pg.quit()
