
import sys, pygame
import pygame.gfxdraw
import time, random
import threading

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BACKGROUND_COLOR = (46, 52, 64)

SCORE_KILL_ALIEN = 100

SCORE_BOARD_TEXT_COLOR = (255, 255, 255)
SCORE_BOARD_FONT_SIZE = 24
SCORE_BOARD_XOFFSET = 10
SCORE_BOARD_YOFFSET = 10

USER_WIDTH=50
USER_HEIGHT=15

USER_X_MOVE_INCR = 5

USER_COLOR = (25, 225, 25)

BULLET_COLOR = (255, 255, 255)
BULLET_WIDTH = 2
BULLET_HEIGHT = 6
BULL_Y_MOVE_INCR = 10

ALIEN_COLOR = (25, 225, 25)

SCALING_FACTOR = 3
ALIEN_WIDTH=33
ALIEN_HEIGHT=24
ALIEN_MOVE_AMOUNT = 12
ALIEN_NUM_OF_SHIFTS_X = 8

FPS = 60
fpsClock = pygame.time.Clock()

class Utils:

    @staticmethod
    def getMiddlePosition():
        return [int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)]

    @staticmethod
    def getMiddleXPosition():
        return int(SCREEN_WIDTH / 2)

    @staticmethod
    def getMiddleYPosition():
        return int(SCREEN_HEIGHT / 2)

    @staticmethod
    def getRandomDirection():
        directions = ['right', 'left', 'down', 'up']
        initialDirection = directions[random.randint(0, 3)]
        return initialDirection

    @staticmethod
    def sign(n):
        if n<0:
            return -1
        elif n>0:
            return 1
        else: 0

class Sound:


    @staticmethod
    def init():
        Sound.SND_LASER_SHOT = pygame.mixer.Sound("lasershot.mp3")
        Sound.SND_INTRO = pygame.mixer.Sound("intro.wav")
        Sound.SND_MONSTER_DEATH = pygame.mixer.Sound("monsterdeath.mp3")

    @staticmethod
    def playLaserShot():
        pygame.mixer.Sound.play(Sound.SND_LASER_SHOT)
        pygame.mixer.music.stop()

    @staticmethod
    def playMonsterDeath():
        pygame.mixer.Sound.play(Sound.SND_MONSTER_DEATH)
        pygame.mixer.music.stop()

    @staticmethod
    def playIntro():
        pygame.mixer.Sound.play(Sound.SND_INTRO)
        pygame.mixer.music.stop()


class Scoreboard:

    @staticmethod
    def init():
        Scoreboard.score = 0
        Scoreboard.text = "Score: " + str(Scoreboard.score)

    @staticmethod
    def addScore(scoreAmount):
        Scoreboard.score += scoreAmount
        Scoreboard.text = "Score: " + str(Scoreboard.score)



class Renderer:

    @staticmethod
    def __drawBackground():
        screen.fill(BACKGROUND_COLOR)

    @staticmethod
    def __drawScoreboard():
        font = pygame.font.SysFont(None, SCORE_BOARD_FONT_SIZE)
        img = font.render(Scoreboard.text, True, SCORE_BOARD_TEXT_COLOR)
        screen.blit(img, (SCORE_BOARD_XOFFSET, SCORE_BOARD_YOFFSET))

    @staticmethod
    def __drawUserShip():
        user = User.user
        pygame.draw.rect(screen, USER_COLOR, pygame.Rect(user.position[0], user.position[1], user.width, user.height))
        pygame.draw.rect(screen, USER_COLOR, pygame.Rect(user.position[0]+user.width/2 - (user.width/5)/2,
                                                         user.position[1]-user.height/1.5, user.width/5, user.height/1.5))

    @staticmethod
    def __drawBullets():
        bullets = Bullet.bullets
        for bullet in bullets:
            bulletRect = pygame.Rect(bullet.position[0], bullet.position[1], bullet.width, bullet.height)
            pygame.draw.rect(screen, BULLET_COLOR, bulletRect)

    @staticmethod
    def __drawAliens():
        aliens = Alien.aliens
        for alien in aliens:
            tempAlienSurface = pygame.surface.Surface((11, 8))
            tempAlienSurface.fill(BACKGROUND_COLOR)
            for i in range(len(alien.pixels)):
                for j in range(len(alien.pixels[i])):
                    if alien.pixels[i][j] == 1:
                        pygame.gfxdraw.pixel(tempAlienSurface, j, i, ALIEN_COLOR)
            tempAlienSurface = pygame.transform.scale(tempAlienSurface, (11*SCALING_FACTOR, 8*SCALING_FACTOR))
            screen.blit(tempAlienSurface, (alien.position[0], alien.position[1]))

    @staticmethod
    def draw():

        Renderer.__drawBackground()
        Renderer.__drawBullets()
        Renderer.__drawUserShip()
        Renderer.__drawAliens()
        Renderer.__drawScoreboard()

class Sprite:
    def __init__(self, pos=[0,0], width=0, height=0):
        self.position = pos
        self.width = width
        self.height = height

    def top(self):
        self.position[1]

    def bottom(self):
        self.position[1] + self.height

    def left(self):
        self.position[0]

    def right(self):
        self.position[0] + self.height

    def isColliding(self, sprite):
        if sprite.position[0] + sprite.width >= self.position[0] and \
            sprite.position[1] + sprite.height >= self.position[1] and \
            sprite.position[0] <= self.position[0] + self.width and \
            sprite.position[1] <= self.position[1] + self.height:
            return True
        return False

class Alien(Sprite):
    def __init__(self, pos=[0,0]):
        Sprite.__init__(self, [pos[0],pos[1]], ALIEN_WIDTH, ALIEN_HEIGHT)
        self.xMoveIncr = USER_X_MOVE_INCR
        self.direction = 'none'
        self.pixels = [[0,0,1,0,0,0,0,0,1,0,0],
                       [0,0,0,1,0,0,0,1,0,0,0],
                       [0,0,1,1,1,1,1,1,1,0,0],
                       [0,1,1,0,1,1,1,0,1,1,0],
                       [1,1,1,1,1,1,1,1,1,1,1],
                       [1,0,1,1,1,1,1,1,1,0,1],
                       [1,0,1,0,0,0,0,0,1,0,1],
                       [0,0,0,1,1,0,1,1,0,0,0]]

    def shootBullet(self):
        bullet = AlienBullet(self.position[0]+self.width/2, self.position[1]+self.height/2)





class Bullet(Sprite):
    def __init__(self, pos=[0,0], dir='up'):
        Sprite.__init__(self, [pos[0],pos[1]], BULLET_WIDTH, BULLET_HEIGHT)
        self.yMoveIncr = BULL_Y_MOVE_INCR
        self.direction = dir

    def update(self):
        if self.direction == 'up':
            self.position[1] -= self.yMoveIncr
        elif self.direction == 'down':
            self.position[1] += self.yMoveIncr


class AlienBullet(Bullet):
    def __init__(self, pos=[0,0]):
        Sprite.__init__(self, [pos[0],pos[1]], BULLET_WIDTH, BULLET_HEIGHT)
        self.yMoveIncr = BULL_Y_MOVE_INCR
        self.direction = 'down'

class User(Sprite):

    def __init__(self, pos=[0,0]):
        Sprite.__init__(self, [pos[0],pos[1]], USER_WIDTH, USER_HEIGHT)
        self.xMoveIncr = USER_X_MOVE_INCR
        self.direction = 'none'

    def update(self):
        if self.direction == 'left':
            self.position[0] -= self.xMoveIncr
        elif self.direction == 'right':
            self.position[0] += self.xMoveIncr

class GameWorld:

    @staticmethod
    def __generateAliens():

        numInRow = 9
        numInColumn = 4
        rowSkip = 50
        columnSkip = 75

        Alien.aliens = []
        aliens = Alien.aliens

        for i in range(0, numInColumn):
            for j in range(0, numInRow):
                aliens.append(Alien(((j+1)*columnSkip, (i+1)*rowSkip)))



    @staticmethod
    def init():

        Sound.init()
        Scoreboard.init()

        Alien.allMovement = 'right'
        Alien.previousMovement = 'none'

        Alien.numOfShifts = ALIEN_NUM_OF_SHIFTS_X / 2
        Alien.shifts = 0

        Bullet.bullets = []
        User.user = User((Utils.getMiddleXPosition()-USER_WIDTH/2, SCREEN_HEIGHT-USER_HEIGHT*2))

        GameWorld.__generateAliens()

        Sound.playIntro()

    @staticmethod
    def reset():

        Scoreboard.init()


    @staticmethod
    def quit():
        return None

    @staticmethod
    def __update_UserBoundariesCheck():
        user = User.user
        if user.position[0] <= 0:
            user.position[0] = 1
        elif user.position[0] + user.width >= SCREEN_WIDTH:
            user.position[0] = SCREEN_WIDTH - user.width

    @staticmethod
    def __update_BulletBoundariesCheck():
        bullets = Bullet.bullets
        for bullet in bullets:
            if bullet.position[1] + bullet.height <= 0:
                bullets.remove(bullet)
                continue

    @staticmethod
    def __update_BulletHitsAliensCheck():
        bullets = Bullet.bullets
        aliens = Alien.aliens
        for bullet in bullets:
            for alien in aliens:
                if alien.isColliding(bullet):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    Scoreboard.addScore(SCORE_KILL_ALIEN)
                    Sound.playMonsterDeath()
                    continue


    @staticmethod
    def __update_Bullets():
        bullets = Bullet.bullets
        for bullet in bullets:
            bullet.update()

    @staticmethod
    def createUserBullet():
        bullets = Bullet.bullets
        bulletPos = ((user.position[0] + user.width / 2) - 1, user.position[1])
        bullets.append(Bullet(bulletPos))
        Sound.playLaserShot()

    @staticmethod
    def updateAliens():

        aliens = Alien.aliens
        allMovement = Alien.allMovement
        for alien in aliens:
            if allMovement == 'right':
                alien.position[0] += ALIEN_MOVE_AMOUNT
            elif allMovement == 'left':
                alien.position[0] -= ALIEN_MOVE_AMOUNT
            elif allMovement == 'down':
                alien.position[1] += ALIEN_MOVE_AMOUNT

        Alien.shifts += 1
        if Alien.shifts == Alien.numOfShifts:
            Alien.shifts = 0
            if allMovement == 'right':
                Alien.allMovement = 'down'
                Alien.previousMovement = 'right'
                Alien.numOfShifts = 2
            elif allMovement == 'left':
                Alien.allMovement = 'down'
                Alien.previousMovement = 'left'
                Alien.numOfShifts = 2
            elif allMovement == 'down' and Alien.previousMovement == 'right':
                Alien.allMovement = 'left'
                Alien.numOfShifts = ALIEN_NUM_OF_SHIFTS_X
            elif allMovement == 'down' and Alien.previousMovement == 'left':
                Alien.allMovement = 'right'
                Alien.numOfShifts = ALIEN_NUM_OF_SHIFTS_X

    @staticmethod
    def update():
        user = User.user

        user.update()
        GameWorld.__update_Bullets()

        GameWorld.__update_BulletBoundariesCheck()
        GameWorld.__update_BulletHitsAliensCheck()
        GameWorld.__update_UserBoundariesCheck()


if __name__ == '__main__':

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Space Invaders")

    prev_time = time.time()

    GameWorld.init()

    running = True
    spacePressed = False
    reloaded = True

    reloadedTimerEvent = pygame.USEREVENT + 1
    alienMoveTimerEvent = pygame.USEREVENT + 2
    pygame.time.set_timer(alienMoveTimerEvent, 1000, 9999999)


    while running:

        user = User.user

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == reloadedTimerEvent:
                reloaded = True
            elif event.type == alienMoveTimerEvent:
                GameWorld.updateAliens()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not spacePressed and reloaded:
            spacePressed = True
            reloaded = False
            pygame.time.set_timer(reloadedTimerEvent, 1000, 1)
            GameWorld.createUserBullet()
        elif not keys[pygame.K_SPACE]:
            spacePressed = False


        if keys[pygame.K_LEFT] and user.direction is not 'right':
            user.direction = 'left'
        elif keys[pygame.K_RIGHT] and user.direction is not 'left':
            user.direction = 'right'
        else:
            user.direction = 'none'

        GameWorld.update()
        Renderer.draw()

        pygame.display.flip()
        fpsClock.tick(FPS)

    GameWorld.quit()
