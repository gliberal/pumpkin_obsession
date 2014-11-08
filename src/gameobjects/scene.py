# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from utils import ImageLoader, MovieLoader

class Scene():
	base_title = "Pumpkin obsession"
	scene_default_width = 640
	scene_default_height = 480
	
	def __init__(self, width = None, height=None):
		if (width is None) | (height is None):
			self.screen = pygame.display.set_mode(( self.scene_default_width , self.scene_default_height ))
		else:
			self.screen = pygame.display.set_mode(( width , height ))
		pygame.display.set_caption(self.base_title)
		pygame.display.set_icon(ImageLoader.get_single_sprite("SPRITE_PUMPKIN_ICO"))
	
	def update_title(self, text):
		""" Update the window title by adding the text argument to the base title """
		pygame.display.set_caption(self.base_title + " - " + text)

	def toggle_fullscreen(self):
		""" Switch to fullscreen mode """
		pygame.display.toggle_fullscreen()

	def clear_screen(self):
		""" Erase everything from the screen and set a background color """
		self.screen.fill((0, 0, 0))
		
class TransitionScene(Scene):
	def __init__(self, img_code):
		Scene.__init__(self)
		self.image = ImageLoader.get_image(img_code)
		self.image = pygame.transform.scale(self.image, (self.screen.get_width(), self.screen.get_height()))

	def display(self):
		""" Display the image """
		self.screen.blit(self.image, self.image.get_rect())

class MovieScene(Scene):
	def __init__(self, video_code):
		Scene.__init__(self)
		self.movie = MovieLoader.get_movie("MOVIE_CELISOFT_INTRO")
		self.movie.set_display(self.screen, self.screen.get_rect())

	def start(self):
		""" Start playing the movie """
		self.movie.play()

	def is_movie_playing(self):
		""" Check if the movie is still playing (True) or not (False) """
		return self.movie.get_busy()

	def stop(self):
		""" Stop the movie and set to None the movie attribute in order to avoid segfault """
		self.movie.stop()
		self.movie = None
		
class MenuScene(Scene):	
	def __init__(self, bg_code):
		Scene.__init__(self)

		self.menuentries = {}
		self.menu_size = 0
		self.background = ImageLoader.get_image(bg_code)
		self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))

	def add_menu_entry(self, menuEntry):
		""" Add a menu entry """
		self.menuentries.update({self.menu_size: menuEntry})
		self.menu_size += 1

	def display(self):
		""" Display the menu, that's to say all menu entries """
		self.screen.blit(self.background, self.background.get_rect())
		pos_y = 0
		for menuentry_key, menuentry in self.menuentries.items():
			pos_y = self.screen.get_height()/3 + (menuentry_key * menuentry.getPixelStep())
			menuentry.display(self.screen, self.screen.get_width()/2, pos_y)

class MenuSceneEntry():
	font_type = None
	font_size = 40
	font_color = (255, 255, 255)
	
	def __init__(self, text, command = None):
		self.font = pygame.font.Font(self.font_type, self.font_size)
		self.text = self.font.render(text, True, self.font_color)

	def getPixelStep(self):
		""" Return the vertical step between menu entries """
		return self.font_size + 5
		
	def display(self, screen, x, y):
		""" Display the menu entry """
		text_rect = self.text.get_rect(centerx=x, centery=y)
		screen.blit(self.text, text_rect)	

class GameScene(Scene):
	def __init__(self):
		Scene.__init__(self)

		