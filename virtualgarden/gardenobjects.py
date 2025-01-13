

class GardenObject:
    """
    Repräsentiert einen Objekttyp im Garten (z.B. Baum, Bank, etc.).
    Enthält das geladene Bild und die Kosten.
    """
    def __init__(self, name, image_path, cost, resource_manager):
        self.name = name
        self.cost = cost
        # Bild wird über ResourceManager bezogen (kein globales loaded_images)
        self.image = resource_manager.get_image(image_path)


class PlacedObject:
    """
    Jedes platzierte Objekt kennt seinen Garden, um sich selbst eintragen/entfernen zu können,
    und das zugrunde liegende GardenObject (Bild, Kosten) + seine Position.
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
