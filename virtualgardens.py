import json
import os
import pygame
import subprocess

pygame.init()

# Einstellungen
WIDTH, HEIGHT = 1250, 700  # 1875, 1050
SQUARE_SIZE = 50  # 75
ROWS, COLS = HEIGHT // SQUARE_SIZE, WIDTH // SQUARE_SIZE
JSON_FILE = "data.json"

FPS = 30
FONT = pygame.font.SysFont("comicsans", 30)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Garden")

MAP_FOLDER_PATH = "virtualgarden\\gardens\\"
MAPDATA_FILE_PATH = os.path.join(MAP_FOLDER_PATH, "gardens_data.json")
assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

placed_objects = []
loaded_images = {}


# Vegetationsdaten mit allen relevanten Pfaden
VEGETATION_DATA = {
    "City Park": {
        "ground": os.path.join(assets_path, "park_grass.png"),
        "objects": [
            {
                "name": "path",
                "image": os.path.join(assets_path, "park_path.png"),
                "cost": 2
            },
            {
                "name": "path_horizontal",
                "image": os.path.join(assets_path, "park_path_horizontal.png"),
                "cost": 2
            },
            {
                "name": "path_cross",
                "image": os.path.join(assets_path, "park_path_cross.png"),
                "cost": 2
            },
            {
                "name": "flowers",
                "image": os.path.join(assets_path, "park_flowers.png"),
                "cost": 2
            },
            {
                "name": "bench",
                "image": os.path.join(assets_path, "park_bench.png"),
                "cost": 4
            },
            {
                "name": "tree",
                "image": os.path.join(assets_path, "park_tree.png"),
                "cost": 8
            },
        ]
    },
    "Desert": {
        "ground": os.path.join(assets_path, "desert_sand.png"),
        "objects": [
            {
                "name": "bush",
                "image": os.path.join(assets_path, "desert_bush.png"),
                "cost": 2
            },
            {
                "name": "bush2",
                "image": os.path.join(assets_path, "desert_bush2.png"),
                "cost": 2
            },
            {
                "name": "cactus",
                "image": os.path.join(assets_path, "desert_cactus.png"),
                "cost": 4
            },
            {
                "name": "cactus2",
                "image": os.path.join(assets_path, "desert_cactus2.png"),
                "cost": 4
            },
            {
                "name": "skeleton",
                "image": os.path.join(assets_path, "desert_skeleton.png"),
                "cost": 8
            },
        ]
    },
    "Rainforest": {
        "ground": os.path.join(assets_path, "rainforest_ground.png"),
        "objects": [
            {
                "name": "flowers",
                "image": os.path.join(assets_path, "rainforest_flowers.png"),
                "cost": 2
            },
            {
                "name": "tree",
                "image": os.path.join(assets_path, "rainforest_tree.png"),
                "cost": 8
            },
            {
                "name": "trees",
                "image": os.path.join(assets_path, "rainforest_trees.png"),
                "cost": 10
            },
        ]
    }
}


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
        """
        Re-creates PlacedObject instances based on the garden_map.
        We only create them for indices > 0 (everything that's NOT ground).
        """
        placed_objects.clear()
        for y, row in enumerate(self.garden_map):
            for x, element in enumerate(row):
                if element != 0:
                    PlacedObject(
                        self.garden_objects[element],
                        (x * SQUARE_SIZE, y * SQUARE_SIZE)
                    )

    def draw_garden_map(self, win):
        # 1) Draw ground for every cell
        for y in range(ROWS):
            for x in range(COLS):
                ground_object = self.garden_objects[0]  # index 0 is ground
                win.blit(ground_object.image, (x * SQUARE_SIZE, y * SQUARE_SIZE))

        # 2) Draw placed objects (these are all indices > 0)
        for o in placed_objects:
            o.draw(win)

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


def load_garden_metadata():
    """
    Lädt den gesamten Inhalt der 'gardens_data.json' als Dictionary.
    Wenn die Datei nicht existiert oder leer ist, wird ein leeres Dictionary zurückgegeben.
    """
    if not os.path.isfile(MAPDATA_FILE_PATH):
        return {}
    
    try:
        with open(MAPDATA_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}
    return data


def save_garden_metadata(metadata):
    """
    Speichert das übergebene Dictionary `metadata` in der 'gardens_data.json'.
    """
    with open(MAPDATA_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)


def cleanup_garden_metadata():
    """
    Synchronisiert den Inhalt der gardens_data.json mit den vorhandenen .map-Dateien.
    
    1. Entfernt Einträge in metadata, zu denen keine .map-Datei mehr existiert.
    2. Fügt Einträge für neue .map-Dateien hinzu, die noch nicht in metadata stehen (optional).
    """
    # 1) Alle vorhandenen .map-Dateien sammeln
    all_map_files = [
        f for f in os.listdir(MAP_FOLDER_PATH) if f.endswith(".map")
    ]
    # Namen ohne .map
    all_garden_names = [os.path.splitext(f)[0] for f in all_map_files]

    # 2) Metadaten laden
    metadata = load_garden_metadata()  # Dictionary

    # 3) Einträge entfernen, die keine .map-Datei mehr besitzen
    to_remove = []
    for garden_name in metadata.keys():
        # Wenn garden_name nicht in all_garden_names => verwaister Eintrag
        if garden_name not in all_garden_names:
            to_remove.append(garden_name)

    for garden_name in to_remove:
        del metadata[garden_name]
        print(f"[Cleanup] Removed metadata entry '{garden_name}' (no corresponding .map file).")

    # 4) Einträge hinzufügen für neue .map-Dateien (optional)
    #    Falls man das möchte, kann man hier eine Standard-Vegetation oder None setzen.
    for garden_name in all_garden_names:
        if garden_name not in metadata:
            # Du kannst ein Standardobjekt definieren oder None zuweisen.
            metadata[garden_name] = {
                "vegetation": "Rainforest",  # z. B. als Default
                # Weitere Felder falls gewünscht
            }
            print(f"[Cleanup] Added metadata entry '{garden_name}' with default vegetation.")

    # 5) Speichern
    save_garden_metadata(metadata)


def choose_vegetation(win):
    """
    Zeigt ein kleines Menü mit den Vegetationen.
    Gibt den String ("City Park", "Desert" oder "Rainforest") zurück,
    oder None bei Abbruch.
    """
    vegetations = list(VEGETATION_DATA.keys())  # ["City Park", "Desert", "Rainforest"]
    
    run = True
    while run:
        win.fill((0, 0, 0))

        title_surf = FONT.render("Choose vegetation:", True, (255, 255, 255))
        win.blit(title_surf, (50, 50))

        y_offset = 100
        rect_list = []
        for vegetation in vegetations:
            text_surf = FONT.render(vegetation, True, (255, 255, 255))
            text_rect = text_surf.get_rect(topleft=(60, y_offset))
            rect_list.append((text_rect, vegetation))
            win.blit(text_surf, text_rect.topleft)
            y_offset += 40

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for (r, veg) in rect_list:
                    if r.collidepoint(mouse_x, mouse_y):
                        return veg  # gewählte Vegetation

    return None


def create_garden_objects(vegetation):
    """
    Erzeugt eine Liste an GardenObject-Instanzen basierend auf
    den Daten aus VEGETATION_DATA für die gewünschte Vegetation.
    """
    data = VEGETATION_DATA[vegetation]
    
    # 1. Zuerst den Boden als Objekt (Index 0)
    objects = [GardenObject("ground", data["ground"], cost=0)]
    
    # 2. Dann alle anderen Objekte
    for obj_data in data["objects"]:
        name = obj_data["name"]
        image = obj_data["image"]
        cost = obj_data["cost"]
        objects.append(GardenObject(name, image, cost))

    return objects


def draw_menu(win: pygame.Surface):
    win.fill((0, 0, 0))
    title_text = FONT.render("Virtual Garden", True, (255, 255, 255))
    new_garden_text = FONT.render("Create Garden", True, (255, 255, 255))
    load_garden_text = FONT.render("Load Garden", True, (255, 255, 255))
    quit_text = FONT.render("Back to Productivity Window", True, (255, 255, 255))

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
      - "quit"  bei Klick auf "Back to Productivity Window"
    """
    run = True
    while run:
        new_garden_rect, load_garden_rect, quit_rect = draw_menu(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "closed"

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
    Zeichnet das inventory am unteren Bildschirmrand und hebt das aktuell
    ausgewählte Objekt (selected_object_index) mit einem roten Rahmen hervor.
    Außerdem wird rechts unten am Icon der Preis angezeigt.
    """
    inventory_height = 60
    pygame.draw.rect(win, (50, 50, 50), (0, HEIGHT - inventory_height, WIDTH, inventory_height))

    icon_size = 50
    x_offset = 10
    y_offset = HEIGHT - inventory_height + 5

    # Liste der Rects für die inventory-Icons, um Klicks abzufangen
    icon_rects = []
    
    for i, obj in enumerate(garden_objects):
        icon_img = obj.image
        icon_rect = pygame.Rect(x_offset, y_offset, icon_size, icon_size)
        icon_rects.append(icon_rect)
        
        # Zeichne das Objekt-Icon
        win.blit(icon_img, icon_rect.topleft)

        # Kosten-Text in weiß rendern
        cost_text = FONT.render(str(obj.cost), True, (255, 255, 255))
        # Unten rechts ins Icon setzen:
        cost_text_rect = cost_text.get_rect(bottomright=(icon_rect.right, icon_rect.bottom))
        win.blit(cost_text, cost_text_rect)

        # Roter Rahmen um das aktuell ausgewählte Objekt
        if i == selected_object_index:
            pygame.draw.rect(win, (255, 0, 0), icon_rect, 2)

        # Nächstes Icon rückt nach rechts
        x_offset += icon_size + 10

    return icon_rects


def create_new_garden():
    # Vegetation auswählen
    vegetation_choice = choose_vegetation(WIN)
    if not vegetation_choice:
        return None  # Falls der User abbricht
    
    # Passende GardenObjects erzeugen
    garden_objects = create_garden_objects(vegetation_choice)
    
    # Name für neuen Garten
    garden_name = text_input_dialog(WIN, "Enter a name for your new garden:")
    if not garden_name:
        return None
    
    # Metadaten laden und erweitern
    metadata = load_garden_metadata()
    metadata[garden_name] = {"vegetation": vegetation_choice}
    save_garden_metadata(metadata)
    
    map_file = MAP_FOLDER_PATH + garden_name + ".map"
    garden = Garden(map_file, garden_objects)
    return garden


def load_existing_garden():
    chosen_file = load_garden_dialog(WIN)  # z. B. "MeinGarten.map"
    if not chosen_file:
        return None
    
    # Dateiendung wegnehmen, um den "Namen" zu erhalten
    garden_name = os.path.splitext(chosen_file)[0]
    
    # Metadaten laden
    metadata = load_garden_metadata()
    
    # Vegetation herausfinden (Standardwert wenn nicht gefunden: "Rainforest")
    # Du kannst auch None zurückgeben lassen und abfragen, was du tun willst.
    vegetation_choice = metadata.get(garden_name, {}).get("vegetation", "Rainforest")
    
    # Jetzt haben wir die korrekte Vegetation
    garden_objects = create_garden_objects(vegetation_choice)

    map_file = MAP_FOLDER_PATH + chosen_file
    garden = Garden(map_file, garden_objects)
    return garden


def save_json_data(available_points : int):
    # save points to json file
    if not os.path.exists(JSON_FILE):
        return False
    else:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
            data["available_points"] = available_points
            with open(JSON_FILE, "w") as file:
                json.dump(data, file, indent=4)
                return True
    return False


def load_json_data() -> int:
    if not os.path.exists(JSON_FILE):
        return 0
    else:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
            return data["available_points"]
        return 0


def draw_garden_map_with_ui(win, garden, available_points, garden_objects, selected_object_index):
    # Zuerst Garten zeichnen
    garden.draw_garden_map(win)
    
    # Punktestand oben links
    points_text = FONT.render(f"Points: {available_points}", True, (255, 255, 255))
    win.blit(points_text, (10, 10))
    
    # Dann inventory
    icon_rects = draw_inventory(win, garden_objects, selected_object_index)
    
    pygame.display.update()
    return icon_rects


def main():
    # Cleanup metadata right at the start
    cleanup_garden_metadata()
    
    # create variables
    clock = pygame.time.Clock()
    available_points = load_json_data()
    garden = None
    user_closed_window = False  # flag to see if user closed the window by hitting "x"
    
    while True:
        if user_closed_window:
            break  # close game
        
        action = main_menu()
        if action == "closed":
            break
        elif action == "quit":
            subprocess.Popen(["python", "main.py"])  # open gui
            break  # close game
        elif action == "new":
            garden = create_new_garden()
            if not garden:
                break
        elif action == "load":
            garden = load_existing_garden()
            if not garden:
                break
        else:
            continue
        
        # Index des aktuell ausgewählten Objekts im inventory
        selected_object_index = 0
        running = True

        while running:
            clock.tick(FPS)

            icon_rects = draw_garden_map_with_ui(WIN, garden, available_points,
                                                 garden.garden_objects, selected_object_index)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    user_closed_window = True  # user clicked "x"
                    running = False
                    break  # close while loop
                if not user_closed_window:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Linksklick
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            clicked_on_inventory = False
                            # inventory-Klick
                            for i, rect in enumerate(icon_rects):
                                if rect.collidepoint(mouse_x, mouse_y):
                                    selected_object_index = i
                                    clicked_on_inventory = True
                                    break
                            # Platzieren des Objekts
                            if not clicked_on_inventory:
                                # Kosten berechnen und prüfen
                                selected_obj = garden.garden_objects[selected_object_index]
                                cost = selected_obj.cost
                                if available_points >= cost:
                                    available_points -= cost
                                    garden.place_object(selected_object_index)
                                    garden.update_garden_map()
                                else:
                                    print("Not enough points!")  # oder irgendeine andere Meldung

    # save data before closing the window
    save_json_data(available_points)
    try:
        garden.save_garden_map()  # type: ignore
    except AttributeError:
        pass
    pygame.quit()


if __name__ == "__main__":
    main()
