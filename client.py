from pygame.locals import *
import time
import pygame
from pygame import mixer
import socket
import pickle


# ----------------------------------------------Client Networking-------------------------------------------------------
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "16.170.251.198"
        self.port = 6666
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)





pygame.init()
mixer.init()



def scale_image(img, factor):
    size = round(img.get_width()* factor),round(img.get_height()* factor)
    return pygame.transform.scale(img,size)

# Sounds
# mixer.music.load('music/background_music.ogg')
# mixer.music.play(-1)
car_collide = mixer.music.load('music/car_collide.ogg')



# Cars
blueCarImg = pygame.image.load("images/blueCar.png")
greenCarImg = pygame.image.load("images/greenCar.png")
redCarImg = pygame.image.load("images/redCar.png")
pinkCarImg = pygame.image.load("images/pinkCar.png")
greyCarImg = pygame.image.load("images/greyCar.png")


# Obstacles
obsBus = pygame.image.load("images/obsBus.png")
obsGreen = pygame.image.load("images/obsGreen.png")
obsWhite = pygame.image.load("images/obsWhite.png")
obsYellow = pygame.image.load("images/obsYellow.png")


borders = scale_image(pygame.image.load("images/borders.png"),1.001)
borders_mask = pygame.mask.from_surface(borders)

borderY = pygame.image.load("images/borderY.png")
borderY_mask = pygame.mask.from_surface(borderY)

startPage = scale_image(pygame.image.load("images/startPage.png"),1.005)
readyPage = scale_image(pygame.image.load("images/readyPage.png"), 1)
window = pygame.image.load("images/window.png")
road = scale_image(pygame.image.load("images/road.png"),1.005)

finishLine = scale_image(pygame.image.load("images/finishLine.png"),1.1)

# Chat text box
chat = pygame.image.load("images/chat.png")
text_area_width = 280
text_area_height = 50
text_area_background_color = (128, 0, 128)  # Purple
border_width = 2
border_radius = 10
text_area_radius = 8  # Radius for the text area background (inner radius)
border_color = (255, 255, 255)  # White
font = pygame.font.Font(None, 26)
text_area_font = pygame.font.Font(None, 27)
text_area_font_color ='white'

button_normal = pygame.image.load('images/submit.png')
button_hover = pygame.image.load('images/submit.png')
button_clicked = pygame.image.load('images/submit.png')
button_width = 45
button_height = 45

# Resize the button images
button_normal = pygame.transform.scale(button_normal, (button_width, button_height))
button_hover = pygame.transform.scale(button_hover, (button_width, button_height))
button_clicked = pygame.transform.scale(button_clicked, (button_width, button_height))

messages = []
text_x = 800
text_y = 75

# Set up the button
button_rect = button_normal.get_rect()
button_image = button_normal





width, height = window.get_width(), window.get_height()
win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Client")


# The score to show finish line after
win_score = 50






class ObstaclesLeft():

    img1 = obsWhite
    img2 = obsGreen

    def __init__(self, x, y,speedy,finish,obs):
        self.img = self.img1
        self.x = x
        self.y = y
        self.speedy = speedy
        self.score = 0
        self.obs = obs
        self.finish = finish



    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def update(self,x,obs):
        if self.score > 5:
            self.y = self.y + self.speedy * 2
        else:
            self.y = self.y +self.speedy*1.5


        if self.y > height:
            self.y = 0-self.img.get_height()
            self.x = x
            if self.finish:
                self.score = self.score
            else:
                self.score = self.score + 2
            self.obs = obs
            if self.obs == 0:
                self.img = self.img1
            elif self.obs == 1:
                self.img = self.img2
            elif self.obs == 2:
                self.img = self.img1
            elif self.obs == 3:
                self.img = self.img2

class ObstaclesRight():

    img1 = obsBus
    img2 = obsYellow

    def __init__(self, x, y,speedy,obs):
        self.img = self.img1
        self.x = x
        self.y = y
        self.speedy = speedy
        self.score = 0
        self.obs = obs


    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def update(self, x,obs):
        if self.score >5:
            self.y = self.y + self.speedy * 2
        else:
            self.y = self.y +self.speedy*1.5


        if self.y > height:
            self.y = 0-self.img.get_height()
            self.x = x
            if self.score >= win_score:
                self.score = self.score
            else:
                self.score = self.score+2
            self.obs = obs
            if self.obs == 0:
                self.img = self.img1
            elif self.obs == 1:
                self.img = self.img2
            elif self.obs == 2:
                self.img = self.img1
            elif self.obs == 3:
                self.img = self.img2

class FinishLine():
    img = finishLine
    img2 = road

    def __init__(self, x, y,speedy,finish):
        self.img = self.img
        self.x = x
        self.y = y
        self.speedy = speedy
        self.finish = finish

    def draw(self, win,show):
        if show:
            win.blit(self.img, (80, self.y))



    def update(self,show):
        if show:
            self.speedy = self.speedy + 0.3           # 0.3 is the acceleration
            self.y = self.y + min(self.speedy, 15)    # 15 is the max_vel


def game_Info(score,startTime,car,car1,car2,car3,car4):
    font = pygame.font.Font(None,25)

    text = font.render("Completed:  " + str((car.score*100/50))+" %", True, 'white')
    win.blit(text, (107, 5))

    text = font.render("Score: "+str(score),True,'white')
    win.blit(text,(82, height-50))

    text = font.render("Time: " + str(round(time.time()-startTime)) + "s", True, 'white')
    car.time = round(time.time()-startTime)
    win.blit(text, (82, height-20))

    text = font.render("Active Players: " + str(car.activePlayers) , True, 'white')
    win.blit(text, (900, 15))

    lst = [car.score,car1.score,car2.score,car3.score,car4.score]
    lst.sort(reverse=True)

    scores = {car.nickname: [car.score,car.imgID], car1.nickname: [car1.score,car1.imgID], car2.nickname: [car2.score,car2.imgID], car3.nickname: [car3.score,car3.imgID], car4.nickname: [car4.score,car4.imgID]}
    sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1][0], reverse=True))


    x = 880
    y = 400
    scoreFont = pygame.font.Font(None, 32)
    for key, value in sorted_scores.items():
        global carImg
        if value[1] == 0:
            carImg = blueCarImg
        if value[1] == 1:
            carImg = greenCarImg
        if value[1] == 2:
            carImg = redCarImg
        if value[1] == 3:
            carImg = pinkCarImg
        if value[1] == 4:
            carImg = greyCarImg


        if value[0] > 0:
            # global carImg
            win.blit(scale_image(carImg, 0.2), (x - 50, y))
            text = scoreFont.render(str(key) + " score: " + str(value[0]), True, 'white')
            win.blit(text, (x, y))
            y = y + 23

def gameOver(finish,obstacles):
    if not finish:
        font = pygame.font.Font(None, 80)
        text = font.render("Game Over!",True, 'white')
        text_width = text.get_width()
        text_height = text.get_height()
        x = int(width/2 - text_width/2)
        y = int(height/2 - text_height)
        score = "score: "+str(obstacles.score)
        displayScore = font.render(score, True, 'white')
        win.blit(text, (260, y))
        win.blit(displayScore, (300, y+100))
        pygame.display.update()
        time.sleep(2)

def Winner(show,obstacleScore):
    if show:
        font = pygame.font.Font(None, 80)
        text = font.render("YOU WON!",True, 'white')
        text_width = text.get_width()
        text_height = text.get_height()
        x = int(width/2 - text_width/2)
        y = int(height/2 - text_height/2)
        win.blit(startPage, (0, 0))
        win.blit(text, (260, y))
        pygame.display.update()
        time.sleep(2)
        obstacleScore = 0

def bordersCollision(car,mask, x=44, y=-2):
    car_mask = pygame.mask.from_surface(blueCarImg)
    offset = (int(car.x -x), int(car.y - y))
    intersection_point = mask.overlap(car_mask, offset)
    return intersection_point

def chatBox(event, car, inputText, text_input, text_input_render, button_image, button_rect):
    if event.type == KEYDOWN:
        if event.key == pygame.K_TAB:
            car.ready = True
        elif event.key == K_BACKSPACE:
            text_input = text_input[:-1]
        elif event.key == K_RETURN:
            car.chatInput = text_input

            if len(text_input) > 0 and (car.nickname + " : " + car.chatInput) not in messages:
                # Button released
                button_image = button_hover

                messages.append(car.nickname + " : " + text_input)

                message = f"{car.nickname}:{text_input}"

                text_input = ""
        else:
            text_input += event.unicode

        text_input_render = text_area_font.render(text_input, True, text_area_font_color)


    elif event.type == MOUSEBUTTONDOWN:
        if button_rect.collidepoint(event.pos):

            car.chatInput = text_input
            if car.chatInput is not None and len(car.chatInput) > 0:
                last_message = car.nickname + " : " + car.chatInput
                if not messages or last_message != messages[-1]:
                    messages.append(last_message)

                message = f"{inputText}:{text_input}"

                print('Submit button pressed!')
                text_input = ""
        else:
            button_image = button_normal

        text_input_render = text_area_font.render(text_input, True, text_area_font_color)



    return text_input, text_input_render

def drawChatBox(text_input_render, car1, car2, car3, car4, button_image,button_rect):
    global y_offset


    if car1.chatInput != None and (car1.nickname + " : " + car1.chatInput) not in messages and len(car1.chatInput) > 0:
        messages.append(car1.nickname + " : " + car1.chatInput)

    if car2.chatInput != None and (car2.nickname + " : " + car2.chatInput) not in messages and len(car2.chatInput) > 0:
        messages.append(car2.nickname + " : " + car2.chatInput)

    if car3.chatInput != None and (car3.nickname + " : " + car3.chatInput) not in messages and len(car3.chatInput) > 0:
        messages.append(car3.nickname + " : " + car3.chatInput)

    if car4.chatInput != None and (car4.nickname + " : " + car4.chatInput) not in messages and len(car4.chatInput) > 0:
        messages.append(car4.nickname + " : " + car4.chatInput)



    font = pygame.font.Font(None, 27)
    # Create a new text surface with the updated messages
    rendered_messages = [font.render(msg, True, (255, 255, 255)) for msg in messages]
    text_height = sum(surface.get_height() for surface in rendered_messages)
    text_surface = pygame.Surface(
        (width, text_height)).convert_alpha()  # Use convert_alpha() to create a surface with transparency
    text_surface.fill((0, 0, 0, 0))

    print(messages, "de el msgs")
    print(rendered_messages, "de el rendered msgs")

    y_offset = 0
    for surface in rendered_messages:
        if y_offset < 225:
            text_surface.blit(surface, (0, y_offset))
            y_offset += surface.get_height()
            window.blit(chat, (800, 72))
            window.blit(text_surface, (text_x, text_y))
        else:
            y_offset = 0
            window.blit(chat, (800, 72))
            messages.clear()
            window.blit(text_surface, (text_x, text_y))


    text_area_rect = pygame.Rect(810, 325, text_area_width, text_area_height)
    pygame.draw.rect(window, text_area_background_color, text_area_rect,border_radius=text_area_radius)  # Draw the text area rectangle with rounded corners
    pygame.draw.rect(window, border_color, text_area_rect, border_width, border_radius)  # Draw the border
    win.blit(text_input_render, (text_area_rect.x + 5, text_area_rect.y + 5))  # Draw the rendered text
    win.blit(button_image, button_rect)
    pygame.display.update()

def redrawWindow(win,images,car, car1,car2,car3,car4,roadx,roady, obstacle,obstacleR,won,show,startTime,button_image,button_rect):
    for img, pos in images:
        win.blit(img, pos)
    win.blit(borders, [44, -2])
    win.blit(road, [roadx, roady - height])  # minus window height
    win.blit(road, [roadx, roady])
    won.draw(win, show)
    obstacle.draw(win)
    obstacleR.draw(win)
    car.draw(win)
    if car1.active == 1:
        car1.draw(win)
    if car2.active == 1:
        car2.draw(win)
    if car3.active == 1:
        car3.draw(win)
    if car4.active == 1:
        car4.draw(win)


    cars =  [car,car1,car2,car3,car4]
    for c in cars:
        if c.imgID == 0:
            if c.active == 1 and c.appear == True:
                win.blit(blueCarImg, (c.x, c.y))
        if c.imgID == 1:
            if c.active == 1 and c.appear == True:
                win.blit(greenCarImg, (c.x, c.y))
        if c.imgID == 2:
            if c.active == 1 and c.appear == True:
                win.blit(redCarImg, (c.x, c.y))
        if c.imgID == 3:
            if c.active == 1 and c.appear == True:
                win.blit(pinkCarImg, (c.x, c.y))
        if c.imgID == 4:
            if c.active == 1 and c.appear == True:
                win.blit(greyCarImg, (c.x, c.y))

    win.blit(button_image, button_rect)
    game_Info(obstacle.score, startTime, car, car1, car2, car3, car4)
    pygame.display.update()


# In python 0,0 is top left
images = [(borderY,(0,0)),(window,(0,0)),(road,(0,0))]


n = Network()

text_input = ""
text_input_render = text_area_font.render("", True, text_area_font_color)

game_over = False
finish = False


def main(inputText):
    global messages
    global startTime
    global text_input
    global text_input_render
    global game_over
    global finish

    run = True

    roadx = 0
    roady = 0
    car_vel = 15
    road_vel = 12

    obs_x = 0
    obs_img = 0
    obstacle_y = -100

    started = False
    chatOnly = False
    show = False
    ready = False
    finishY = -100
    startTime = 0

    counter = 3  # Counter for countdown
    counter_text_font = pygame.font.Font(None, 60)
    start_text_font = pygame.font.Font(None, 60)

    text_input = ""
    text_input_render = text_area_font.render("", True, text_area_font_color)

    car = n.getP()

    obstacle = ObstaclesLeft(car.obsL_x[obs_x], obstacle_y, road_vel, finish, car.obsL_img[obs_img])
    obstacleR = ObstaclesRight(car.obsR_x[obs_x], obstacle_y, road_vel, car.obsR_img[obs_img])

    # Check if this was a new player
    if car.reconnected == 0:
        car.nickname = inputText
        startTime = time.time()
    else:
        obstacle.score = car.score
        messages = car.messages
        startTime = time.time()-car.time
        if car.finish == True:
            chatOnly = True
            started = True

    if game_over == True:
        startTime = time.time()
        obstacle.score = 0


    won = FinishLine(0, finishY, road_vel, show)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        button_image = button_normal
        button_rect = pygame.Rect(1028, 327, button_width, button_height)


        car.score = obstacle.score


        p2, p3, p4, p5 = n.send(car)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            else:
                # Players can chat while playing
                text_input, text_input_render = chatBox(event, car,inputText, text_input, text_input_render,button_image, button_rect)

        drawChatBox(text_input_render, p2, p3, p4, p5, button_image,button_rect)

        players = [car,p2,p3,p4,p5]
        for p in players:
            p.messages = messages
            if p.winner == True:
                chatOnly = True



        car.activePlayers = p2.activePlayers


        while not started:
            font = pygame.font.Font(None, 50)
            if car.activePlayers <= 2:
                text = font.render("Waiting for opponents.. ", True, 'white')
            else:
                text = font.render("You May Start Now! ", True, 'white')
            win.blit(window,(0,0))
            win.blit(readyPage, (0, 0))
            win.blit(text, (200, (height / 2) - 200))

            # Check if this was a new player
            if car.reconnected == 0:
                car.nickname = inputText

            players = [car, p2, p3, p4, p5]

            for p in players:
                if p.ready == True and car.activePlayers >= 2:
                    ready = True

            p2, p3, p4, p5 = n.send(car)
            car.activePlayers = p2.activePlayers
            text = pygame.font.Font(None, 25).render("Active Players: " + str(car.activePlayers), True, 'white')
            win.blit(text, (900, 15))
            urCar = pygame.font.Font(None, 25).render("this is your car", True, 'white')
            win.blit(urCar, (925, 465))

            if car.imgID == 0:
                win.blit(blueCarImg,(800,420))
                text = pygame.font.Font(None, 25).render("Hello! "+ str(car.nickname), True, 'white')
                win.blit(text, (950, 445))
            elif car.imgID == 1:
                win.blit(greenCarImg, (800,420))
                text = pygame.font.Font(None, 25).render("Hello! " + str(car.nickname), True, 'white')
                win.blit(text, (950, 445))
            elif car.imgID == 2:
                win.blit(redCarImg, (800,420))
                text = pygame.font.Font(None, 25).render("Hello! " + str(car.nickname), True, 'white')
                win.blit(text, (950, 445))
            elif car.imgID == 3:
                win.blit(pinkCarImg, (800,420))
                text = pygame.font.Font(None, 25).render("Hello! " + str(car.nickname), True, 'white')
                win.blit(text, (950, 445))
            elif car.imgID == 4:
                win.blit(greyCarImg, (800,420))
                text = pygame.font.Font(None, 25).render("Hello! " + str(car.nickname), True, 'white')
                win.blit(text, (950, 445))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                else:
                    # Players can chat before they play the game
                    text_input, text_input_render = chatBox(event, car, inputText, text_input, text_input_render, button_image, button_rect)

            drawChatBox(text_input_render, p2, p3, p4, p5, button_image,button_rect)

            for p in players:
                p.messages = messages

            while counter > 0 and ready == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.QUIT()
                # Draw the counter
                counter_text = font.render(str(counter), True, 'white')
                counter_rect = counter_text.get_rect(center=(400 , 150))
                car.active = 1
                redrawWindow(win, images, car, p2, p3, p4, p5, roadx, roady, obstacle, obstacleR, won, show, startTime,button_image, button_rect)
                win.blit(counter_text, counter_rect)
                pygame.display.update()
                pygame.time.delay(1000)  # 1-second delay
                counter -= 1
                started = True


        car.move()

        # Same obstacles for all players
        obs_x += 1
        obs_img += 1
        if obs_x == len(car.obsL_x):
            obs_x = 0
            obs_img = 0
        obstacle.update(car.obsL_x[obs_x], car.obsL_img[obs_img])
        obstacleR.update(car.obsR_x[obs_x], car.obsR_img[obs_img])


        won.update(show)
        redrawWindow(win, images, car, p2, p3,p4, p5, roadx, roady, obstacle, obstacleR, won, show, startTime,button_image, button_rect)

        keys = pygame.key.get_pressed()
        if obstacle.score < 2:
            roady = roady + road_vel * 1.6
            if (roady == height) or (roady > height):
                roady = 0
        else:
            if keys[pygame.K_UP]:
                roady = roady + road_vel * 2.3
            else:
                roady = roady + road_vel * 1.7
            if (roady == height) or (roady > height):
                roady = 0


        if bordersCollision(car,borders_mask) != None:
            car.bounce()
        if bordersCollision(car,borderY_mask) != None:
            car.boundary()

        if ((obstacle.x - car.x) < 55 and abs(car.y - obstacle.y) <= 124):
            if ((car.x - obstacle.x) < 55 and abs(car.y - obstacle.y) <= 124):
                game_over = True
                car.appear = False
                car.active = 0
                car.finish = True
                started = False
                chatOnly = True
                gameOver(finish, obstacle)
        if ((obstacleR.x - car.x) < 55 and abs(car.y - obstacleR.y) <= 124):
            if ((car.x - obstacleR.x) < 55 and abs(car.y - obstacleR.y) <= 124):
                game_over = True
                car.appear = False
                car.active = 0
                car.finish = True
                started = False
                chatOnly = True
                gameOver(finish, obstacle)

        if obstacle.score >= win_score:
            show = True
            if abs(won.y - car.y) < won.img.get_height() / 11:
                car.active = 0
                car.winner = True
                car.appear = False
                started = False
                chatOnly = True
                Winner(show, obstacle.score)



        if ((car.x - p2.x) < 55 and abs(p2.y - car.y) <= 124):
            if ((p2.x - car.x) < 55 and abs(p2.y - car.y) <= 124):
                global flag2
                flag2 = True
                if p2.active == 1 and flag2 is True and p2.appear == True:
                    car_collide = mixer.Sound('music/car_collide.ogg')
                    car_collide.play()
                    obstacle.score -= 1
                    flag2 = False
                    print("collided")

        if ((car.x - p3.x) < 55 and abs(p3.y - car.y) <= 124):
            if ((p3.x - car.x) < 55 and abs(p3.y - car.y) <= 124):
                global flag3
                flag3 = True
                if p3.active == 1 and flag3 is True and p3.appear == True:
                    car_collide = mixer.Sound('music/car_collide.ogg')
                    car_collide.play()
                    obstacle.score -= 1
                    flag3 = False
                    print("collided")

        if ((car.x - p4.x) < 55 and abs(p4.y - car.y) <= 124):
            if ((p4.x - car.x) < 55 and abs(p4.y - car.y) <= 124):
                global flag4
                flag4 = True
                if p4.active == 1 and flag4 is True and p4.appear == True:
                    car_collide = mixer.Sound('music/car_collide.ogg')
                    car_collide.play()
                    obstacle.score -= 1
                    flag4 = False
                    print("collided")

        if ((car.x - p5.x) < 55 and abs(p5.y - car.y) <= 124):
            if ((p5.x - car.x) < 55 and abs(p5.y - car.y) <= 124):
                global flag5
                flag5 = True
                if p5.active == 1 and flag5 is True and p5.appear == True:
                    car_collide = mixer.Sound('music/car_collide.ogg')
                    car_collide.play()
                    obstacle.score -= 1
                    flag5 = False
                    print("collided")

        players = [car, p2, p3, p4, p5]
        for p in players:
            if p.score >= 54:
                p.winner = True
                chatOnly = True

        while chatOnly:
            car.appear = False
            font = pygame.font.Font(None, 50)
            text = font.render("YOUR SCORE: "+str(car.score), True, 'white')
            percentage = font.render("YOU COMPLETED " + str(min(100,car.score*100/50))+" %", True, 'white')
            win.blit(window,(0,0))
            win.blit(readyPage, (0, 0))
            win.blit(text, (220, 100 ))
            win.blit(percentage, (160, 200))

            # Check if this was a new player
            if car.reconnected == 0:
                car.nickname = inputText

            p2, p3, p4, p5 = n.send(car)
            car.activePlayers = p2.activePlayers
            text = pygame.font.Font(None, 25).render("Active Players: " + str(car.activePlayers), True, 'white')
            win.blit(text, (900, 15))
            urCar = pygame.font.Font(None, 25).render("this is your car", True, 'white')
            win.blit(urCar, (925, 465))

            if car.imgID == 0:
                win.blit(blueCarImg,(800,420))
                text = pygame.font.Font(None, 25).render("Hello! "+ str(car.nickname), True, 'white')
                win.blit(text, (950, 445))
            elif car.imgID == 1:
                win.blit(greenCarImg, (800,420))
                text = pygame.font.Font(None, 25).render("Hello! " + str(car.nickname), True, 'white')
                win.blit(text, (950, 445))
            elif car.imgID == 2:
                win.blit(redCarImg, (800,420))
                text = pygame.font.Font(None, 25).render("Hello! " + str(car.nickname), True, 'white')
                win.blit(text, (950, 445))
            elif car.imgID == 3:
                win.blit(pinkCarImg, (800,420))
                text = pygame.font.Font(None, 25).render("Hello! " + str(car.nickname), True, 'white')
                win.blit(text, (950, 445))
            elif car.imgID == 4:
                win.blit(greyCarImg, (800,420))
                text = pygame.font.Font(None, 25).render("Hello! " + str(car.nickname), True, 'white')
                win.blit(text, (950, 445))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                else:
                    # Players can chat after they play the game
                    text_input, text_input_render = chatBox(event, car, inputText, text_input, text_input_render, button_image, button_rect)
            drawChatBox(text_input_render, p2, p3, p4, p5, button_image,button_rect)
            players = [car, p2, p3, p4, p5]
            for p in players:
                p.messages = messages
                if p.winner == True:
                    text_winner =  pygame.font.Font(None, 50).render(str(p.nickname) + " Won", True, 'white')
                    win.blit(text_winner, (320, 300))
                    scores = {car.nickname: [car.score, car.imgID], p2.nickname: [p2.score, p2.imgID], p3.nickname: [p3.score, p3.imgID], p4.nickname: [p4.score, p4.imgID], p5.nickname: [p5.score, p5.imgID]}
                    sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1][0], reverse=True))
                    x = 250
                    y = 400
                    for key, value in sorted_scores.items():
                        if value[0] > 0:
                            text_rank = font.render(str(key) + " score: " + str(value[0]), True, 'white')
                            win.blit(text_rank, (x, y))
                            y = y + 23
                pygame.display.update()


def startPageWindow():
    # Text box for the player to enter their nickname
    textBox = pygame.Rect(395, 260, 300, 50)
    global inputText
    inputText = ''
    started = False
    font = pygame.font.Font(None, 50)

    while not started:
        text = font.render("Please Enter Your Nickname", True, 'white')
        text_condition = pygame.font.Font(None,25).render("Do not exceed 10 Characters", True, 'white')
        win.blit(startPage, (0, 0))
        win.blit(text, (300, 200))
        win.blit(text_condition, (430, 320))
        textSurf = pygame.font.Font(None,35).render(inputText, True, 'white')
        win.blit(textSurf, (400,275))
        pygame.draw.rect(win, 'white', textBox, 2)
        pygame.display.flip()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    inputText = inputText[:-1]
                elif len(inputText)<10:
                    inputText += event.unicode


            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                started = True
                it = inputText[len(inputText)-1]
                inputText = inputText.replace(it,"",1)
                main(inputText)



if __name__ == "__main__":
    startPageWindow()


