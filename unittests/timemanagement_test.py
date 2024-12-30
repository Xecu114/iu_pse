import unittest
from PyQt6.QtCore import QTime
from productivitysession.timemanagement import TimeManagement


class TestTimeManagement(unittest.TestCase):

    def setUp(self):
        self.tm = TimeManagement()

    def test_initial_state(self):
        self.assertEqual(self.tm.selected_timer, "pomodoro")
        self.assertEqual(self.tm.mode, "stopped")
        self.assertEqual(self.tm.elapsed_time, QTime(0, 0, 0))
        self.assertEqual(self.tm.target_time, QTime(0, 0, 0))
        self.assertFalse(self.tm.timer_elapsed)
        self.assertTrue(self.tm.is_work_phase)
        self.assertEqual(self.tm.pomodoro_work_time, QTime(0, 25, 0))
        self.assertEqual(self.tm.pomodoro_break_time, QTime(0, 5, 0))
        self.assertEqual(self.tm.productiv_minutes, 0)

    def test_start_stopwatch(self):
        self.tm.start_stopwatch()
        self.assertEqual(self.tm.mode, "running")

    def test_set_timer(self):
        self.tm.set_timer(1, 30, 0)
        self.assertEqual(self.tm.target_time, QTime(1, 30, 0))
        self.assertEqual(self.tm.elapsed_time, QTime(0, 0, 0))

    def test_start_timer(self):
        self.tm.set_timer(0, 2, 0)
        self.tm.start_timer()
        self.assertEqual(self.tm.mode, "running")

    def test_set_pomodoro_time(self):
        self.tm.set_pomodoro_time(0, 30, 0, 0, 10, 0)
        self.assertEqual(self.tm.pomodoro_work_time, QTime(0, 30, 0))
        self.assertEqual(self.tm.pomodoro_break_time, QTime(0, 10, 0))

    def test_start_pomodoro(self):
        self.tm.start_pomodoro()
        self.assertTrue(self.tm.is_work_phase)
        self.assertEqual(self.tm.mode, "running")

    def test_switch_pomodoro_phase(self):
        self.tm.switch_pomodoro_phase()
        self.assertFalse(self.tm.is_work_phase)
        self.tm.switch_pomodoro_phase()
        self.assertTrue(self.tm.is_work_phase)

    def test_increment_time(self):
        self.tm.increment_time()
        self.assertEqual(self.tm.elapsed_time, QTime(0, 0, 1))

    def test_decrement_time(self):
        self.tm.set_timer(0, 2, 0)
        self.tm.decrement_time()
        self.assertEqual(self.tm.target_time, QTime(0, 1, 59))

    def test_pause(self):
        self.tm.start_stopwatch()
        self.tm.pause()
        self.assertEqual(self.tm.mode, "paused")

    def test_resume(self):
        self.tm.start_stopwatch()
        self.tm.pause()
        self.tm.resume()
        self.assertEqual(self.tm.mode, "running")

    def test_stop(self):
        self.tm.start_stopwatch()
        self.tm.stop()
        self.assertEqual(self.tm.mode, "stopped")
        self.assertEqual(self.tm.elapsed_time, QTime(0, 0, 0))
        self.assertEqual(self.tm.target_time, QTime(0, 0, 0))

    def test_get_display_time(self):
        self.tm.set_timer(1, 0, 0)
        self.tm.decrement_time()
        self.assertEqual(self.tm.get_display_time(), "00:59:59")
        self.tm.start_stopwatch()
        self.tm.increment_time()
        self.assertEqual(self.tm.get_display_time(), "00:00:01")

    def test_set_timer_mode(self):
        self.tm.set_timer_mode("timer")
        self.assertEqual(self.tm.selected_timer, "timer")
        self.assertEqual(self.tm.mode, "stopped")