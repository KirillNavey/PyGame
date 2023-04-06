import pygame as pg

RES = W, H = 1920, 1080
ALPHA = 1
FPS = 120
HUE_SPEED = 0.1
HUE = 0.1

win = pg.display.set_mode(RES, pg.FULLSCREEN)
#pg.mouse.set_visible(False)

alpha_surface = pg.Surface(RES)
alpha_surface.set_alpha(ALPHA)

clock = pg.time.Clock()
run = True
while run:
	win.blit(alpha_surface, (0,0))
	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False

	mx, my = mouse_pos = pg.mouse.get_pos()

	if HUE < 360:
		HUE += HUE_SPEED
	if HUE >= 360:
		HUE = 0.0

	color = pg.Color(0)
	color.hsla = (HUE, 100, 50, 100)

	mouse_pressed = pg.mouse.get_pressed()
	for mouse in mouse_pressed:
		if mouse == 1:
			draw_circle = pg.draw.circle(win, color, mouse_pos, 25, 0)

	pg.display.update()
	clock.tick(FPS)