import pygame

pygame.init()
pygame.mixer.init()
file = ''
screen = pygame.display.set_mode((598,400))

pygame.display.set_caption('My Game')

score = 0
music = pygame.mixer.music.load('music (1).wav')
hit_sound = pygame.mixer.Sound('shot.wav')
#music = pygame.mixer.music.load(file)
pygame.mixer.music.play(-1)
 
#uplaoding character images to lists so i can call them through indexes
#when moving
walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]

walk_left = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
#Game clock
clock = pygame.time.Clock()




class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_count = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 50)
        self.score = 0



    def draw(self,screen):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
         
        if not (self.standing):
            if self.left:
                screen.blit(walk_left[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                screen.blit(walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count +=1
        else:
            if self.right:
                screen.blit(walk_right[0], (self.x, self.y))
            else:
                screen.blit(walk_left[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 50)
        # pygame.draw.rect(screen,(255,0,0), self.hitbox, 2)
            
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = 3
        self.speed_y = 3
        self.radius = 30
        self.hitbox = (self.x, self.y, 30, 30)
        


    def update(self, width, height):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x + self.radius > width:
            self.speed_x = -5
        if self.y + self.radius > height:
            self.speed_y = -5
        if self.x - self.radius < 0:
            self.speed_x = 5
        if self.y - self.radius < 0:
            self.speed_y = 5
        self.hitbox = (self.x + 10, self.y, 30, 30)

    def draw(self, screen):
        pygame.draw.circle(screen, (250, 0, 0), (self.x, self.y), self.radius)
        # self.hitbox = (self.x , self.y, 30, 30)

    def hit(self):
        print('hit')
        print(score)
        pass



class projectile:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 10 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

#Displaying screen
def screen_draw():
    screen.blit(bg, (0, 0))
    dave.draw(screen)
    text = font.render('Score: ' + str(dave.score), 1, (255,255,255))
    screen.blit(text,(480,20))
    for bullet in bullets:
        bullet.draw(screen)
    for balls in ball:
        balls.draw(screen)    


    pygame.display.update()
    
#Defining Hero
dave = Player(300, 288, 64, 64)
    # Game initialization

bullets = []
ball = [Ball(30, 20)]
font = pygame.font.SysFont('comicsans', 30, True)
def main():
    # score = 0
    width = 598
    height = 350
    shooter = 0
    start_game = True
    while start_game:
    #setting the frame rate 
        clock.tick(27)
    #Event listener
        if shooter > 0:
            shooter +=1
        if shooter > 3:
            shooter = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_game = False

        for balls in ball:
            balls.update(width, height)

        for bullet in bullets:
            if bullet.y - bullet.radius < ball[0].hitbox[1] + ball[0].hitbox[3] and bullet.y + bullet.radius > ball[0].hitbox[1]:
                if bullet.x + bullet.radius > ball[0].hitbox[0] and bullet.x + bullet.radius < ball[0].hitbox[0] + ball[0].hitbox[2]:
                    hit_sound.play()
                    ball[0].hit()
                    bullets.pop(bullets.index(bullet))
                    dave.score += 1
            if bullet.x < 598 and bullet.x > 0:
                bullet.x += bullet.speed  # Moves the bullet by its.speed
            else:
            # This will remove the bullet if it is off the screen
                bullets.pop(bullets.index(bullet))
        
            

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and shooter == 0:
            #hit_sound.play()
            if dave.left:
                facing = -1
            else:
                facing = 1

            if len(bullets) < 5:
                bullets.append(projectile(round(dave.x + dave.width // 2),round(dave.y + dave.height//2), 6, (51, 255, 51), facing))

            shooter += 1
    # This will create a bullet starting at the middle of the character
    #letting the character go left and right without going over borders
        if keys[pygame.K_LEFT] and dave.x > dave.speed :
            dave.x -= dave.speed
            dave.left = True
            dave.right = False
            dave.standing = False
        elif keys[pygame.K_RIGHT] and dave.x < 598 - dave.width - dave.speed:
            dave.x += dave.speed
            dave.right = True
            dave.left = False
            dave.standing = False
        else:
            dave.standing = True
            dave.walk_count = 0

    #alloscreeng character to jump
        if not (dave.jump):
            if keys[pygame.K_UP]:
                dave.jump = True
                dave.right = False
                dave.left = False
                dave.walk_count = 0
        else:
            if dave.jump_count >= -10:
                neg = 1
                if dave.jump_count < 0:
                    neg = -1
                dave.y -= (dave.jump_count ** 2) / 2 * neg
                dave.jump_count -= 1
            else:
                dave.jump = False
                dave.jump_count = 10
        


        screen_draw()
    pygame.quit()

# if __name__ == '__main__':
main()
