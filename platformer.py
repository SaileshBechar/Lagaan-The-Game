import pygame
import random

#Initialize pygame
pygame.init()

display_width = 640
display_height = 480

win = pygame.display.set_mode((display_width, display_height))

#Load Sprites
pygame.display.set_caption("Lagaan")  
bat_left = pygame.image.load('bat_left.png')
bat_right = pygame.image.load('bat_right.png')
bg = pygame.image.load('bg.png')
standing = pygame.image.load('R1.png')

#Init clock
clock = pygame.time.Clock()

score = 0
run = True

class player(object) :
    walk_left = [pygame.image.load('L1.png'), pygame.image.load('L2.png')]
    walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png')]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_Jump = False
        self.jump_height = 20
        self.vel = 25
        self.height_of_Jump = -1 * self.jump_height
        self.left = False
        self.right = True
        self.walk_count = False
        self.is_Fall = False

    def draw(self, win):
        if self.left:
            win.blit(self.walk_left[self.walk_count], (self.x,self.y))
            self.walk_count = not self.walk_count
        if self.right:
            win.blit(self.walk_right[self.walk_count], (self.x,self.y))
            self.walk_count = not self.walk_count

    def Jump(self):
        if self.y > display_height - self.height - 11:
            self.y = display_height - self.height - 11
        if self.is_Jump and not self.is_Fall:
            if self.height_of_Jump <= self.jump_height:
                if self.height_of_Jump < 0:
                    self.y -= (self.height_of_Jump/2) ** 2
                    for surface in platforms:
                        surface.isHit(self, "UP")
                else:
                    self.y += (self.height_of_Jump/2)** 2
                    for surface in platforms:
                        surface.isHit(self, "DOWN")
                self.height_of_Jump += 2
            else:
                self.is_Jump = False
                self.height_of_Jump = -1 * self.jump_height
                self.is_Fall = True
    def Fall(self, surface):
        if self.is_Fall:
            bhuvan.y += bhuvan.vel
            surface.isHit(bhuvan, "DOWN")
            if bhuvan.y > display_height - bhuvan.height - 11:
                bhuvan.y = display_height - bhuvan.height - 11
                self.is_Fall = False
    def isOnPlatform(self, surface):
        if not self.is_Fall and not self.is_Jump and self.y < display_height - self.height - 11:
            if self.y + self.height == surface.y1 and (self.x + self.width < surface.x1 or self.x > surface.x2): 
                self.is_Fall = True

class enemy(object) :
    walk_left = [pygame.image.load('s_l1.png'), pygame.image.load('s_l2.png')]
    walk_right = [pygame.image.load('s_r1.png'), pygame.image.load('s_r2.png')]
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.is_Fall = True
        self.is_Jump = False
        self.jump_height = 6
        self.vel = 3
        self.height_of_Jump = -1 * self.jump_height
        self.left = False
        self.right = True
        self.walk_count = False
        self.stop_walk = False

    def draw(self, win):
        if self.left:
            win.blit(self.walk_left[self.walk_count], (self.x,self.y))
            if not self.stop_walk:
                self.walk_count = not self.walk_count
        if self.right:
            win.blit(self.walk_right[self.walk_count], (self.x,self.y))
            if not self.stop_walk:
                self.walk_count = not self.walk_count
        
    def move(self, new_x, new_y):
        self.stop_walk  = False
        if self.x <= new_x - self.vel:
            self.right = True
            self.left = False
            self.x += self.vel
            for surface in platforms:
                surface.isHit(self,"RIGHT")
        elif self.x - self.vel >= new_x:
            self.left = True
            self.right = False
            self.x -= self.vel
            for surface in platforms:
                surface.isHit(self, "LEFT")
        else:
            self.stop_walk = True
        if new_y < display_height/2:
            self.is_Jump = True

    def Jump(self):
        if self.y > display_height - self.height - 11:
            self.y = display_height - self.height - 11
        if self.is_Jump and not self.is_Fall:
            if self.height_of_Jump <= self.jump_height:
                if self.height_of_Jump < 0:
                    self.y -= self.height_of_Jump ** 2
                    for surface in platforms:
                        surface.isHit(self, "UP")
                else:
                    self.y += self.height_of_Jump ** 2 
                    for surface in platforms:
                        surface.isHit(self, "DOWN")
                self.height_of_Jump += 1
            else:
                self.is_Jump = False
                self.is_Fall = True
                self.height_of_Jump = -1 * self.jump_height
    def Fall(self, surface):
        if self.is_Fall:
            self.y += self.vel
            surface.isHit(self, "DOWN")
            if self.y >= display_height - self.height - 11:
                self.y = display_height - self.height - 11
                self.is_Fall = False
    def isOnPlatform(self, surface):
        if not self.is_Fall and not self.is_Jump and self.y < display_height - self.height - 11:
            if self.y + self.height == surface.y1 and (self.x + self.width < surface.x1 or self.x > surface.x2): 
                self.is_Fall = True
    def is_Hit(self, bhuvan):
        if bhuvan.x <= self.x + self.width and bhuvan.x > self.x or bhuvan.x + bhuvan.width >= self.x and bhuvan.x + bhuvan.width <= self.x + self.width:
            if bhuvan.y + bhuvan.height >= self.y and bhuvan.y + bhuvan.height <= self.y + 30 :
                english.pop(english.index(self))
            else:
                if (bhuvan.y >= self.y and bhuvan.y <= self.y + self.height) or (bhuvan.y + bhuvan.height >= self.y and bhuvan.y + bhuvan.height <= self.y + self.height) or (bhuvan.y <= self.y and bhuvan.y + bhuvan.height >= self.y + self.height):
                    for soldier in english:
                        english.pop(english.index(soldier))
                    return True
        return False

class projectile(object):
    def __init__(self, x, y, width, height, facing, type_of_projectile):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.facing = facing
        self.type_of_projectile = type_of_projectile
        self.is_Created = True
        if facing:
            self.vel = facing * 10
        else:
            self.vel = -1 * 10

    def draw(self, win):
        if self.facing:
            if self.type_of_projectile == "bat":
                win.blit(bat_right, (self.x, self.y))
        else:
            if self.type_of_projectile == "bat":
                win.blit(bat_left, (self.x, self.y))
    
    def isHit(self, soldier):
        if (self.x >= soldier.x and self.x <= (soldier.x + soldier.width)) or (self.x + self.width >= soldier.x and self.x + self.width <= soldier.x + soldier.width):
                if (self.y > soldier.y and self.y < (soldier.y + soldier.height)) or (self.y + self.height > soldier.y and self.y + self.height< (soldier.y + soldier.height)) or (self.y >= soldier.y and self.y + self.height <= soldier.y + soldier.height) :
                    bats.pop(bats.index(self))
                    english.pop(english.index(soldier))
                    return True
        return False
        

class platform(object):
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        pygame.draw.rect(win, (132, 0, 66), (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))

    def isHit(self, person, direction):        
        if (person.x < self.x2 and person.x + person.width > self.x1) or (person.x + person.width > self.x1 and person.x + person.width < self.x2):
            if (person.y > self.y1 and person.y < self.y2) or (person.y + person.height > self.y1 and person.y + person.height < self.y2) or (person.y < self.y1 and person.y + person.height > self.y2):
                person.is_Fall = True
                if direction == "LEFT":
                    # print("Left")
                    person.x = self.x2
                elif direction == "RIGHT":
                    # print("Right")
                    person.x = self.x1 - person.width
                elif direction == "UP":
                    # print("Up", person.is_Jump)
                    person.y = self.y2
                elif direction == "DOWN":
                    # print("Down")
                    person.y = self.y1 - person.height
                    person.is_Fall = False
                person.is_Jump = False
                person.height_of_Jump = -1 * person.jump_height
                return True
        return False
def redrawWindow():
    global score
    global game_over 
    win.blit(bg, (0,0))

    for surface in platforms:
        surface.draw()
        bhuvan.isOnPlatform(surface)
        bhuvan.Fall(surface)

    for bat in bats:
        bat.draw(win)

    bhuvan.Jump()
    for soldier in english:
        soldier.move(bhuvan.x, bhuvan.y)
        soldier.Jump()
        for surface in platforms:
            soldier.isOnPlatform(surface)
            soldier.Fall(surface)
        for bat in bats:
            if bat.isHit(soldier):
                score += 1
            if bat.x > 0 and bat.x < display_width:
                bat.x += bat.vel
            else:
                bats.pop(bats.index(bat))
        if soldier.is_Hit(bhuvan):
            game_over = True
        soldier.draw(win)
    bhuvan.draw(win) 
    if game_over:
        text = font.render('Game Over', 1, (255,0,0))
        win.blit(text, (display_width/2 - 65, display_height/2))

    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (display_width/2 - 50, 10))
    
    pygame.display.update()

#main
game_over = False
bhuvan = player(display_width/2, display_height - 11 - 84, 28, 84) 
platforms = []
platforms.append(platform(display_width/2 - 100, display_width/2 + 100, display_height/2 + 20 , display_height/2 + 50))
bats = []
english = []
spacebar_spam = 0
spawn_timer = 0
english.append(enemy(36, 60, 0, display_height - 11 - 60))
font = pygame.font.SysFont('comicsans', 30, True)
score = 0
while run :
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if (spawn_timer > (200 - (score * 10)) or len(english) == 0) and not game_over:
        english.append(enemy(36, 60, random.randint(0, display_width - 36), random.randint(0, display_height - 11 - 60)))
        spawn_timer = 0
    else:
        spawn_timer += 1
    
    if keys[pygame.K_r]:
        game_over = False
        score = 0

    if keys[pygame.K_RIGHT]:
        bhuvan.right = True
        bhuvan.left = False
        bhuvan.x += bhuvan.vel
        for surface in platforms:
            surface.isHit(bhuvan, "RIGHT")
        #Right boundries
        if bhuvan.x > display_width - bhuvan.width:
            bhuvan.x = display_width - bhuvan.width
    elif keys[pygame.K_LEFT]:
        bhuvan.left = True
        bhuvan.right = False
        bhuvan.x -= bhuvan.vel
        for surface in platforms:
            surface.isHit(bhuvan, "LEFT")
        if bhuvan.x < 0:
            bhuvan.x = 0
    else:
        bhuvan.walk_count = False

    if keys[pygame.K_UP] and bhuvan.is_Fall == False:
        bhuvan.is_Jump = True
        spacebar_spam = 1

    if spacebar_spam > 0:
        spacebar_spam += 1
    
    if spacebar_spam == 10:
        spacebar_spam = 0

    for bat in bats:
    #     for soldier in english:
    #         if bat.x >= soldier.x and bat.x <= (soldier.x + soldier.width) or bat.x + bat.width >= soldier.x and bat.x + bat.width <= soldier.x + soldier.width:
    #             if bat.y > soldier.y and bat.y < (soldier.y + soldier.height) or bat.y + bat.height > soldier.y and bat.y + bat.height< (soldier.y + soldier.height) :
    #                 soldier.hit()
    #                 bats.pop(bats.index(bat))
    #                 english.pop(english.index(soldier))

        if bat.x > 0 and bat.x < display_width:
            bat.x += bat.vel
        else:
            bats.pop(bats.index(bat))
    if len(bats) < 5 and spacebar_spam == 0:
        if keys[pygame.K_SPACE]:
            bats.append(projectile(bhuvan.x, bhuvan.y + 35, 87, 13, bhuvan.right, "bat"))
            spacebar_spam = 1

    redrawWindow()
pygame.quit()

