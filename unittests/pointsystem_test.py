import unittest
from pointsystem.pointsystem import PointSystem


class TestPointSystem(unittest.TestCase):

    def setUp(self):
        self.ps = PointSystem()

    def test_initial_state(self):
        self.assertEqual(self.ps.total_points, 0)
        self.assertEqual(self.ps.available_points, 0)

    def test_add_points(self):
        self.ps.add_points(10)
        self.assertEqual(self.ps.total_points, 10)
        self.assertEqual(self.ps.available_points, 10)

    def test_remove_points(self):
        self.ps.add_points(10)
        self.ps.remove_points(5)
        self.assertEqual(self.ps.total_points, 10)
        self.assertEqual(self.ps.available_points, 5)

    def test_set_points(self):
        self.ps.set_points(20, 15)
        self.assertEqual(self.ps.total_points, 20)
        self.assertEqual(self.ps.available_points, 15)

    def test_get_points(self):
        self.ps.set_points(30, 25)
        self.assertEqual(self.ps.get_points(), (30, 25))