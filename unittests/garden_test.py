import unittest
from src.garden import Garden
from src.constants import ROWS, COLS
from unittest.mock import patch, mock_open, MagicMock


class MockGardenObject:
    """
    Mock für Gartenobjekte
    Hat nur ein "image" Attribut haben, das man an Pygame weitergeben kann.
    """
    def __init__(self, image=None):
        self.image = image


class TestGarden(unittest.TestCase):

    def setUp(self):
        self.map_file = "test_map.map"
        self.garden_objects = {
            0: MockGardenObject(image=MagicMock(name="GroundImage")),
            1: MockGardenObject(image=MagicMock(name="TreeImage")),
            2: MockGardenObject(image=MagicMock(name="FlowerImage"))
        }

    @patch("os.path.isfile", return_value=False)
    def test_init_garden_map_no_file(self, mock_isfile):
        """
        Testet, ob init_garden_map eine leere (nur Nullen)
        garden_map erstellt, wenn die Datei nicht existiert.
        """
        garden = Garden(self.map_file, self.garden_objects)

        self.assertEqual(len(garden.garden_map), ROWS)
        for row in garden.garden_map:
            self.assertEqual(len(row), COLS)
            # Alle Einträge sollten 0 sein
            self.assertTrue(all(elem == 0 for elem in row))

        # placed_objects sollte entsprechend leer sein
        self.assertEqual(len(garden.placed_objects), 0)

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="012\n120")
    def test_init_garden_map_with_file(self, mock_file, mock_isfile):
        """
        Testet, ob init_garden_map die Daten aus der map-Datei korrekt einliest.
        """
        garden = Garden(self.map_file, self.garden_objects)

        # garden_map sollte entsprechend den Daten aus der Datei sein.
        # Wir haben in read_data zwei Zeilen definiert:
        # "012" und "120"
        # Daraus ergeben sich:
        # garden_map[0] = [0,1,2]
        # garden_map[1] = [1,2,0]
        expected_map = [[0, 1, 2], [1, 2, 0]]
        self.assertEqual(garden.garden_map[:2], expected_map)

        # In "012" und "120" sind insgesamt 4 Positionen > 0:
        # -> placed_objects sollte 4 Objekte enthalten.
        self.assertEqual(len(garden.placed_objects), 4)

    @patch("pygame.mouse.get_pos", return_value=(210, 55))  # -> [1][4]
    @patch("os.path.isfile", return_value=False)
    def test_place_object(self, mock_isfile, mock_mouse):
        """
        Testet das Platzieren eines Objekts per place_object().
        """
        garden = Garden(self.map_file, self.garden_objects)

        with patch("os.path.isfile", return_value=False):
            garden.init_garden_map()

        garden.place_object(2)

        self.assertEqual(garden.garden_map[1][4], 2)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_garden_map(self, mock_file):
        """
        Testet, ob save_garden_map die Daten korrekt in die Datei schreibt.
        """
        garden = Garden(self.map_file, self.garden_objects)

        # Beispiel-garden_map:
        garden.garden_map = [
            [0, 1, 2],
            [2, 0, 1]
        ]

        garden.save_garden_map()

        # Überprüfe, ob in die Datei reingeschrieben wurde:
        mock_file.assert_called_once_with(self.map_file, 'w')
        
        handle = mock_file()
        handle.write.assert_any_call("012\n")
        handle.write.assert_any_call("201\n")

    @patch("pygame.Surface")  # Win-Objekt als Mock
    @patch("os.path.isfile", return_value=False)
    def test_draw_garden_map(self, mock_isfile, mock_surface):
        """
        Testet, ob draw_garden_map() für jeden Zellenplatz
        das Bodenbild (Index 0) zeichnet und
        anschließend alle placed_objects zeichnet.
        """
        garden = Garden(self.map_file, self.garden_objects)
        with patch("os.path.isfile", return_value=False):
            garden.init_garden_map()

        # Füge ein paar Objekte hinzu:
        garden.garden_map[4][6] = 1  # (300,200)
        garden.garden_map[1][2] = 2  # (100,50)
        
        garden.update_garden_map()
        window_mock = MagicMock()
        garden.draw_garden_map(window_mock)

        # Für jede Zelle in ROWS x COLS wird boden_object.image gezeichnet
        # -> Anzahl der erwarteten blit-Aufrufe = ROWS*COLS + #PlacedObjects
        self.assertEqual(window_mock.blit.call_count, 350 + 2)

        # Erste Aufruf sollte Boden sien
        first_call_args = window_mock.blit.call_args_list[0][0]
        # first_call_args ist ein Tuple (image, (x, y))
        # ground_object = self.garden_objects[0]
        # wir erwarten also ground_object.image, Position = (0,0)
        self.assertEqual(first_call_args[0], self.garden_objects[0].image)
        self.assertEqual(first_call_args[1], (0, 0))

        # Die placed_objects wurden als letztes gezeichnet, also:
        # placed_object 1 -> (0,0)
        # placed_object 2 -> (100,50)
        obj1_call = window_mock.blit.call_args_list[-2][0]
        self.assertEqual(obj1_call[1], (100, 50))

        obj2_call = window_mock.blit.call_args_list[-1][0]
        self.assertEqual(obj2_call[1], (300, 200))


if __name__ == '__main__':
    unittest.main()