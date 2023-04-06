import pygame as pg
import sys, random, math
from pygame.locals import *

pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()

W, H = 1920, 1080
win = pg.display.set_mode((W, H), pg.FULLSCREEN)
clock = pg.time.Clock()
pg.mouse.set_visible(False)



global start, player_pos, volume
start = pg.time.get_ticks()
player_pos = win.get_rect().center
volume = 0.01


enemies = []


player_sprite = pg.image.load('Sprites\\player.png').convert()
player_rect = player_sprite.get_rect()
enemy_sprite = pg.image.load('Sprites\\enemy.png').convert()
enemy_rect = enemy_sprite.get_rect()
green_line_part_sprite = pg.image.load('Sprites\\green.png').convert()


hit_sound = pg.mixer.Sound('Sounds\\Hit.mp3')
hit_sound.set_volume(0.01)

#pg.mixer.music.load('Sounds\\Song.mp3')
pg.mixer.music.load('Sounds\\OKSI_SWDR.mp3')
pg.mixer.music.set_volume(volume)


class Enemy:
	def __init__(self, win, sprite, pos, direction):
		self.win = win
		self.sprite = sprite
		self.rect = self.sprite.get_rect()
		self.rect.center = (pos[0], pos[1])
		self.direction = direction
		self.vel = random.randint(1,7)

	def draw(self):
		self.win.blit(self.sprite, (self.rect.center))


class Player:
	def __init__(self, win, sprite, pos):
		self.win = win
		self.sprite = sprite
		self.rect = self.sprite.get_rect()
		self.rect.center = pos
		self.orig = self.sprite
		self.speed = 3

	def update(self):
		global player_pos
		mx, my = pg.mouse.get_pos()

		circle = pg.draw.circle(win, (0,255,0), (mx, my), 5, 1)

		dx = mx - player_pos[0] - 10
		dy = my - player_pos[1] - 10

		angle = math.atan2(dx, dy)
		mvx = math.sin(angle)
		mvy = math.cos(angle)

		player_pos = (player_pos[0] + mvx*self.speed, player_pos[1] + mvy*self.speed)

	def draw(self):
		self.win.blit(self.sprite, (self.rect.center))


def Collide(rect_pl, rect_en):
	collide = rect_en.colliderect(rect_pl)
	if collide:
		return True
	else:
		return False


def EnemySpawn():
	global start
	now = pg.time.get_ticks()
	if now - start >= random.randint(10, 200):
		start = now
		direction = random.choice(['up','left','down','right','dl','dr','ul','ur'])
		if direction == 'up':
			enemies.append(Enemy(win, enemy_sprite, (random.randint(0, 1900), 1080), direction))
		elif direction == 'down':
			enemies.append(Enemy(win, enemy_sprite, (random.randint(0, 1900), -20), direction))
		elif direction == 'left':
			enemies.append(Enemy(win, enemy_sprite, (1920, random.randint(0, 1080)), direction))
		elif direction == 'right':
			enemies.append(Enemy(win, enemy_sprite, (-20, random.randint(0, 1080)), direction))
		elif direction == 'dl':
			enemies.append(Enemy(win, enemy_sprite, (1920, random.randint(-540, 520)), direction))
		elif direction == 'dr':
			enemies.append(Enemy(win, enemy_sprite, (-20, random.randint(-540, 520)), direction))
		elif direction == 'ul':
			enemies.append(Enemy(win, enemy_sprite, (1920, random.randint(540, 1600)), direction))
		else:
			enemies.append(Enemy(win, enemy_sprite, (-20, random.randint(540, 1600)), direction))


def EnemyMove():
	pos = pg.mouse.get_pos()
	for enemy in enemies:
		if enemy.direction == 'down':
			if enemy.rect.center[1] < 1080:
				enemy.rect.center = (enemy.rect.center[0], enemy.rect.center[1] + enemy.vel)
			else:
				enemies.pop(enemies.index(enemy))
		if enemy.direction == 'up':
			if enemy.rect.center[1] > -20:
				enemy.rect.center = (enemy.rect.center[0], enemy.rect.center[1] - enemy.vel)
			else:
				enemies.pop(enemies.index(enemy))
		if enemy.direction == 'left':
			if enemy.rect.center[0] > -20:
				enemy.rect.center = (enemy.rect.center[0] - enemy.vel, enemy.rect.center[1])
			else:
				enemies.pop(enemies.index(enemy))
		if enemy.direction == 'right':
			if enemy.rect.center[0] < 1980:
				enemy.rect.center = (enemy.rect.center[0] + enemy.vel, enemy.rect.center[1])
			else:
				enemies.pop(enemies.index(enemy))
		if enemy.direction == 'dl':
			if enemy.rect.center[1] < 1080:
				if enemy.rect.center[0] > -20:
					enemy.rect.center = (enemy.rect.center[0] - enemy.vel//2, enemy.rect.center[1] + enemy.vel//2)
				else:
					enemies.pop(enemies.index(enemy))
			else:
				enemies.pop(enemies.index(enemy))
		if enemy.direction == 'dr':
			if enemy.rect.center[1] < 1080:
				if enemy.rect.center[0] < 1920:
					enemy.rect.center = (enemy.rect.center[0] + enemy.vel//2, enemy.rect.center[1] + enemy.vel//2)
				else:
					enemies.pop(enemies.index(enemy))
			else:
				enemies.pop(enemies.index(enemy))
		if enemy.direction == 'ul':
			if enemy.rect.center[1] > -20:
				if enemy.rect.center[0] > -20:
					enemy.rect.center = (enemy.rect.center[0] - enemy.vel//2, enemy.rect.center[1] - enemy.vel//2)
				else:
					enemies.pop(enemies.index(enemy))
			else:
				enemies.pop(enemies.index(enemy))
		if enemy.direction == 'ur':
			if enemy.rect.center[1] < 1080:
				if enemy.rect.center[0] < 1920:
					enemy.rect.center = (enemy.rect.center[0] + enemy.vel//2, enemy.rect.center[1] - enemy.vel//2)
				else:
					enemies.pop(enemies.index(enemy))
			else:
				enemies.pop(enemies.index(enemy))


def main():
	global volume

	with open('score.txt', 'r') as file:
		best_score = int(file.read(1))

	RES = 1920, 1080
	ALPHA = 40
	ALPHA_FOR_START_SCREEN = 20
	alpha_surface = pg.Surface(RES)
	alpha_surface.set_alpha(ALPHA)
	alpha_surface_for_start_screen = pg.Surface(RES)
	alpha_surface_for_start_screen.set_alpha(ALPHA_FOR_START_SCREEN)

	font = pg.font.SysFont('impact', 40)

	#buttons [start, exit]
	center = win.get_rect().center
	start_button      = pg.Rect(*center, 0, 0).inflate(120, 50)
	start_button_text = font.render(str(f'START'), True, (255,255,255))

	exit_button       = pg.Rect(center[0], center[1] + 60, 0, 0).inflate(120, 50)
	exit_button_text  = font.render(str(f'EXIT'), True, (255,255,255))

	while True:
		start_screen = True
		while start_screen:
			
			win.blit(alpha_surface_for_start_screen, (0,0))
			best_score_text = font.render(str(f'{best_score}'), True, (255,255,255))

			point = pg.mouse.get_pos()
			start_button_collide = start_button.collidepoint(point)
			exit_button_coliide  = exit_button.collidepoint(point)
			
			if start_button_collide:
				start_button_color = (100,255,100)
			else:
				start_button_color = (0,200,0)

			if exit_button_coliide:
				exit_button_color = (255,100,100)
			else:
				exit_button_color = (255,0,0)

			pg.draw.rect(win, exit_button_color, exit_button)
			pg.draw.rect(win, start_button_color, start_button)
			win.blit(start_button_text, (W//2-50,H//2-25))
			win.blit(exit_button_text, (W//2-32,H//2+35))

			coursor = pg.draw.circle(win, (255,0,0), point, 5, 1)

			for event in pg.event.get():
				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 1 and start_button_collide:
						enemies.clear()
						start_screen = False
					if event.button == 1 and exit_button_coliide:
						with open('score.txt', 'r+') as file:
							file.write(str(best_score))
						pg.quit()
						sys.exit()

			pg.display.flip()

		pg.mixer.music.play(-1)

		hp = 3
		score = 0
		run = True
		while run:
			win.blit(alpha_surface, (0, 0))
			best_score_text = font.render(str(f'BEST SCORE: {best_score}'), True, (255,255,255))
			score_text = font.render(str(f'SCORE: {score}'), True, (255,255,255))
			for event in pg.event.get():
				if event.type == pg.QUIT:
					file.write(str(best_score))
					pg.quit()
					sys.exit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_LEFT:
						if volume > 0.01:
							volume -= 0.01
							pg.mixer.music.set_volume(volume)
					if event.key == pg.K_RIGHT:
						if volume < 1:
							volume += 0.01
							pg.mixer.music.set_volume(volume)
					if event.key == pg.K_SPACE:
						if P.speed == 1:
							P.speed = 10
						else:
							P.speed = 1

			mouse_pos = pg.mouse.get_pos()

			P = Player(win, player_sprite, player_pos)
			P.update()
			P.draw()

			EnemySpawn()
			EnemyMove()

			for enemy in enemies:
				enemy.draw()

			for enemy in enemies:
				if Collide(P.rect, enemy.rect):
					enemies.pop(enemies.index(enemy))
					hit_sound.play()
					hp -= 1
					if hp == 0:
						run = False
						start_screen = True
						with open('score.txt', 'r+') as file:
							file.write(str(best_score))
						pg.mixer.music.pause()


			win.blit(score_text, (5, 50))
			win.blit(best_score_text, (5, 5))
			score += 1
			if best_score < score:
				best_score = score

			pg.display.flip()
			clock.tick(120)


if __name__ == '__main__':
	main()