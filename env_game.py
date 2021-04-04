import numpy as np
import pygame
import random

from agent import Agent


class EnvGame:
    def __init__(self):
        pygame.init()

        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)

        self.dis_width = 200
        self.dis_height = 200

        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake Game')

        self.clock = pygame.time.Clock()

        self.snake_block = 10
        self.snake_speed = 15

        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 15)

        self.agent = Agent(self.dis_height, self.dis_width, self.snake_block)
        self.state = None
        self.episodes = 0

    def Your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.yellow)
        self.dis.blit(value, [0, 0])

    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.dis, self.black, [x[0], x[1], snake_block, snake_block])
            if x[0] >= 0 and x[0] < self.dis_height and x[1] >= 0 and x[1] < self.dis_width:
                self.state[int(x[1] / 10), int(x[0] / 10)] = 2

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])

    def gameLoop(self):
        game_over = False
        game_close = False

        x1 = self.dis_width / 2
        y1 = self.dis_height / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0

        self.state = np.zeros([int(self.dis_height / 10), int(self.dis_width / 10)])
        self.agent.updateState(self.state, [x1, y1], [foodx, foody])
        qlearn = False

        while not game_over:

            while game_close == True:
                self.dis.fill(self.blue)
                self.message("You Lost! Press C-Play Again or Q-Quit", self.red)
                self.Your_score(Length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.gameLoop()

                self.episodes += 1
                self.agent.episodes += 1
                if self.episodes < 100:
                    self.gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            key = self.agent.nextActton(qlearn)

            if key == 'l':
                x1_change = -self.snake_block
                y1_change = 0
            elif key == 'r':
                x1_change = self.snake_block
                y1_change = 0
            elif key == 'u':
                y1_change = self.snake_block
                x1_change = 0
            elif key == 'd':
                y1_change = -self.snake_block
                x1_change = 0

            if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0:
                game_close = True
                reward = -10
                self.agent.updateState(self.state, [x1, y1], [foodx, foody], True)
                continue
            x1 += x1_change
            y1 += y1_change
            self.dis.fill(self.blue)
            self.state = np.zeros([int(self.dis_height / 10), int(self.dis_width / 10)])
            reward = 0
            pygame.draw.rect(self.dis, self.green, [foodx, foody, self.snake_block, self.snake_block])
            self.state[int(foody / 10), int(foodx / 10)] = 1
            snake_Head = [x1, y1]
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
                    reward = -10
                    self.agent.updateState(self.state, [x1, y1], [foodx, foody], True)
                    self.agent.QLearn(reward)
                    self.agent.QLearn(reward)

            self.our_snake(self.snake_block, snake_List)
            self.Your_score(Length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                Length_of_snake += 1
                reward = 10
                self.agent.updateState(self.state, [x1, y1], [x1, y1], False)
                self.agent.QLearn(reward)
                continue

            #self.clock.tick(self.snake_speed)
            self.agent.updateState(self.state, snake_Head, [foodx, foody], False)
            self.agent.QLearn(reward)
            qlearn = True

        pygame.quit()
