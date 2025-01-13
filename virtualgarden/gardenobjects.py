

class GardenObject:
    """
    Represents an object type in the garden (e.g. tree, bench, etc.).
    Contains the loaded image and the cost.
    """
    def __init__(self, name, image_path, cost, resource_manager):
        self.name = name
        self.cost = cost
        # get the image from ResourceManager
        self.image = resource_manager.get_image(image_path)


class PlacedObject:
    """
    Each placed object knows its garden in order to be able to enter/remove itself
    and the underlying GardenObject (image, cost) + its position.
    """
    def __init__(self, garden, garden_object, location):
        self.garden = garden
        self.garden_object = garden_object
        self.location = location
        self.garden.placed_objects.append(self)

    def delete(self):
        self.garden.placed_objects.remove(self)

    def draw(self, win):
        win.blit(self.garden_object.image, self.location)
