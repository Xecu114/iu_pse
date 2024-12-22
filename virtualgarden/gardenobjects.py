import pygame
from ..common.constants import SQUARE_SIZE

placed_objects = []
loaded_images = {}


class GardenObject:
    def __init__(self, name, image):
        self.name = name
        if image in loaded_images:
            self.image = loaded_images[image]
        else:
            self.image = pygame.transform.scale(pygame.image.load(image),
                                                (SQUARE_SIZE, SQUARE_SIZE))
            loaded_images[image] = self.image


class PlacedObject:
    def __init__(self, garden_object, location):
        self.garden_object = garden_object
        self.location = location
        placed_objects.append(self)

    def delete(self):
        placed_objects.remove(self)
        
    def draw(self, win):
        win.blit(self.garden_object.image, self.location)