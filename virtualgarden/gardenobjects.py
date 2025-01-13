import pygame
from common.constants import SQUARE_SIZE


class GardenObject:
    def __init__(self, name, image, cost: int):
        self.name = name
        self.cost = cost
        if image in loaded_images:
            self.image = loaded_images[image]
        else:
            img = pygame.image.load(image).convert_alpha()
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            loaded_images[image] = img
            self.image = img


class PlacedObject:
    def __init__(self, garden_object, location):
        self.garden_object = garden_object
        self.location = location
        placed_objects.append(self)

    def delete(self):
        placed_objects.remove(self)
        
    def draw(self, win):
        win.blit(self.garden_object.image, self.location)
