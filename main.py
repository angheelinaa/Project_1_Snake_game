import pygame
from pygame.math import Vector2
import sys
import random
import pygame_menu


class Food:
    def __init__(self, bonus_image='food_image'):
        # random position for food
        self.x = random.randint(0, cell_number - 2)
        self.y = random.randint(0, cell_number - 2)
        self.pos = Vector2(self.x, self.y)
        self.bonus_image = bonus_image

    def draw_food(self):
        # draw two types of food
        if self.bonus_image == 'turtle_image':
            screen.blit(turtle_image, (self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size))
        elif self.bonus_image == 'food_image':
            screen.blit(food_image, (self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size))


class Snake:
    def __init__(self):
        # start position of snake
        self.body = [Vector2(cell_number // 2 + 1, cell_number // 2), Vector2(cell_number // 2, cell_number // 2)]
        # start direction of snake is right
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        for block in self.body:
            # choose color of snake
            if snake_color.get_index() == 0:
                pygame.draw.rect(screen, green, (block.x * cell_size, block.y * cell_size, cell_size, cell_size))
            elif snake_color.get_index() == 1:
                pygame.draw.rect(screen, pink, (block.x * cell_size, block.y * cell_size, cell_size, cell_size))
            elif snake_color.get_index() == 2:
                pygame.draw.rect(screen, blue, (block.x * cell_size, block.y * cell_size, cell_size, cell_size))
            elif snake_color.get_index() == 3:
                pygame.draw.rect(screen, red, (block.x * cell_size, block.y * cell_size, cell_size, cell_size))

    def move_snack(self):
        # head of snake is first element of list body
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self, other):
        self.body.append(other)

    def __len__(self):
        return len(self.body)


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.speed = 3

    def update(self):
        self.snake.move_snack()
        self.check_food()
        self.check_hits()

    def draw_elements(self):
        self.draw_background()
        self.food.draw_food()
        self.snake.draw_snake()
        self.draw_score()

    def check_food(self):
        # if position of food and head of snake have the same x and y
        if self.food.pos == self.snake.body[0]:
            # grow snake
            self.snake.add_block(self.food)
            if len(self.snake) % 6 == 1:
                self.speed -= 2
                # reposition food
                self.food = Food('turtle_image')
            else:
                self.speed += 1
                # reposition food
                self.food = Food('food_image')

    def check_hits(self):
        # snake hits a wall (check snake is outside)
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            return True
        # snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                return True
        return False

    def show_game_over(self):
        screen.fill(bg_color)
        game_over_message = message_font.render(f'Game is over! Your score is {len(self.snake) - 2}', True, score_color)
        screen.blit(game_over_message, (cell_size * 5, cell_size * 12))
        restart_game_message = message_font.render('Press SPACE for restart', True, score_color)
        screen.blit(restart_game_message, (cell_size * 7, cell_size * 16))
        menu_message = message_font.render('or ESCAPE to open menu', True, score_color)
        screen.blit(menu_message, (cell_size * 7, cell_size * 18))

    def is_game_over(self):
        if self.check_hits():
            return True
        return False

    def draw_background(self):
        screen.fill(bg_color)
        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, grass_color, (col * cell_size, row * cell_size, cell_size, cell_size))

    def draw_score(self):
        score_text = score_font.render(f"Score: {len(self.snake) - 2}", True, score_color)
        screen.blit(score_text, (cell_size, cell_size))
        speed_text = score_font.render(f"Speed: {self.speed - 2}", True, score_color)
        screen.blit(speed_text, (cell_size, cell_size * 3))


# sizes
cell_size = 20
cell_number = 30
width = cell_size * cell_number
height = cell_size * cell_number

# colors
white = (255, 255, 255)
red = (237, 24, 24)
blue = (44, 92, 138)
green = (52, 78, 91)
pink = (183, 101, 122)
grass_color = (167, 209, 61)
bg_color = (175, 215, 70)
score_color = (56, 74, 12)

# init pygame
pygame.init()
pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# fonts
score_font = pygame.font.SysFont('courier', 20)
message_font = pygame.font.SysFont('courier', 25)

# images
food_image = pygame.image.load('food.png').convert_alpha()
turtle_image = pygame.image.load('turtle.png').convert_alpha()
bg_image = pygame.image.load('bg_image.png').convert_alpha()
icon_image = pygame.image.load('icon.png').convert_alpha()

pygame.display.set_icon(icon_image)


def start_the_game():
    main_game = Game()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # keys for game over screen
                if main_game.is_game_over():
                    if event.key == pygame.K_SPACE:
                        main_game = Game()
                    elif event.key == pygame.K_ESCAPE:
                        menu.mainloop(screen, bgfun=background)
                # keys for game
                else:
                    if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                    elif event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)

        # check game over
        if main_game.is_game_over():
            main_game.show_game_over()
        else:
            main_game.update()
            main_game.draw_elements()

        pygame.display.update()
        clock.tick(main_game.speed)


def background():
    screen.blit(bg_image, (-75, 45))


# change theme for menu
theme_menu = pygame_menu.themes.THEME_DARK.copy()
theme_menu.background_color = (0, 0, 0, 0)
theme_menu.title = False
theme_menu.widget_font = pygame_menu.font.FONT_FIRACODE_BOLD
theme_menu.widget_font_size = 25
theme_menu.widget_font_color = white

# init menu
menu = pygame_menu.Menu('', 450, 250, theme=theme_menu)

# add button
menu.add.text_input('Name: ', default='Player 1')
snake_color = menu.add.selector('Snake color: ', [('Green', 0), ('Pink', 1), ('Blue', 2), ('Red', 3)])
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen, bgfun=background)