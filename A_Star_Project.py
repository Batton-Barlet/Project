import pygame
import random
import math
from queue import PriorityQueue
import time
# import msvcrt
pygame.init()


WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Algorithm Project")

font = pygame.font.SysFont('comicsansms', 32, True)
text = font.render('Добрый день', True, (255, 255, 255))
WIN.blit(text, (170, 250))
pygame.display.update()
time.sleep(3)

class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = (100, 100, 100)
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == (200, 0, 0)

	def is_open(self):
		return self.color == (0, 200, 0)

	def is_barrier(self):
		return self.color == (0, 0, 0)

	def is_start(self):
		return self.color == (255, 255, 0)

	def is_end(self):
		return self.color == (0, 0, 250)

	def reset(self):
		self.color = (100, 100, 100)

	def make_start(self):
		self.color = (255, 255, 0)

	def make_closed(self):
		self.color = (200, 0, 0)

	def make_open(self):
		self.color = (0, 200, 0)

	def make_barrier(self):
		self.color = (0, 0, 0)

	def make_end(self):
		self.color = (0, 0, 250)

	def make_path(self):
		self.color = (148, 0, 211)

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw, grid):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw, grid)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, (75, 75, 75), (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, (75, 75, 75), (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	win.fill((75, 75, 75))

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def print_end():
	win.fill((0, 0, 0))
	text = font.render('ИГРА ОКОНЧЕНА', True, (255, 255, 255))
	WIN.blit(text, (150, 250))
	pygame.display.update()

def draw_evrth(win, width):
	global text
	WIN.fill((50, 50, 50))
	font = pygame.font.SysFont('comicsansms', 24, True)
	text = font.render('Этим проектом я хочу наглядно показать', True, (200, 200, 200))
	text1 =  font.render('как думает ИИ(искусственный интеллект)', True, (200, 200, 200))
	text2 = font.render('в видеоиграх ', True, (200, 200, 200))
	WIN.blit(text, (60, 250))
	WIN.blit(text1, (60, 290))
	WIN.blit(text2, (60, 330))
	pygame.display.update()
	time.sleep(4)

	WIN.fill((50, 50, 50))
	text = font.render('Знаете такую функцию в игре, ', True, (200, 200, 200))
	text1 = font.render('когда вы даете своему персонажу задание', True, (200, 200, 200))
	text2 = font.render('добежать до какого-либо места на карте,', True, (200, 200, 200))
	text3 = font.render('и он,огибая все препятствия,до него доходит?', True, (200, 200, 200))
	WIN.blit(text, (30, 250))
	WIN.blit(text1, (30, 290))
	WIN.blit(text2, (30, 330))
	WIN.blit(text3, (30, 370))
	pygame.display.update()
	time.sleep(6)

	WIN.fill((50, 50, 50))
	text = font.render('Иногда даже бывает так,', True, (200, 200, 200))
	text1 = font.render('что чтобы дойти до указанного места ', True, (200, 200, 200))
	text2 = font.render('нужно пройти сквозь всю карту,', True, (200, 200, 200))
	text3 = font.render('на которой может быть очень много преград', True, (200, 200, 200))
	WIN.blit(text, (30, 250))
	WIN.blit(text1, (30, 290))
	WIN.blit(text2, (30, 330))
	WIN.blit(text3, (30, 370))
	pygame.display.update()
	time.sleep(6)

	WIN.fill((50, 50, 50))
	text = font.render('Так, как же персонаж понимает,', True, (200, 200, 200))
	text1 = font.render('куда и как ему нужно идти? ', True, (200, 200, 200))
	WIN.blit(text, (30, 250))
	WIN.blit(text1, (30, 290))
	pygame.display.update()
	time.sleep(4)

	WIN.fill((50, 50, 50))
	text = font.render('Тут как раз таки на помощь и приходит ИИ', True, (200, 200, 200))
	WIN.blit(text, (30, 250))
	pygame.display.update()
	time.sleep(7)

	WIN.fill((50, 50, 50))
	img = pygame.image.load('include/astar.png').convert_alpha()
	new_img = pygame.transform.scale(img, (WIDTH, 200))
	text = font.render('A star', True, (230, 230, 230))
	text1 = font.render('Это оптимальный алгоритм нахождения', True, (230, 230, 230))
	text2 = font.render('самого короткого пути от точки до точки', True, (230, 230, 230))
	text4 = font.render('Даже если на пути будут препятствия', True, (230, 230, 230))
	text3 = font.render('А этот проект - визуализация этого алгоритма', True, (230, 230, 230))
	WIN.blit(text, (200, 250))
	WIN.blit(text1, (30, 290))
	WIN.blit(text2, (30, 330))
	WIN.blit(text4, (30, 390))
	WIN.blit(text3, (20, 480))
	WIN.blit(new_img, (0, 0))
	pygame.display.update()
	time.sleep(8)

	WIN.fill((50, 50, 50))
	text = font.render('Сейчас вы сами сможете увидеть то', True, (230, 230, 230))
	text1 = font.render('как в описанной выше ситуации думает ИИ', True, (230, 230, 230))
	WIN.blit(text, (20, WIDTH//2))
	WIN.blit(text1, (20, WIDTH//2+40))
	pygame.display.update()
	time.sleep(6)

	font = pygame.font.SysFont('comicsansms', 36, True)
	WIN.fill((0, 0, 0))
	text = font.render('НО! Для начала', True, (255, 255, 255))
	text1 = font.render('я предлагаю', True, (255, 255, 255))
	font = pygame.font.SysFont('comicsansms', 26, True)
	text2 = font.render('ознакомиться с функционалом программы', True, (255, 255, 255))
	WIN.blit(text, (WIDTH/4, WIDTH/4))
	WIN.blit(text1, (WIDTH/5, WIDTH/2+30))
	WIN.blit(text2, (10, WIDTH/2+100))
	pygame.display.update()
	time.sleep(5)

	WIN.fill((0, 0, 0))
	text0 = font.render("Нажатие клавиши: ", True, (255, 255, 255))
	text = font.render("'r' - обновляет поле", True, (255, 255, 255))
	text1 = font.render("'c' - очищает поле", True, (255, 255, 255))
	text2 = font.render("'Space' - запускает алгоритм", True, (255, 255, 255))
	text3 = font.render("И бонус)", True, (100, 0, 0))
	WIN.blit(text0, (WIDTH/4, 50))
	WIN.blit(text, (10, 150))
	WIN.blit(text1, (10, 200))
	WIN.blit(text2, (10, 250))
	WIN.blit(text3, (WIDTH-150, WIDTH-60))
	pygame.display.update()
	time.sleep(5)

	WIN.fill((0, 0, 0))
	text0 = font.render("БОНУС:", True, (180, 0, 0))
	font = pygame.font.SysFont('comicsansms', 24, True)
	text = font.render("после нажатия клавиши 'c'", True, (255, 255, 255))
	text1 = font.render("Вы сможете создать свое собственное", True, (255, 255, 255))
	text2 = font.render("Уникальное поле", True, (255, 255, 255))
	text3 = font.render("Первое нажатие мышкой устанавливает начало", True, (220, 220, 220))
	text4 = font.render("Второе - конец", True, (220, 220, 220))
	text5 = font.render("Потом вы сможете рисовать преграды мышкой", True, (220, 220, 220))
	WIN.blit(text0, (WIDTH/4, 50))
	WIN.blit(text, (10, 150))
	WIN.blit(text1, (10, 200))
	WIN.blit(text2, (10, 250))
	WIN.blit(text3, (10, 350))
	WIN.blit(text4, (10, 400))
	WIN.blit(text5, (10, 450))
	pygame.display.update()
	time.sleep(5)

	WIN.fill((0, 0, 0))
	font = pygame.font.SysFont('comicsansms', 55, True)
	text = font.render("ПОЕХАЛИ", True, (0, 0, 100))
	WIN.blit(text, (WIDTH/4, WIDTH/4))
	pygame.display.update()
	time.sleep(3)

def main(win, width):

	ROWS = 40
	grid = make_grid(ROWS, width)
	level = 1

	if level == 1:

		q = random.randrange(ROWS)
		z = random.randrange(ROWS)

		node = grid[1][1]
		start = node
		start.make_start()

		node = grid[q][z]
		end = node
		end.make_end()

		wall = []

		for i in range(ROWS*14):
			x = random.randrange(ROWS)
			y = random.randrange(ROWS)
			if [x, y] != [1, 1] and [x, y] != [q, z]:
				wall.append([x, y])

		for w in wall:
			node = grid[w[0]][w[1]]
			walls = node
			walls.make_barrier()

		level += 1

	else:
		start = None
		end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				# print(pos)
				row, col = get_clicked_pos(pos, ROWS, width)
				# print(f'x={row}, y={col}')
				node = grid[row][col]
				if not start and node != end:
					start = node
					start.make_start()

				elif not end and node != start:
					end = node
					end.make_end()

				if node != end and node != start:
					node.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				# print(f'x={row}, y={col}')
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_r:
							for i in range(ROWS):
								for j in range(ROWS):
									node = grid[i][j]
									node.reset()
							q = random.randrange(ROWS)
							z = random.randrange(ROWS)
					
							node = grid[1][1]
							start = node
							start.make_start()

							node = grid[q][z]
							end = node
							end.make_end()
					
							wall = []
					
							for i in range(ROWS*14):
								x = random.randrange(ROWS)
								y = random.randrange(ROWS)
								if [x, y] != [1, 1] and [x, y] != [q, z]:
									wall.append([x, y])
					
							for w in wall:
								node = grid[w[0]][w[1]]
								walls = node
								walls.make_barrier()
					
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
					
			# if :
			# 	print_end()


	pygame.quit()



# k = msvcrt.getch()
# if not k == b'\x1b':
# 	draw_evrth(WIN, WIDTH)
# 	main(WIN, WIDTH)
# elif k == b'\x1b':
# 	main(WIN, WIDTH)

draw_evrth(WIN, WIDTH)
main(WIN, WIDTH)