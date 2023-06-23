import pygame

class Car():
    def __init__(self, playerId, imgID, x, y, obsL_x, obsR_x, obsL_img, obsR_img):
        self.imgID = imgID
        self.x = x
        self.y = y
        self.vel = 20
        self.playerId = playerId
        self.activePlayers = 0
        self.color = 'white'
        self.rect = (x,y,0,0)
        self.nickname = ''
        self.score = 0
        self.chatInput = None
        self.active = 0
        self.messages = []
        self.obsL_x = obsL_x
        self.obsR_x = obsR_x
        self.obsL_img = obsL_img
        self.obsR_img = obsR_img
        self.obs_y = -100
        self.reconnected = 0
        self.time = 0
        self.ready = False
        self.finish = False
        self.obsOnScreenL = []
        self.obsOnScreenR = []
        self.appear = True
        self.winner = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        # win.blit(self.img, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel*0.1
            # self.obs_y += 15*1.2

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.x = self.x
        self.y = self.y
        self.playerId = self.playerId
        self.rect = (self.x, self.y,0, 0)
        self.obs_y = self.obs_y

    def bounce(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x, self.y = (73,self.y)

        if keys[pygame.K_RIGHT]:
            self.x, self.y = (620,self.y)

    def boundary(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y<210:
            self.y = 75
        if keys[pygame.K_DOWN] and self.y > 210:
            self.y = 400
