import pygame
import random
import os

WIN_WIDTH = 1000
WIN_HEIGHT = 600
xscreen = 175
yscreen = 90

FPS = 60
snake_speed = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG = (51, 0, 102)
FOODCOLOR = (255, 255, 153)
SNAKECOLOR = (102, 204, 0)

show_score = False
snake_block = 10

umesg = 'You'
ctrls = 'Use W,A,S,D controls'
pygame.init()

font_style = pygame.font.SysFont("Copperplate Gothic", 15)


clock = pygame.time.Clock()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xscreen,yscreen)
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


left = False
right = False
up = False
down = False
x_change = 0
y_change = 0
x = WIN_WIDTH // 2
y = WIN_HEIGHT // 2




class Snake:
	def __init__(self, snake_block, gameOver):
		self.snake_block = snake_block
		self.gameOver = gameOver
		self.Length_of_snake = 1
		

	def snakeChunk(self, snake_block, snake_list):
		for i in snake_list:
			pygame.draw.rect(screen, SNAKECOLOR, [i[0], i[1], snake_block, snake_block])


	def gameLoop(self):
		global x, y, x_change, y_change, show_score, BG, snake_speed, umesg, ctrls
		snakeList = []
		foodx = round(random.randrange(snake_block * 3, WIN_WIDTH - (snake_block * 3)) // 10) * 10
		foody = round(random.randrange(snake_block * 3, WIN_HEIGHT - (snake_block * 3)) // 10) * 10
		
		file_pointer = open("highscore.txt", "rt")
		HIGHSCORE = file_pointer.read()
		GREEN   = (0, 255, 0)
		while not self.gameOver:
			if show_score == True:
				BG = (128,128,128)
				self.message("You Lost! Play Again? (y/n)", RED)
				# self.Your_score(self.Length_of_snake - 1)
				pygame.display.update()
				clock.tick(snake_speed)
				   
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.gameOver = True
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_n:
							print('quit')
							self.gameOver = True
							# game_close = False
						elif event.key == pygame.K_y:
							show_score = False
							BG = (51, 0, 102)
							self.refresh()
							snakeHead = []
							self.snakeList = []
							self.Length_of_snake = 1
							self.highScore(HIGHSCORE)
							umesg = 'You'
							ctrls = 'Use W,A,S,D controls'
							self.gameLoop()

			self.gameControls()
			if x >= WIN_WIDTH or x < 0 or y >= WIN_HEIGHT or y < 0:
				show_score = True
				# self.gameOver = True
			x += x_change
			y += y_change
			screen.fill(BG)
			
			
			r = random.randint(30,230)
			g = random.randint(30,230)
			b = random.randint(30,230)
			pygame.draw.rect(screen, (r, g, b), [foodx, foody, snake_block, snake_block])

			## check the position of the head
			snakeHead = []
			snakeHead.append(x)
			snakeHead.append(y)
			snakeList.append(snakeHead)

			## sets the head
			if len(snakeList) > self.Length_of_snake:
				del snakeList[0]

			## if head hits the body
			for body in snakeList[:-1]:
				if body == snakeHead:
					show_score = True
					# self.gameOver = True

			self.snakeChunk(self.snake_block, snakeList)
			self.your_score(self.Length_of_snake - 1, GREEN)
			self.highScore(HIGHSCORE)
			self.playerLocator(umesg, WHITE)
			self.useWASD(ctrls, (0, 255, 255))
			# self.check_highScore()


			
			pygame.display.update()
			if x == foodx and y == foody:
				foodx = round(random.randrange(snake_block * 3, WIN_WIDTH - (snake_block * 3)) // 10) * 10
				foody = round(random.randrange(snake_block * 3, WIN_HEIGHT - (snake_block * 3)) // 10) * 10
				self.Length_of_snake += 1
				# c+=10
				print('Yummy!')

			if self.Length_of_snake - 1 > int(HIGHSCORE):
				file_pointer = open("highscore.txt", "rt")
				#read file contents to string
				highscore = file_pointer.read()
				#replace all occurrences of the required string
				highscore = highscore.replace(highscore, str(self.Length_of_snake - 1))
				#close the input file
				file_pointer.close()

				file_pointer = open("highscore.txt", "wt")
				#overrite the input file with the resulting data
				file_pointer.write(highscore)
				#close the file
				
				print('new highscore!')
				file_pointer.close()
				GREEN = (r,g,b)
				
			clock.tick(snake_speed)
		file_pointer.close()
		pygame.quit()
		quit()
	
	def gameControls(self):
		global x_change, y_change, show_score, umesg, ctrls
		global left, right, up, down
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameOver = True
				if event.type == pygame.KEYDOWN:
					umesg = ''
					ctrls = ''
					if event.key == pygame.K_a and right != True:
						x_change = -10
						y_change = 0
						left = True
						right = False
						up = False
						down = False
						
						
					elif event.key == pygame.K_d and left != True:
						x_change = 10
						y_change = 0
						left = False
						right = True
						up = False
						down = False
						
					elif event.key == pygame.K_w and down != True:
						x_change = 0
						y_change = -10
						left = False
						right = False
						up = True
						down = False
					elif event.key == pygame.K_s and up != True:
						x_change = 0
						y_change = 10
						left = False
						right = False
						up = False
						down = True
	def refresh(self):
		global left, right, up, down, x_change, y_change, x, y
		left = False
		right = False
		up = False
		down = False
		x_change = 0
		y_change = 0
		x = WIN_WIDTH // 2
		y = WIN_HEIGHT // 2

	def your_score(self, score, color):
	    value = font_style.render("Your Score: " + str(score), True, color)
	    screen.blit(value, [0, 0])

	def playerLocator(self, score, color):
	    mesg = font_style.render(umesg, True, color)
	    screen.blit(mesg, [x - 10, y + 10])

	def message(self, msg, color):
	    mesg = font_style.render(msg, True, color)
	    screen.blit(mesg, [(WIN_WIDTH // 2) - 100, WIN_HEIGHT // 2])

	def useWASD(self, msg, color):
		mesg = font_style.render(msg, True, color)
		screen.blit(mesg, [(WIN_WIDTH // 2) - 90, (WIN_HEIGHT // 2) - 100])

	def highScore(self, hscore):
		text = "High Score: "
		value = font_style.render(text + str(hscore), True, (255, 0, 0))
		screen.blit(value, [0, 20])

		      
gameOver = False
s = Snake(snake_block, gameOver)

s.gameLoop()
