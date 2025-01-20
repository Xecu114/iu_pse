import json
import os
import pygame
import subprocess
from src.gardenobjects import GardenObject
from src.garden import Garden
from src.constants import GAME_WIDTH, GAME_HEIGHT, SQUARE_SIZE, \
                             JSON_FILE, ASSETS_PATH, MAP_FOLDER_PATH, MAPDATA_FILE_PATH

# initialize pygame
pygame.init()
FPS = 30
FONT = pygame.font.SysFont("comicsans", 30)
WIN = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Virtual Garden")


# vegetation data with all relevant paths
VEGETATION_DATA = {
    "City Park": {
        "ground": os.path.join(ASSETS_PATH, "park_grass.png"),
        "objects": [
            {
                "name": "path",
                "image": os.path.join(ASSETS_PATH, "park_path.png"),
                "cost": 2
            },
            {
                "name": "path_horizontal",
                "image": os.path.join(ASSETS_PATH, "park_path_horizontal.png"),
                "cost": 2
            },
            {
                "name": "path_cross",
                "image": os.path.join(ASSETS_PATH, "park_path_cross.png"),
                "cost": 2
            },
            {
                "name": "flowers",
                "image": os.path.join(ASSETS_PATH, "park_flowers.png"),
                "cost": 2
            },
            {
                "name": "bench",
                "image": os.path.join(ASSETS_PATH, "park_bench.png"),
                "cost": 4
            },
            {
                "name": "tree",
                "image": os.path.join(ASSETS_PATH, "park_tree.png"),
                "cost": 8
            },
        ]
    },
    "Desert": {
        "ground": os.path.join(ASSETS_PATH, "desert_sand.png"),
        "objects": [
            {
                "name": "bush",
                "image": os.path.join(ASSETS_PATH, "desert_bush.png"),
                "cost": 2
            },
            {
                "name": "bush2",
                "image": os.path.join(ASSETS_PATH, "desert_bush2.png"),
                "cost": 2
            },
            {
                "name": "cactus",
                "image": os.path.join(ASSETS_PATH, "desert_cactus.png"),
                "cost": 4
            },
            {
                "name": "cactus2",
                "image": os.path.join(ASSETS_PATH, "desert_cactus2.png"),
                "cost": 4
            },
            {
                "name": "skeleton",
                "image": os.path.join(ASSETS_PATH, "desert_skeleton.png"),
                "cost": 8
            },
        ]
    },
    "Rainforest": {
        "ground": os.path.join(ASSETS_PATH, "rainforest_ground.png"),
        "objects": [
            {
                "name": "flowers",
                "image": os.path.join(ASSETS_PATH, "rainforest_flowers.png"),
                "cost": 2
            },
            {
                "name": "tree",
                "image": os.path.join(ASSETS_PATH, "rainforest_tree.png"),
                "cost": 8
            },
            {
                "name": "trees",
                "image": os.path.join(ASSETS_PATH, "rainforest_trees.png"),
                "cost": 10
            },
        ]
    }
}


class ResourceManager:
    def __init__(self):
        self._images = {}

    def get_image(self, path):
        """
        Loads (and caches) an image, scaled to (SQUARE_SIZE, SQUARE_SIZE).
        """
        if path not in self._images:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            self._images[path] = img
        return self._images[path]


def load_garden_metadata():
    """
    Loads the entire content of 'gardens_data.json' as a dictionary.
    If the file does not exist or is empty, an empty dictionary is returned.
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
    Saves the passed dictionary `metadata` in the 'gardens_data.json'.
    """
    with open(MAPDATA_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)


def cleanup_garden_metadata():
    """
    Synchronizes the content of gardens_data.json with the existing .map files.
    
    1. removes entries in metadata for which a .map file no longer exists.
    2. adds entries for new .map files that are not yet in metadata.
    """
    # collect .map-files
    all_map_files = [
        f for f in os.listdir(MAP_FOLDER_PATH) if f.endswith(".map")
    ]
    # names without ".map"
    all_garden_names = [os.path.splitext(f)[0] for f in all_map_files]

    metadata = load_garden_metadata()  # Dictionary

    # remove entries that no longer have a .map file
    to_remove = []
    for garden_name in metadata.keys():
        # if garden_name is not in all_garden_names => orphaned entry
        if garden_name not in all_garden_names:
            to_remove.append(garden_name)

    for garden_name in to_remove:
        del metadata[garden_name]
        print(f"[Cleanup] Removed metadata entry '{garden_name}' (no corresponding .map file).")

    # Add entries for new .map files
    for garden_name in all_garden_names:
        if garden_name not in metadata:
            metadata[garden_name] = {"vegetation": "City Park", }
            print(f"[Cleanup] Added metadata entry '{garden_name}' with default vegetation.")

    save_garden_metadata(metadata)


def choose_vegetation(win: pygame.Surface):
    """
    Shows a small menu with the vegetation.
    Returns the string (“City Park”, “Desert” or “Rainforest”)
    or None if canceled.
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
                        return veg  # return chosen vegetation

    return None


def create_garden_objects(vegetation, resource_manager):
    """
    Creates a list of GardenObject instances based on data from
    the data from VEGETATION_DATA for the desired vegetation.
    resource_manager is required to load the images
    """
    data = VEGETATION_DATA[vegetation]
    
    objects = [GardenObject("ground", data["ground"], cost=0, resource_manager=resource_manager)]
    
    for obj_data in data["objects"]:
        name = obj_data["name"]
        image = obj_data["image"]
        cost = obj_data["cost"]
        objects.append(GardenObject(name, image, cost, resource_manager=resource_manager))

    return objects


def draw_menu(win: pygame.Surface):
    """
    Draws the main menu interface on the given surface.

    Returns:
        A tuple containing the rectangles for
        the "Create Garden", "Load Garden" and "Back to Productivity Window" text areas
    """
    win.fill((0, 0, 0))
    title_text = FONT.render("Virtual Garden", True, (255, 255, 255))
    new_garden_text = FONT.render("Create Garden", True, (255, 255, 255))
    load_garden_text = FONT.render("Load Garden", True, (255, 255, 255))
    quit_text = FONT.render("Back to Productivity Window", True, (255, 255, 255))

    title_rect = title_text.get_rect(center=(GAME_WIDTH // 2, 100))
    new_garden_rect = new_garden_text.get_rect(center=(GAME_WIDTH // 2, 250))
    load_garden_rect = load_garden_text.get_rect(center=(GAME_WIDTH // 2, 350))
    quit_rect = quit_text.get_rect(center=(GAME_WIDTH // 2, 450))
    
    win.blit(title_text, title_rect.topleft)
    win.blit(new_garden_text, new_garden_rect.topleft)
    win.blit(load_garden_text, load_garden_rect.topleft)
    win.blit(quit_text, quit_rect.topleft)
    
    pygame.display.update()
    return new_garden_rect, load_garden_rect, quit_rect


def main_menu():
    """
    Displays the main menu, handles user interactions and
    returns a corresponding string based on the user's selection:
    - "new" for Create Garden
    - "load" for Load Garden
    - "quit" for Back to Productivity Window
    - "closed" if the window is closed
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


def text_input_dialog(win: pygame.Surface, prompt):
    """
    Displays an input field in which the user can enter a name.
    The entry is confirmed with ENTER and then returned.
    """
    user_text = ""
    input_active = True
    error_message = ""

    while input_active:
        win.fill((0, 0, 0))

        # Render prompt
        prompt_surf = FONT.render(prompt, True, (255, 255, 255))
        win.blit(prompt_surf, (50, 50))

        # Render input box
        input_surf = FONT.render(user_text, True, (255, 255, 255))
        input_rect = pygame.Rect(50, 100, 400, 40)  # rect to cover input
        pygame.draw.rect(win, (100, 100, 100), input_rect)
        win.blit(input_surf, (input_rect.x + 5, input_rect.y + 5))

        # Render error message if any
        if error_message:
            error_surf = FONT.render(error_message, True, (255, 0, 0))
            win.blit(error_surf, (50, 150))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not user_text.strip():
                        error_message = "Name cannot be empty."
                    elif len(user_text) > 40:
                        error_message = "Name cannot exceed 40 characters."
                    else:
                        input_active = False
                        return user_text  # Valid name entered
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:  # normal letter, number, symbol
                    if len(user_text) < 40:  # Prevent adding more than 40 characters
                        user_text += event.unicode

    return user_text


def load_garden_dialog(win: pygame.Surface):
    """
    Scans the current directory for .map files and displays them as a list.
    When clicked, the file name is returned.
    """
    # collect .map files
    map_files = [f for f in os.listdir(MAP_FOLDER_PATH) if f.endswith('.map')]

    run = True

    while run:
        win.fill((0, 0, 0))

        title_surf = FONT.render("Choose a garden to load (click on name):", True, (255, 255, 255))
        win.blit(title_surf, (50, 50))

        y_offset = 100
        # show file names
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
                # check, if a filename was clicked
                for (r, fn) in rect_list:
                    if r.collidepoint(mouse_x, mouse_y):
                        return fn
    
    return None


def draw_inventory(win: pygame.Surface, garden_objects, selected_object_index):
    """
    Draws the inventory at the bottom of the screen and highlights the currently
    selected object (selected_object_index) with a red frame.
    The price is also displayed at the bottom right of the icon.
    """
    inventory_height = 60
    pygame.draw.rect(win, (50, 50, 50), (0, GAME_HEIGHT - inventory_height, GAME_WIDTH, inventory_height))

    icon_size = 50
    x_offset = 10
    y_offset = GAME_HEIGHT - inventory_height + 5

    # List of rects for the inventory icons to intercept clicks
    icon_rects = []
    
    for i, obj in enumerate(garden_objects):
        icon_img = obj.image
        icon_rect = pygame.Rect(x_offset, y_offset, icon_size, icon_size)
        icon_rects.append(icon_rect)
        
        # draw object-icon
        win.blit(icon_img, icon_rect.topleft)

        # draw costs in white
        cost_text = FONT.render(str(obj.cost), True, (255, 255, 255))
        cost_text_rect = cost_text.get_rect(bottomright=(icon_rect.right, icon_rect.bottom))
        win.blit(cost_text, cost_text_rect)

        # draw red frame around current object
        if i == selected_object_index:
            pygame.draw.rect(win, (255, 0, 0), icon_rect, 2)

        # shift next icon to the right
        x_offset += icon_size + 10

    return icon_rects


def create_new_garden(resource_manager):
    """
    Create a new garden, by selecting a vegetation,
    creating matching garden_objects, set a name and load and save metadata
    Returns:
        - new Garden() instance
        - None: if something went wrong or user trys to close the app
    """
    vegetation_choice = choose_vegetation(WIN)
    if not vegetation_choice:
        return None  # Break
    
    garden_objects = create_garden_objects(vegetation_choice, resource_manager)
    
    garden_name = text_input_dialog(WIN, "Enter a name for your new garden:")
    if not garden_name:
        return None  # Break
    
    metadata = load_garden_metadata()
    metadata[garden_name] = {"vegetation": vegetation_choice}
    save_garden_metadata(metadata)
    
    map_file = MAP_FOLDER_PATH + garden_name + ".map"
    garden = Garden(map_file, garden_objects)
    return garden


def load_existing_garden(resource_manager):
    """
    Load an existing garden
    Returns:
        - Garden() instance
        - None: if something went wrong or user trys to close the app
    """
    chosen_file = load_garden_dialog(WIN)
    if not chosen_file:
        return None
    
    garden_name = os.path.splitext(chosen_file)[0]
    
    metadata = load_garden_metadata()
    
    # get vegetation (defaults to "Park")
    vegetation_choice = metadata.get(garden_name, {}).get("vegetation", "City Park")
    
    # create corresponding garden_objects
    garden_objects = create_garden_objects(vegetation_choice, resource_manager)

    map_file = MAP_FOLDER_PATH + chosen_file
    garden = Garden(map_file, garden_objects)
    return garden


def save_json_data(available_points : int):
    """
    Write "available_points" back into the json file
    Returns True if successful
    """
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
    """
    Read "available_points" from the json file
    Returns the currently available points
    """
    if not os.path.exists(JSON_FILE):
        return 0
    else:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
            return data["available_points"]
        return 0


def draw_garden_map_with_ui(win: pygame.Surface, garden: Garden,
                            available_points, garden_objects, selected_object_index):
    """
    Draw the garden with point score and inventory
    """
    # First draw garden
    garden.draw_garden_map(win)
    
    # Draw points top left
    points_text = FONT.render(f"Points: {available_points}", True, (255, 255, 255))
    win.blit(points_text, (10, 10))
    
    # Draw inventory
    icon_rects = draw_inventory(win, garden_objects, selected_object_index)
    
    pygame.display.update()
    return icon_rects


def main():
    # Cleanup metadata right at the start
    cleanup_garden_metadata()
    
    # create variables and instances
    resource_manager = ResourceManager()
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
            garden = create_new_garden(resource_manager)
            if not garden:
                break
        elif action == "load":
            garden = load_existing_garden(resource_manager)
            if not garden:
                break
        else:
            continue
        
        # Index of the currently selected object in the inventory
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
                        if event.button == 1:  # Left-click
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            clicked_on_inventory = False
                            # inventory-click
                            for i, rect in enumerate(icon_rects):
                                if rect.collidepoint(mouse_x, mouse_y):
                                    selected_object_index = i
                                    clicked_on_inventory = True
                                    break
                            # Place an object
                            if not clicked_on_inventory:
                                # Calculate costs and validate
                                selected_obj = garden.garden_objects[selected_object_index]
                                cost = selected_obj.cost
                                if available_points >= cost:
                                    available_points -= cost
                                    garden.place_object(selected_object_index)
                                    garden.update_garden_map()
                                else:
                                    print("Not enough points!")  # show only in debugging window
                                # save garden data
                                garden.save_garden_map()

    # save data before closing the window
    save_json_data(available_points)
    try:
        garden.save_garden_map()  # type: ignore
    except AttributeError:
        pass
    pygame.quit()
    return


if __name__ == "__main__":
    main()
    print("See you soon")