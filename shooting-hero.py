import pygame as p

p.init()

win = p.display.set_mode((500, 480))
p.display.set_caption('First game')
walkRight = [p.image.load('files/R1.png'), p.image.load('files/R2.png'), p.image.load('files/R3.png'),
             p.image.load('files/R4.png'), p.image.load('files/R5.png'), p.image.load('files/R6.png'),
             p.image.load('files/R7.png'), p.image.load('files/R8.png'), p.image.load('files/R9.png')]
walkLeft = [p.image.load('files/L1.png'), p.image.load('files/L2.png'), p.image.load('files/L3.png'),
            p.image.load('files/L4.png'), p.image.load('files/L5.png'), p.image.load('files/L6.png'),
            p.image.load('files/L7.png'), p.image.load('files/L8.png'), p.image.load('files/L9.png')]

bg = p.image.load('files/bg.jpg')
char = p.image.load('files/standing.png')

clock = p.time.Clock()

bulletSound = p.mixer.Sound('files\Game_bullet.mp3')
hitSound = p.mixer.Sound('files\Game_hit.mp3')

music = p.mixer.music.load('files/music.mp3')
p.mixer.music.play(-1)
score = 0


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # p.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump=False
        self.jumpCount=10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = p.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        p.display.update()
        i = 0
        while i < 300:
            p.time.delay(10)
            i += 1

            for event in p.event.get():
                if event.type == p.QUIT:
                    i = 301
                    p.quit()


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        p.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    walkRight = [p.image.load('files/R1E.png'), p.image.load('files/R2E.png'), p.image.load('files/R3E.png'),
                 p.image.load('files/R4E.png'), p.image.load('files/R5E.png'), p.image.load('files/R6E.png'),
                 p.image.load('files/R7E.png'), p.image.load('files/R8E.png'), p.image.load('files/R9E.png'),
                 p.image.load('files/R10E.png'), p.image.load('files/R11E.png')]
    walkLeft = [p.image.load('files/L1E.png'), p.image.load('files/L2E.png'), p.image.load('files/L3E.png'),
                p.image.load('files/L4E.png'), p.image.load('files/L5E.png'), p.image.load('files/L6E.png'),
                p.image.load('files/L7E.png'), p.image.load('files/L8E.png'), p.image.load('files/L9E.png'),
                p.image.load('files/L10E.png'), p.image.load('files/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            p.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            p.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((5 * (10 - self.health))), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # p.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: %d' % score, 1, (0, 0, 0))
    win.blit(text, (350, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    p.display.update()


# mainloop
font = p.font.SysFont('comicsans', 30, True)
man = Player(300, 410, 64, 64)
goblin = Enemy(100, 415, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)
    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[
                2]:
                man.hit()
                score -= 5
    else:
        goblin = Enemy(100, 415, 64, 64, 450)


    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[
                1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                        goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        else:
            goblin = Enemy(100, 415, 64, 64, 450)

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = p.key.get_pressed()

    if keys[p.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(
                Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))

        shootLoop = 1

    if keys[p.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[p.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[p.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1

            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

p.quit()
