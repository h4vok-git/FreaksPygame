import pygame as pg             #this creates an alias for pg as pg which makes it much faster to type in
import time
import random

from settings import *
pg.init()
SHOOT_SOUND = pg.mixer.Sound('sound/shoot.wav')
KILL_SOUND = pg.mixer.Sound('sound/kill.wav')
HURT_SOUND = pg.mixer.Sound('sound/hurt.wav')
GROAN_SOUND = pg.mixer.Sound('sound/hit.wav')
HEAL_SOUND = pg.mixer.Sound('sound/heal.wav')
CASH_SOUND = pg.mixer.Sound('sound/cash.wav')
SHOOT_SOUND.set_volume(0.7)
HURT_SOUND.set_volume(0.5)
KILL_SOUND.set_volume(2.0)
GROAN_SOUND.set_volume(1.0)


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()
shot_time = 0
#player actions
moving_left = False
moving_right = False
shooting = False
wavemsg = "null"

#load sprites
bullet_sprite = pg.image.load('img/bullet/bullet.png').convert_alpha() 
HealthPack_img = pg.image.load('img/misc/health.png').convert_alpha()
sky_img = pg.image.load('img/sky.png').convert_alpha()
dirt_img = pg.image.load('img/dirt.png').convert_alpha()

#load fonts

font = pg.font.SysFont('consolas', 20)
sfont = pg.font.SysFont('consolas', 14)
lfont = pg.font.SysFont('consolas', 44)
mfont = pg.font.SysFont('consolas', 34)
mfont2 = pg.font.SysFont('consolas', 20)


def draw_text(text, font, text_col, x, y):
    text = font.render(text, True, text_col)
    screen.blit(text, (x,y))

def draw_bg():
    screen.fill(BG)
    screen.blit(sky_img,(0,0))
    screen.blit(dirt_img,(0,450))

class Entity(pg.sprite.Sprite):
    def __init__(self, type, x, y, scale, speed):
        pg.sprite.Sprite.__init__(self)
        self.alive = True       #checks if the player is alive
        self.hp = 100
        self.max_hp = self.hp
        self.type = type        
        self.speed = speed      #Is the player speed
        self.direction = 1      #checks which direction the player is facing
        self.vel_y = 0          #player jump velocity (currently zero as the player isn't jumping)
        self.jump = False       #checks if the player has jumped
        self.airborne = True    #checks if the player is airborne
        self.flip = False       #attribute for flipping the player sprite 
        img = pg.image.load(f'img/{self.type}/idle/idle.png').convert_alpha()    #path to the sprite file
        self.image = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) #sprite resize
        self.rect = self.image.get_rect() 
        self.rect.center = (x , y)


    def hitbox(self):
        screen.blit(pg.transform.flip(self.image, self.flip, False), self.rect)
        pg.draw.rect(screen, RED, self.rect, 1)

    def update(self):
        self.check_alive()

    def move(self, moving_left, moving_right):
        #reset movement
        screen_scroll = 0
        dx = 0
        dy = 0 
        #movement
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right: 
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump == True and self.airborne == False:
            self.vel_y = PLAYER_JUMP
            self.jump = False
            self.airborne = True 

        # gravity
        self.vel_y += GRAVITY 
        if self.vel_y > 0:
            self.vel_y > 0
        dy += self.vel_y 

        #check collision
        if self.rect.bottom + dy > 450:
            dy =  450 - self.rect.bottom
            self.airborne = False

        #update player position
        self.rect.x += dx
        self.rect.y += dy
        #update scroll
        if self.type == 'player':
            if self.rect.right > SCREEN_WIDTH + 50 or self.rect.left < -50:
                self.rect.x -= dx 
                

        return screen_scroll

    def ai(self):
        if self.alive and player.alive: 
                if self.rect.centerx > playerpos:
                    ai_moving_right = False
                else:
                    ai_moving_right = True
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right)


    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.speed = 0
            self.alive = False 
        if self.hp == 0:
            self.kill()

    def draw(self):
        screen.blit(pg.transform.flip(self.image, self.flip, False), self.rect)

class Items(pg.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pg.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = HealthPack_img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 100 // 2, y + (300 - self.image.get_height()))
        self.timer = 0

    def update(self):
        #check if the player has picked up the box
        self.timer += 1
        if pg.sprite.collide_rect(self, player) and player.hp != 100:
            #check what kind of box it was        
            if self.item_type == 'Health':
                player.hp += 50
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                self.kill()
                HEAL_SOUND.play()
        if self.timer == 1800:
            self.kill()

class HpBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x 
        self.y = y 
        self.hp = hp 
        self.max_hp = max_hp 

    def draw(self, hp):
        self.hp = hp
        var = self.hp / self.max_hp
        pg.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pg.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pg.draw.rect(screen, DEEPRED, ((self.x + 3), (self.y + 2), 144, 16))
        pg.draw.rect(screen, RED, (self.x, self.y, 150 * var , 20))
        pg.draw.rect(screen, RED1, ((self.x + 3) , (self.y +2), 144 * var , 16))

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.speed = 20
        self.image = bullet_sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def hitbox(self):
        screen.blit(pg.transform.flip(self.image, self.flip, False), self.rect)
        pg.draw.rect(screen, RED, self.rect, 1)

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        #check collision with characters
        if pg.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.hp -= 5
                self.kill()
        for zombie in zombie_group:
            if pg.sprite.spritecollide(zombie, bullet_group, False):
                if zombie.alive:
                    zombie.hp -= 25
                    GROAN_SOUND.play()
                    if zombie.direction == 1:
                        zombie.vel_y = -5
                        zombie.rect.centerx -= 20
                        zombie.speed -= 0.5
                    else:
                        zombie.rect.centerx += 20 
                        zombie.vel_y = -5
                        zombie.speed -= 0.5
                    self.kill()
                if zombie.hp == 0:
                    KILL_SOUND.play() 
                    zombiedeathpos = zombie.rect.centerx
                    health_roll = random.randint(1,4)
                    if health_roll == 1:
                        items = Items('Health', zombiedeathpos, 150)
                        items_group.add(items)
                    global score 
                    score += 10 
            
class Items(pg.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pg.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = HealthPack_img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 100 // 2, y + (300 - self.image.get_height()))
        self.timer = 0

    def update(self):
        #check if the player has picked up the item
        self.timer += 1
        if pg.sprite.collide_rect(self, player) and player.hp != 100:
            #check what kind of item it was        
            if self.item_type == 'Health':
                player.hp += 50
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                self.kill()
                HEAL_SOUND.play()
        if self.timer == 1800:
            self.kill()
    
                
#sprite groups
zombie_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
items_group = pg.sprite.Group()
items1 = Items('Health', 550, 150)
items_group.add(items1)
items2 = Items('Health', 850, 150)
items_group.add(items2)
items3 = Items('Health', 250, 150)
items_group.add(items3)

#sprite transform (x, y, scale, speed)
player = Entity('player', 300, 200, 0.1, PLAYERSPEED)
HpBar = HpBar(10, 10, player.hp, player.hp)
running = True

while running: 
    #fpstext = str(int(clock.get_fps()))
    #print(fpstext)
    pos = pg.mouse.get_pos()
    if gameisplaying == False:
        screen.fill(BG)
        play_button = pg.draw.rect(screen, WHITE, pg.Rect(500, 190, 175, 60))
        draw_text(f'FREAKS', lfont, RED, 520, 30)
        draw_text(f'PLAY', lfont, BLACK, 540, 200)
        draw_text(f'How To Play', mfont, WHITE, 490, 380)
        draw_text(f'[space] jump', font, WHITE, 400, 420)
        draw_text(f'[a] move left', font, WHITE, 400, 440)
        draw_text(f'[d] move right', font, WHITE, 400, 460)
        draw_text(f'[e/lmb] shoot', font, WHITE, 400, 480)
        draw_text(f'[esc] quit', font, WHITE, 400, 500)
        draw_text(f'Kill as many zombies', font, WHITE, 600, 420)
        draw_text(f'as you can to earn points', font, WHITE, 600, 440)
        draw_text(f'use these points for upgrades.', font, WHITE, 600, 460)
        draw_text(f'Pick up medkits to heal', font, WHITE, 600, 480)
        draw_text(f'yourself before they despawn.', font, WHITE, 600, 500)
        draw_text(f'Beware zombie spawn rates will', font, WHITE, 600, 520)
        draw_text(f'increase after each wave', font, WHITE, 600, 540)
        if play_button.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1: 
                gameisplaying = True
    else:
        if player.hp == 0:
            running = False  #quits program if player dies

        player.speed = PLAYERSPEED
        for zombie in zombie_group:
                if wavestart == False and zombie.rect.centerx > 1300 or wavestart == False and zombie.rect.centerx < -100:
                    zombie.kill()   

        if wavestart == True:
            wavemsg = ('wave in progress')
        else:
            wavemsg = ('[r] start wave')


        zombie_spawn_counter += 1
        if zombie_spawn_counter > 200 - (wavenumber * 10) and wavestart == True and zombie_spawn_counter > 3:
            zombie = Entity("zombie", random.choice([-2000, 3000]), 200, 0.2, random.uniform(3.0, 5.0)) 
            zombie_group.add(zombie)
            zombie_spawn_counter = 0

        if zombie_spawn_counter < 0:
            zombie_spawn_counter = 0

        if wavestart == True:
            wave_time += 1
            

        if wave_time == 3000:
            wavestart = False
            wave_time = 0
            
        playerpos = player.rect.centerx 
        iFrame += 10          
        clock.tick(FPS)
        shot_time -= 1
        pg.event.set_grab(True)
        pg.mouse.set_visible(True)
        draw_bg() 
        HpBar.draw(player.hp)



        draw_text(f'{player.hp}', font, BLACK, 12, 16)
        draw_text(f'points:{score}', font, WHITE, 12, 40)
        draw_text(f'wave {wavenumber}', font, WHITE, 180, 16)
        draw_text(f'{wavemsg}', font, RED, 500, 15)
        draw_text(f'[space] jump', sfont, WHITE, 1101, 30)
        draw_text(f'[a] move left', sfont, WHITE, 1093, 45)
        draw_text(f'[d] move right', sfont, WHITE, 1085, 60)
        draw_text(f'[e/lmb] shoot', sfont, WHITE, 1093, 75)
        draw_text(f'[esc] quit', sfont, WHITE, 1117, 90)

        #UPGRADE MENU

        jumpheight_rect = pg.draw.rect(screen, WHITE, pg.Rect(400, 500, 100, 40))
        playerspeed_rect = pg.draw.rect(screen, WHITE, pg.Rect(550, 500, 100, 40))
        firerate_rect = pg.draw.rect(screen, WHITE, pg.Rect(700, 500, 100, 40))
        draw_text(f'Fire Rate', sfont, BLACK, 715, 505)
        draw_text(f'[200 points]', sfont, GREEN, 702, 520)
        draw_text(f'[200 points]', sfont, GREEN, 702, 520)
        draw_text(f'Player Speed', sfont, BLACK, 553, 505)
        draw_text(f'[200 points]', sfont, GREEN, 552, 520)
        draw_text(f'[200 points]', sfont, GREEN, 552, 520)
        draw_text(f'Jump Height', sfont, BLACK, 406, 505)
        draw_text(f'[200 points]', sfont, GREEN, 402, 520)
        draw_text(f'[200 points]', sfont, GREEN, 402, 520)
        draw_text(f'UPGRADES:', mfont2, WHITE, 260, 510)
        draw_text(f'LVL {jumpheighlvl}/5', sfont, WHITE, 420, 545)
        draw_text(f'LVL {playerspeedlvl}/5', sfont, WHITE, 570, 545)
        draw_text(f'LVL {fireratelvl}/5', sfont, WHITE, 720, 545)


        cooldown += 1

        if jumpheight_rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and cooldown > 30 and jumpheighlvl <= 4 and score >= 200: 
                PLAYER_JUMP -= 1.5
                cooldown = 0 
                jumpheighlvl += 1
                score -= 200
                CASH_SOUND.play()

        if playerspeed_rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and cooldown > 30 and playerspeedlvl <= 4 and score >= 200: 
                PLAYERSPEED += 2
                cooldown = 0 
                playerspeedlvl += 1
                score -= 200
                CASH_SOUND.play()

        if firerate_rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and cooldown > 30 and fireratelvl <= 4 and score >= 200: 
                SHOT_DELAY -= 3
                cooldown = 0 
                fireratelvl += 1
                score -= 200
                CASH_SOUND.play()


        player.draw()
        player.update()
        bullet_group.update()
        items_group.update()
        bullet_group.draw(screen)
        items_group.draw(screen)
        
        for zombie in zombie_group:
            zombie.ai()
            zombie.update()
            zombie.draw()

        if player.alive:
            if player.hp == 0:
                player.alive = False

            screen_scroll = player.move(moving_left, moving_right)
            #shoot bullets
            if shooting and shot_time <= 0:
                bullet = Bullet(player.rect.centerx + (0.8 * player.rect.size[0] * player.direction), player.rect.centery, player.direction)
                bullet_group.add(bullet)
                shot_time = SHOT_DELAY
                SHOOT_SOUND.play()
                player.img = False

            if pg.sprite.spritecollide(player, zombie_group, False):
                if iFrame > 200:
                    player.hp -= 5
                    iFrame = 0
                    HURT_SOUND.play()
                    screen.fill(RED)

        ########################  
        ######  CONTROLS ####### 
        ########################   


    for event in pg.event.get():
        #quit game
        if event.type == pg.QUIT:
            running = False
        #keyboard presses
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:     #move left when a is pressed
                moving_left = True
            if event.key == pg.K_d:     #move right when d is pressed
                moving_right = True
            if event.key == pg.K_SPACE and player.alive and player.airborne == False:
                player.jump = True
            if event.key == pg.K_w and player.alive and player.airborne == False:
                player.jump = True      #jump when space or w is pressed
            if event.key == pg.K_e:
                shooting = True 

        #keyboard button released

        #updates the direction you are travelling and ignores old direction
        if event.type == pg.KEYUP:
            if event.key == pg.K_a:
                moving_left = False
                gameisplaying = True
            if event.key == pg.K_d:
                moving_right = False
            if event.key == pg.K_r and wavestart == False and gameisplaying == True:             
                wavenumber += 1
                wavestart = True
            if event.key == pg.K_r and wavestart == True:
                HURT_SOUND.play()
            if event.key == pg.K_ESCAPE:        #terminate program
                quit()     
            if event.key == pg.K_e:
                shooting = False    
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                shooting = True   
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                shooting = False  
    pg.display.update()

pg.quit()
