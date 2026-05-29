# finished space shooter game
from pygame import *
from random import randint
from time import time as timer

# init
init()
mixer.init()
font.init()

# music
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# sound effect
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.5)

# images
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"

# window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# FPS
clock = time.Clock()
FPS = 60

# statistics
score = 0
lost = 0
lives = 3

goal = 20
max_lost = 10
finish = False
game_started = False
game_result = ""

# reload variables
num_fire = 0
rel_time = False
last_time = 0

# sound variable
sound_on = True

# fonts
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Arial', 45)

win_text = font1.render("YOU WIN!", True, (255, 255, 255))
lose_text = font1.render("YOU LOSE!", True, (180, 0, 0))
title_text = font1.render("SPACE SHOOTER", True, (255, 255, 255))
start_text = font3.render("Press S to start", True, (255, 255, 255))
restart_text = font2.render("Press R to restart", True, (255, 255, 255))
controls_text = font2.render("SPACE: UFO | A: Asteroid | B: Big bullet | M: Sound", True, (255, 255, 255))

# base class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # draw sprite on screen
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# player
class Player(GameSprite):
    # move player left and right
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # normal bullet for UFOs
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 7, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

    # bullet for asteroids
    def asteroid_fire(self):
        asteroid_bullet = AsteroidBullet(img_bullet, self.rect.centerx - 10, self.rect.top, 20, 30, 18)
        asteroid_bullets.add(asteroid_bullet)

    # big special bullet
    def big_fire(self):
        big_bullet = BigBullet(img_bullet, self.rect.centerx - 35, self.rect.top, 70, 90, 25)
        big_bullets.add(big_bullet)

# enemy
class Enemy(GameSprite):
    # move enemy down
    def update(self):
        global lost

        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = randint(-100, -40)
            self.speed = randint(1, 5)
            lost += 1

# asteroid
class Asteroid(GameSprite):
    # move asteroid down
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = randint(-100, -40)
            self.speed = randint(1, 4)

# normal bullet
class Bullet(GameSprite):
    # move bullet up
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

# asteroid bullet
class AsteroidBullet(GameSprite):
    # move asteroid bullet up
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

# big bullet
class BigBullet(GameSprite):
    # move big bullet up
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

# create one enemy
def create_enemy():
    monster = Enemy(
        img_enemy,
        randint(80, win_width - 80),
        randint(-100, -40),
        80,
        50,
        randint(1, 5)
    )
    monsters.add(monster)

# create one asteroid
def create_asteroid():
    asteroid = Asteroid(
        img_ast,
        randint(80, win_width - 80),
        randint(-100, -40),
        80,
        50,
        randint(1, 4)
    )
    asteroids.add(asteroid)

# restart the game
def restart_game():
    global score, lost, lives, finish, game_result
    global num_fire, rel_time, last_time, game_started

    score = 0
    lost = 0
    lives = 3
    finish = False
    game_started = True
    game_result = ""

    num_fire = 0
    rel_time = False
    last_time = 0

    bullets.empty()
    asteroid_bullets.empty()
    big_bullets.empty()
    monsters.empty()
    asteroids.empty()

    ship.rect.x = 5
    ship.rect.y = win_height - 100

    for i in range(5):
        create_enemy()

    for i in range(3):
        create_asteroid()

# shoot function with reload
def can_shoot():
    global num_fire, rel_time, last_time

    if num_fire < 5 and rel_time == False:
        num_fire += 1
        return True

    if num_fire >= 5 and rel_time == False:
        last_time = timer()
        rel_time = True

    return False

# create player
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# create groups
monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()
asteroid_bullets = sprite.Group()
big_bullets = sprite.Group()

# create enemies
for i in range(5):
    create_enemy()

# create asteroids
for i in range(3):
    create_asteroid()

# game loop
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_s and game_started == False:
                game_started = True

            if e.key == K_r and finish == True:
                restart_game()

            if e.key == K_m:
                sound_on = not sound_on

                if sound_on == True:
                    mixer.music.unpause()
                else:
                    mixer.music.pause()

            if game_started == True and finish == False:
                if e.key == K_SPACE:
                    if can_shoot():
                        if sound_on == True:
                            fire_sound.play()
                        ship.fire()

                if e.key == K_a:
                    if can_shoot():
                        if sound_on == True:
                            fire_sound.play()
                        ship.asteroid_fire()

                if e.key == K_b:
                    if can_shoot():
                        if sound_on == True:
                            fire_sound.play()
                        ship.big_fire()

    if game_started == False:
        window.blit(background, (0, 0))

        # main menu text
        window.blit(title_text, (115, 140))
        window.blit(start_text, (240, 230))
        window.blit(controls_text, (50, 300))

        if sound_on == True:
            sound_text = font2.render("Sound: ON", True, (255, 255, 255))
        else:
            sound_text = font2.render("Sound: OFF", True, (255, 255, 255))

        window.blit(sound_text, (10, 460))

    elif finish == False:
        window.blit(background, (0, 0))

        # update sprites
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        asteroid_bullets.update()
        big_bullets.update()

        # reload timer
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload_text = font2.render("Wait, reload...", True, (150, 0, 0))
                window.blit(reload_text, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        # normal bullets destroy UFOs
        collisions = sprite.groupcollide(monsters, bullets, True, True)

        for collision in collisions:
            score += 1
            create_enemy()

        # asteroid bullets destroy asteroids
        asteroid_collisions = sprite.groupcollide(asteroids, asteroid_bullets, True, True)

        for collision in asteroid_collisions:
            create_asteroid()

        # big bullets destroy UFOs
        big_enemy_collisions = sprite.groupcollide(monsters, big_bullets, True, True)

        for collision in big_enemy_collisions:
            score += 1
            create_enemy()

        # big bullets destroy asteroids
        big_asteroid_collisions = sprite.groupcollide(asteroids, big_bullets, True, True)

        for collision in big_asteroid_collisions:
            create_asteroid()

        # player loses life when touching UFO
        player_hits = sprite.spritecollide(ship, monsters, True)

        for hit in player_hits:
            lives -= 1
            create_enemy()

        # player loses life when touching asteroid
        asteroid_hits = sprite.spritecollide(ship, asteroids, True)

        for hit in asteroid_hits:
            lives -= 1
            create_asteroid()

        # draw sprites
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        asteroid_bullets.draw(window)
        big_bullets.draw(window)

        # show score
        text_score = font2.render("Score: " + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 20))

        # show missed enemies
        text_lost = font2.render("Missed: " + str(lost), True, (255, 255, 255))
        window.blit(text_lost, (10, 50))

        # show lives
        text_lives = font2.render("Lives: " + str(lives), True, (255, 255, 255))
        window.blit(text_lives, (win_width - 130, 20))

        # show sound status
        if sound_on == True:
            sound_text = font2.render("Sound: ON", True, (255, 255, 255))
        else:
            sound_text = font2.render("Sound: OFF", True, (255, 255, 255))

        window.blit(sound_text, (win_width - 130, 50))

        # victory
        if score >= goal:
            finish = True
            game_result = "win"

        # defeat
        if lost >= max_lost or lives <= 0:
            finish = True
            game_result = "lose"

    else:
        window.blit(background, (0, 0))

        # show final result
        if game_result == "win":
            window.blit(win_text, (200, 200))
        else:
            window.blit(lose_text, (200, 200))

        window.blit(restart_text, (250, 280))

        final_score = font2.render("Final score: " + str(score), True, (255, 255, 255))
        window.blit(final_score, (260, 330))

    display.update()
    clock.tick(FPS)