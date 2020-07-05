#import socket
import pygame 
import random
import keyboard 
from os import path
from network import Network               

#n.auth()
bullet_shoot = False

WIDTH = 480
HEIGHT = 600
FPS = 60
#load all game graphics
background = pygame.image.load('blue.png')
background_rect = background.get_rect()
player_img = pygame.image.load('PlayerShip.png')
meteor_img = pygame.image.load('meteor.png')
enemy_img = pygame.image.load('EnemyShip.png')
bullet_img = pygame.image.load('laser.png')
#Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        #global mob_y 
        #global mob_speedy
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)



    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

mobs = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    mobs.add(m)

class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self,centerx, bottom, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
       	self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
       	if keystate [pygame.K_LEFT]:
            self.speedx = -5
            #print("Player Moving to left and New postion: ", self.rect.centerx, self.rect.top)
        if keystate [pygame.K_UP]:
            self.speedy = -5
        if keystate [pygame.K_DOWN]:
            self.speedy = +5

        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
            #print("Player Moving to right and New postion: ", self.rect.centerx, self.rect.top)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        return str(self.rect.centerx)+","+str(self.rect.top)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -5
    def update(self):
        self. rect.y += self.speedy
        #remove it if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
bullets = pygame.sprite.Group()

#Initialize pygame and create the window
def read_pos(str):
    str = str.split(",")
    #print(str[2])
    if str[2] ==  "shoot":
        #print(str[2])
        global bullet_shoot
        bullet_shoot = True
    else:
        bullet_shoot = False
    #print(str[2])
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

n = Network()

boolian = True
while boolian:
    choice = int(input("Enter Your Choice:\n1. Create New Accout\n2. Sign In\n"))

    if choice == 1:
        username = input("Enter User Name: ")
        pswd1 = input("Enter Password: ")
        pswd2 = input("Confirm Password: ")
        if(pswd1 == pswd2):
            mesg = str(choice)+" "+username+" "+ pswd1
            print(mesg)
            mesg = n.send(mesg)
            #mesg = self.client.recv(1024).decode("utf-8")
            if(mesg == "True"):
                print("Your Account has been created.\nNow, Sign In to Play the Game")
                # fuction call for choice
            else:
                print("Something went wrong please try again.")
                #fucntion call to choice

    elif choice == 2:
        username = input("Enter User Name: ")
        password = input("Enter your Password: ")
        mesg = str(choice)+" "+username+" "+password
        #self.client.send(mesg.encode("utf-8"))
        #mesg = self.client.recv(1024).decode("utf-8")
        mesg = n.send(mesg)
        if(mesg == "True"):
            print("Login Successfull!\n Press SPACE to play the game")
            #fucntion call for game
            keyboard.wait("SPACE")
            boolian = False

        else:
            print("You have enter wrong credentials!\nPlease try again.")
            #fucntion call to choice
    else:
        print("You have enter wrong choice!")

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("vishesh")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_sprites.add(m)
#Game LÖÖP
running = True
startPos = read_pos(n.getPos())
print(startPos)
p = Player(startPos[0],startPos[1],"PlayerShip.png")
p2 = Player(100,590, "EnemyShip.png")
all_sprites.add(p)
all_sprites.add(p2)
while running:
    #Keep loop running at the right speed
    clock.tick(FPS)
    data = n.send(make_pos((p.rect.centerx,p.rect.bottom)))
   #print(data)
    p2Pos = read_pos(data)
    p2.rect.centerx = p2Pos[0]
    p2.rect.bottom = p2Pos[1]
    p2.update()

    p.shoot()
    p2.shoot()
    #Check to see if a mob hit the Player
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        #print("Enemy dies!")'''


# Player Dies!
    '''hits = pygame.sprite.spritecollide(p, mobs, False)
    if hits:
    	#print("Player dies!")
    	running = False
    hits = pygame.sprite.spritecollide(p2, mobs, False)
    if hits:
    	#print("Player dies!")
    	running = False'''

    #Procces input
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
    if event.type == pygame.KEYDOWN:
        '''if event.key == pygame.K_SPACE:
            p.shoot()
            #n.bullet_shoot("True")
            n.send("shoot")
            print(bullet_shoot)
            if bullet_shoot:
                print("Bullet Shoots")
                p2.shoot()'''
        #if evet.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            pygame.quit()
            #print("Player shoots bullet")
    #Update
    all_sprites.update()

    #Draw / render

    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
    screen.fill(BLACK)

