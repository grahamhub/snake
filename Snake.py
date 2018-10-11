__author__ = 'JR'

import pygame
import random
import sys
import time

# colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (35, 25, 255)
green = (35, 255, 25)
red = (255, 35, 25)

count = 0

# width/height of snake segments
seg_width = 15
seg_height = 15
# space between each segment
seg_margin = 3

# set initial speed
x_change = seg_width + seg_margin
y_change = 0


def play():
    while True:
        font = pygame.font.Font(None, 60)
        font.set_bold(True)
        title = font.render("Press Enter to Play", True, white)
        titlepos = title.get_rect()
        titlepos.centerx = screen.get_rect().centerx
        titlepos.centery = screen.get_rect().centery
        screen.blit(title, titlepos)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True


def score():
    while True:
        font = pygame.font.Font(None, 60)
        font.set_bold(True)
        title = font.render("Your score was " + str(count) + "!", True, white)
        titlepos = title.get_rect()
        titlepos.centerx = screen.get_rect().centerx
        titlepos.centery = screen.get_rect().centery
        screen.blit(title, titlepos)
        pygame.display.flip()
        time.sleep(3)
        break


def replay():
    while True:
        font = pygame.font.Font(None, 60)
        font.set_bold(True)
        title = font.render("Press Enter to Replay", True, white)
        titlepos = title.get_rect()
        titlepos.centerx = screen.get_rect().centerx
        titlepos.centery = screen.get_rect().centery
        screen.blit(title, titlepos)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    sys.exit()


class Segment(pygame.sprite.Sprite):
    # class to represent one segment of the snake
    def __init__(self, x, y):
        super(Segment, self).__init__()

        # set height/width
        self.image = pygame.Surface([seg_width, seg_height])
        self.image.fill(white)

        # starting pos(top left corner)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Block(pygame.sprite.Sprite):
    # class for blocks to collect
    def __init__(self):
        super(Block, self).__init__()
        self.image = pygame.Surface([seg_width, seg_height])
        self.image.fill(green)
        self.rect = self.image.get_rect()

    # spawning the block
    def spawn(self):
        self.rect.x = random.randrange(10, 790)
        self.rect.y = random.randrange(10, 590)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.Surface([seg_width, seg_height])
        self.image.fill(red)
        self.rect = self.image.get_rect()

    def spawn(self):
        self.rect.x = random.randrange(10, 790)
        self.rect.y = random.randrange(10, 590)


pygame.init()

screen = pygame.display.set_mode([800, 600])

pygame.display.set_caption('Snake')

points = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
allspriteslist = pygame.sprite.Group()
block = Block()
points.add(block)

# create the snake
snake_segs = []
for i in range(5):
    x = 250 - (seg_width + seg_margin) * i
    y = 30
    segment = Segment(x, y)
    snake_segs.append(segment)
    allspriteslist.add(segment)

clock = pygame.time.Clock()

enemies = []


def addenemy():
    enemy = Enemy()
    enemy.spawn()
    enemies.append(enemy)
    obstacles.add(enemies)
    obstacles.draw(screen)


# spawn the first block
block.spawn()


if play() is True:
    while True:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # speed = a segment plus the margin
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = (seg_width + seg_margin) * -1
                        y_change = 0
                    if event.key == pygame.K_RIGHT:
                        x_change = (seg_width + seg_margin)
                        y_change = 0
                    if event.key == pygame.K_UP:
                        x_change = 0
                        y_change = (seg_height + seg_margin) * -1
                    if event.key == pygame.K_DOWN:
                        x_change = 0
                        y_change = (seg_height + seg_margin)

            # so that the snake doesn't keep growing:
            old_segment = snake_segs.pop()
            allspriteslist.remove(old_segment)

            # where the new segment will be:
            x = snake_segs[0].rect.x + x_change
            y = snake_segs[0].rect.y + y_change
            segment = Segment(x, y)
            # if out of bounds
            if x > 800 or x < 0:
                allspriteslist.empty()
                screen.fill(black)
                break
            if y > 600 or y < 0:
                allspriteslist.empty()
                screen.fill(black)
                break

            # put new segment into list
            snake_segs.insert(0, segment)
            allspriteslist.add(segment)

            screen.fill(blue)

            points.draw(screen)
            obstacles.draw(screen)
            allspriteslist.draw(screen)

            # check for collisions
            blocks_hit = pygame.sprite.spritecollide(segment, points, False)
            if blocks_hit:
                snake_segs.append(segment)
                allspriteslist.add(segment)
                block.spawn()
                points.add(block)
                addenemy()
                count += 1
            endgame = pygame.sprite.spritecollide(segment, obstacles, True)
            if endgame:
                allspriteslist.empty()
                screen.fill(black)
                break

            pygame.display.flip()

            # set speed
            clock.tick(10)
        score()
        screen.fill(black)
        if replay() is True:
            for i in range(count):
                enemies.pop()
                obstacles.empty()
            snake_segs = []
            for i in range(5):
                x = 250 - (seg_width + seg_margin) * i
                y = 30
                segment = Segment(x, y)
                snake_segs.append(segment)
                allspriteslist.add(segment)
            x_change = (seg_width + seg_margin)
            y_change = 0
            count -= count
