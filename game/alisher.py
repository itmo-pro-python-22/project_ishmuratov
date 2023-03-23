import pygame
import random

pygame.init()
display_w = 800
display_h = 600
display = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('SoftGame')
logo = pygame.image.load('ic.png')
pygame.display.set_icon(logo)

enemy_img = [pygame.image.load('en1.png'), pygame.image.load('en2.png'), pygame.image.load('en3.png')]
enemy_options = [77, 414, 82, 414, 66, 429]

grass_img = [pygame.image.load('grass1.png'), pygame.image.load('grass2.png'), pygame.image.load('grass3.png'),
             pygame.image.load('grass4.png')]

cloud_img = [pygame.image.load('cloud1.png'), pygame.image.load('cloud2.png'), pygame.image.load('cloud3.png'),
             pygame.image.load('cloud4.png')]

pers_img = [pygame.image.load('pers1.png'), pygame.image.load('pers2.png'), pygame.image.load('pers3.png'),
            pygame.image.load('pers4.png'), pygame.image.load('pers5.png'), pygame.image.load('pers6.png')]

pers_counter = 0

score = 0
above_enemy = False


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            # pygame.draw.rect(display, (150,20,200),(self.x,self.y,self.width,self.height))
            self.x -= self.speed
            return True
        else:
            return False
            # self.x = display_w + 100 + random.randrange(-80, 60)

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


pers_width = 94
pers_height = 125
make_jump = False
make_up = False
pers_x = display_w // 4
pers_y = display_h - 100 - pers_height

enemy_width = 20
enemy_height = 70
enemy_x = display_w - 50
enemy_y = display_h - enemy_height - 100

dy = 20
dy_up = 10


def rungame():
    global make_jump, make_up, pers_counter
    game = True
    enemies = []
    create_enemies(enemies)
    land = pygame.image.load('BG.png')
    grass, cloud = open_rand_objects()

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if make_jump:
            jump()
        if keys[pygame.K_UP]:
            make_up = True
        if keys[pygame.K_ESCAPE]:
            pause()
        if make_up:
            pers_up()

        display.blit(land, (0, 0))
        count_scores(enemies)
        print_text("SCORE: " + str(score), 600, 10, (0, 160, 0))

        draw_enemies(enemies)

        draw_pers()

        if check_collision(enemies):
            game = False

        move_objects(grass, cloud)
        # pygame.draw.rect(display, (251,186,0),(pers_x, pers_y, pers_width, pers_height))
        pygame.display.update()
        pygame.time.Clock().tick(60)
    return game_over()


def jump():
    global pers_y, make_jump, dy
    if dy >= -20:
        pers_y -= dy
        dy -= 1
    else:
        dy = 20
        make_jump = False


def pers_up():
    global pers_height, make_up, dy_up
    if dy_up >= -10:
        pers_height -= dy_up
        dy_up -= 1
    else:
        dy_up = 10
        make_up = False


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Paused. Press ENTER to continue', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        pygame.time.Clock().tick(15)


def print_text(message, x, y, font_color=(200, 0, 100), font_type='comic.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def create_enemies(enemies):
    choice = random.randrange(0, 3)
    img = enemy_img[choice]
    width = enemy_options[choice * 2]
    height = enemy_options[choice * 2 + 1]
    enemies.append(Object(display_w + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = enemy_img[choice]
    width = enemy_options[choice * 2]
    height = enemy_options[choice * 2 + 1]
    enemies.append(Object(display_w + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = enemy_img[choice]
    width = enemy_options[choice * 2]
    height = enemy_options[choice * 2 + 1]
    enemies.append(Object(display_w + 600, height, width, img, 4))


def find_radius(enemies):
    maximum = max(enemies[0].x, enemies[1].x, enemies[2].x)
    if maximum < display_w:
        radius = display_w
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)

    return radius


def draw_pers():
    global pers_counter
    if pers_counter == 30:
        pers_counter = 0
    display.blit(pers_img[pers_counter // 5], (pers_x, pers_y))
    pers_counter += 1


def draw_enemies(enemies):
    for x in enemies:
        check = x.move()
        if not check:
            radius = find_radius(enemies)
            choice = random.randrange(0, 3)
            img = enemy_img[choice]
            width = enemy_options[choice * 2]
            height = enemy_options[choice * 2 + 1]
            x.return_self(radius, height, width, img)


def open_rand_objects():
    choice = random.randrange(0, 4)
    img_of_grass = grass_img[choice]

    choice = random.randrange(0, 4)
    img_of_cloud = cloud_img[choice]

    grass = Object(display_w, display_h - 80, 65, img_of_grass, 3)
    cloud = Object(display_w, 80, 165, img_of_cloud, 2)

    return grass, cloud


def move_objects(grass, cloud):
    check = grass.move()
    if not check:
        choice = random.randrange(0, 4)
        img_of_grass = grass_img[choice]
        grass.return_self(display_w, 450 + random.randrange(25, 80), grass.width, img_of_grass)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 4)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_w, random.randrange(10, 200), cloud.width, img_of_cloud)


def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 429:
            if not make_jump:
                if barrier.x <= pers_x + pers_width - 45 <= barrier.x + barrier.width:
                    return True
            elif dy >= 0:
                if pers_y + pers_height - 5 >= barrier.y:
                    if barrier.x <= pers_x + pers_width - 55 <= barrier.x + barrier.width:
                        return True
            else:
                if pers_y + pers_height - 20 >= barrier.y:
                    if barrier.x <= pers_x + 15 <= barrier.x + barrier.width:
                        return True

                '''if pers_y + pers_height >= barrier.y:
            if barrier.x <= pers_x <= barrier.x + barrier.width:
                return True
            elif barrier.x <= pers_x + pers_width:
                return True'''

    return False


def game_over():
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game Over. Press ENTER to play again, Esc to exit', 60, 250)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        pygame.time.Clock().tick(15)


def count_scores(barriers):
    global score, above_enemy

    if not above_enemy:
        for barrier in barriers:
            if barrier.x <= pers_x + pers_width / 2 <= barrier.x + barrier.width:
                if pers_y + pers_height - 5 <= barrier.y:
                    above_enemy = True
                    break
    else:
        if dy == -20:
            score += 1
            above_enemy = False


while rungame():
    score = 0
    pers_y = display_h - 100 - pers_height
    make_jump = False
    dy = 20
pygame.quit()
quit()
