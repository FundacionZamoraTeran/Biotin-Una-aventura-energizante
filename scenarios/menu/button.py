import pygame
from scenarios.utils import utils

class Button(pygame.sprite.Sprite):
    """
       Acts as a button constructor, expects:
       x => X position,
       y => Y position,
       base_file => the base image the button will display
       transition_file => transition between states image
       end_file => final state image,
       width => the width the button should be
       height => the height the button should be
       folder => the folder where the images are in
    """
    def __init__(self, x,y, base_file, transition_file, end_file , width=100, height=100, folder = "menu"):
        #pygame Sprite class constructor
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.pos = (x, y)

        #set the states images
        self.base = utils.load_image(base_file, folder, -1, (width, height))
        self.transition = utils.load_image(transition_file, folder, -1, (width, height))
        self.end = utils.load_image(end_file, folder, -1, (width, height))

        #define the rects for all the sprite's states, _rect.x and _rect.y set the position of the objects
        self.base_rect = self.base.get_rect(topleft=self.pos)
        self.transition_rect = self.transition.get_rect(topleft=self.pos)
        self.end_rect = self.end.get_rect(topleft=self.pos)

    def update(self):
        pass

    def flip(self):
        self.base = pygame.transform.flip(self.base, 180, 0)
        self.transition = pygame.transform.flip(self.transition, 180, 0)
        self.end = pygame.transform.flip(self.end, 180, 0)
        return self