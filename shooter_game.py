from pygame import *
from random import randint
 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_w, player_h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_w,player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top,35,35,-15)
        bullets.add(bullet)
        fire.play()
 
 
class Enemy(GameSprite):
    def update(self):
        global missed  
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = 50*randint(1,13)
            missed += 1
        self.rect.y += self.speed
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y<0:
            self.kill()
 
#fonts
font.init()
font1 = font.SysFont('Arial',80)
font2 = font.SysFont('Arial',36)
 
#GLOBAL VARIABLES
missed = 0
hit = 0
max_missed = 20
 
 
 
window = display.set_mode((700, 500))
display.set_caption("Space Invaderz")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
mixer.init()
mixer.music.load('Phantom_from_Space.mp3') 
mixer.music.play()
fire=mixer.Sound('fire.ogg')
#money=mixer.Sound('money.ogg')
 
hero = Player("rocket.png",0,400,55,55,5)
 
ufos = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
 
for i in range (1,6):
    ufo = Enemy("ufo.png", 50*randint(1,13), -40,50,50, randint(1,3))
    ufos.add(ufo)
for j in range (1,4):
    asteroid = Enemy("asteroid.png", 50*randint(1,13), -40,55,55, randint(1,5))
    asteroids.add(asteroid)
 
 
 
 
font.init()
font = font.SysFont('Arial',70)
win = font.render("YOU WIN!",True,(255,215,0))
lose = font.render("YOU LOSE!",True,(255,0,0))
 
#game loop
run = True
finish = False
clock = time.Clock()
FPS = 60
 
while run:
 
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
    
    if finish != True:
        window.blit(background,(0, 0))
        text = font2.render("Missed: " + str(missed), 1, (255,255,255))
        window.blit(text,(10,20))
 
        text2 = font2.render("Score: " + str(hit), 1, (255,255,255))
        window.blit(text2,(10,50))
 
 
        keys_pressed = key.get_pressed()
        
        hero.reset()
        ufos.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
 
        hero.update()
        ufos.update()
        bullets.update()
        asteroids.update()
 
        collides = sprite.groupcollide(ufos,bullets, True,True)
        for c in collides:
            hit += 1
            ufo = Enemy("ufo.png",50*randint(1,13),0,50,50,randint(1,3))
            ufos.add(ufo)
        
        if sprite.spritecollide(hero, ufos, False) or sprite.spritecollide(hero, asteroids, False) or missed>max_missed:
            finish=True
            window.blit(lose,(200,200))
 
        if hit >= 30:
            finish=True
            window.blit(win,(200,200))
 
 
        
    
        display.update()
    
    else:
        finish = False
        hit=0
        missed=0
        for b in bullets:
            b.kill()
        for u in ufos:
            u.kill()
        for a in asteroids:
            a.kill()
        
        time.delay(3000)
        for i in range (1,6):
            ufo = Enemy("ufo.png", 50*randint(1,13), -40,50,50, randint(1,4))
            ufos.add(ufo)
        for j in range (1,4):
            asteroid = Enemy("asteroid.png", 50*randint(1,13), -40,40,40, randint(1,5))
            asteroids.add(asteroid)
 
 
    clock.tick(FPS)
 

