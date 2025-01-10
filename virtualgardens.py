import pygame
import os

pygame.init()

# Einstellungen
WIDTH, HEIGHT = 1280, 720
SQUARE_SIZE = 50
ROWS, COLS = HEIGHT // SQUARE_SIZE, WIDTH // SQUARE_SIZE

FPS = 30
FONT = pygame.font.SysFont("comicsans", 30)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Garden")

MAP_FOLDER_PATH = "virtualgarden\\gardens\\"
assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

IMGDIR_GRASS = str(os.path.join(assets_path, "grass.png"))
IMGDIR_TREE = str(os.path.join(assets_path, "Regenwald_Baum.jpg"))
IMGDIR_FLOWER = str(os.path.join(assets_path, "Regenwald_Blume.jpg"))

placed_objects = []
loaded_images = {}


class GardenObject:
    def __init__(self, name, image):
        self.name = name
        if image in loaded_images:
            self.image = loaded_images[image]
        else:
            img = pygame.image.load(image)
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


class Garden:
    def __init__(self, map_file, garden_objects):
        self.map_file = map_file
        self.garden_objects = garden_objects
        self.garden_map = []
        self.init_garden_map()

    def init_garden_map(self):
        # Leere zunächst die globale Liste platzierter Objekte
        placed_objects.clear()

        # Prüfe, ob es die Datei schon gibt
        if os.path.isfile(self.map_file):
            with open(self.map_file, 'r') as f:
                lines = f.read().splitlines()
            for line in lines:
                row_data = [int(ch) for ch in line]
                self.garden_map.append(row_data)
        else:
            # Falls nein, erstelle einen leeren Garten (nur 0)
            for _ in range(ROWS):
                row_data = [0] * COLS
                self.garden_map.append(row_data)

        self.update_garden_map()

    def update_garden_map(self):
        placed_objects.clear()
        for y, row in enumerate(self.garden_map):
            for x, element in enumerate(row):
                PlacedObject(
                    self.garden_objects[element],
                    (x * SQUARE_SIZE, y * SQUARE_SIZE)
                )

    def draw_garden_map(self, win):
        for o in placed_objects:
            o.draw(win)
        pygame.display.update()

    def save_garden_map(self):
        with open(self.map_file, 'w') as f:
            for row in self.garden_map:
                f.write("".join(map(str, row)) + "\n")

    def place_object(self, object_index):
        """
        Platziert das Objekt (object_index) an der aktuellen Mausposition.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = mouse_y // SQUARE_SIZE
        col = mouse_x // SQUARE_SIZE
        self.garden_map[row][col] = object_index


def draw_menu(win: pygame.Surface):
    win.fill((0, 0, 0))
    title_text = FONT.render("Virtual Garden", True, (255, 255, 255))
    new_garden_text = FONT.render("Create Garden", True, (255, 255, 255))
    load_garden_text = FONT.render("Load Garden", True, (255, 255, 255))
    quit_text = FONT.render("Quit", True, (255, 255, 255))

    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    new_garden_rect = new_garden_text.get_rect(center=(WIDTH // 2, 250))
    load_garden_rect = load_garden_text.get_rect(center=(WIDTH // 2, 350))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, 450))
    
    win.blit(title_text, title_rect.topleft)
    win.blit(new_garden_text, new_garden_rect.topleft)
    win.blit(load_garden_text, load_garden_rect.topleft)
    win.blit(quit_text, quit_rect.topleft)
    
    pygame.display.update()
    return new_garden_rect, load_garden_rect, quit_rect


def main_menu():
    """
    Gibt einen String zurück:
      - "new"   bei Klick auf "Create Garden"
      - "load"  bei Klick auf "Load Garden"
      - "quit"  bei Klick auf "Quit"
    """
    run = True
    while run:
        new_garden_rect, load_garden_rect, quit_rect = draw_menu(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if new_garden_rect.collidepoint(mouse_x, mouse_y):
                    return "new"
                elif load_garden_rect.collidepoint(mouse_x, mouse_y):
                    return "load"
                elif quit_rect.collidepoint(mouse_x, mouse_y):
                    return "quit"


def text_input_dialog(win, prompt):
    """
    Zeigt ein Eingabefeld an, in das der Nutzer einen Namen eingeben kann.
    Die Eingabe wird mit ENTER bestätigt und dann zurückgegeben.
    """
    user_text = ""
    input_active = True

    while input_active:
        win.fill((0, 0, 0))

        # Prompt (Aufforderung)
        prompt_surf = FONT.render(prompt, True, (255, 255, 255))
        win.blit(prompt_surf, (50, 50))

        # Nutzer-Eingabe
        input_surf = FONT.render(user_text, True, (255, 255, 255))
        # Kleines Rechteck, um Eingabe zu hinterlegen
        input_rect = pygame.Rect(50, 100, 400, 40)
        pygame.draw.rect(win, (100, 100, 100), input_rect)
        win.blit(input_surf, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Abbruch

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    # Normaler Buchstabe/Ziffer etc.
                    user_text += event.unicode

    return user_text


def load_garden_dialog(win):
    """
    Scannt das aktuelle Verzeichnis nach .map-Dateien und zeigt sie als Liste an.
    Bei Klick wird der Dateiname zurückgegeben.
    """
    # Alle .map Dateien sammeln
    map_files = [f for f in os.listdir(MAP_FOLDER_PATH) if f.endswith('.map')]
    # Falls du sie in einem Unterordner hast, musst du den Pfad anpassen.

    run = True

    while run:
        win.fill((0, 0, 0))

        title_surf = FONT.render("Choose a garden to load (click on name):", True, (255, 255, 255))
        win.blit(title_surf, (50, 50))

        y_offset = 100
        # Zeichne die Dateinamen
        rect_list = []
        for i, filename in enumerate(map_files):
            text_surf = FONT.render(filename, True, (255, 255, 255))
            text_rect = text_surf.get_rect(topleft=(60, y_offset))
            rect_list.append((text_rect, filename))
            win.blit(text_surf, text_rect.topleft)
            y_offset += 40

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Prüfe, ob in einen Dateinamen geklickt wurde
                for (r, fn) in rect_list:
                    if r.collidepoint(mouse_x, mouse_y):
                        return fn  # Dateiname zurückgeben
    
    return None


def draw_inventory(win, garden_objects, selected_object_index):
    """
    Zeichnet das Inventar am unteren Bildschirmrand und hebt das aktuell
    ausgewählte Objekt (selected_object_index) mit einem roten Rahmen hervor.
    """
    inventory_height = 60
    pygame.draw.rect(win, (50, 50, 50), (0, HEIGHT - inventory_height, WIDTH, inventory_height))

    icon_size = 50
    x_offset = 10
    y_offset = HEIGHT - inventory_height + 5

    # Liste der Rects für die Inventar-Icons, um Klicks abzufangen
    icon_rects = []
    
    for i, obj in enumerate(garden_objects):
        icon_img = obj.image
        icon_rect = pygame.Rect(x_offset, y_offset, icon_size, icon_size)
        icon_rects.append(icon_rect)
        
        # Zeichne das Objekt-Icon
        win.blit(icon_img, (x_offset, y_offset))

        # Roter Rahmen um das aktuell ausgewählte Objekt
        if i == selected_object_index:
            pygame.draw.rect(win, (255, 0, 0), icon_rect, 2)

        # Nächstes Icon rückt nach rechts
        x_offset += icon_size + 10

    return icon_rects


def main():
    # Verfügbare Objekte
    garden_objects = [
        GardenObject("grass", IMGDIR_GRASS),   # Index 0
        GardenObject("tree", IMGDIR_TREE),     # Index 1
        GardenObject("flower", IMGDIR_FLOWER)  # Index 2
    ]

    clock = pygame.time.Clock()

    while True:
        action = main_menu()
        if action == "quit":
            break

        if action == "new":
            # Name für neuen Garten
            garden_name = text_input_dialog(WIN, "Enter a name for your new garden:")
            if not garden_name:
                continue
            map_file = MAP_FOLDER_PATH + garden_name + ".map"
            garden = Garden(map_file, garden_objects)

        elif action == "load":
            # Wähle eine vorhandene .map aus
            chosen_file = load_garden_dialog(WIN)
            if not chosen_file:
                continue
            map_file = MAP_FOLDER_PATH + chosen_file
            garden = Garden(map_file, garden_objects)

        # Index des aktuell ausgewählten Objekts im Inventar
        selected_object_index = 0
        running = True

        while running:
            clock.tick(FPS)

            # Zuerst Garten und Inventar zeichnen
            garden.draw_garden_map(WIN)
            icon_rects = draw_inventory(WIN, garden_objects, selected_object_index)
            pygame.display.update()

            # Events abfangen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Linksklick
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        clicked_on_inventory = False

                        # Prüfen, ob Klick auf ein Inventar-Icon
                        for i, rect in enumerate(icon_rects):
                            if rect.collidepoint(mouse_x, mouse_y):
                                selected_object_index = i
                                clicked_on_inventory = True
                                break

                        # Wenn nicht auf Inventar geklickt -> platziere Objekt im Garten
                        if not clicked_on_inventory:
                            garden.place_object(selected_object_index)
                            garden.update_garden_map()

        # Garden speichern, bevor wir das nächste Menü/Garden laden
        garden.save_garden_map()

    pygame.quit()


if __name__ == "__main__":
    main()
