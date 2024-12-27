from PyQt6.QtCore import QTimer, QTime


class TimeManagement:
    def __init__(self):
        self.timer = QTimer()
        self.elapsed_time = QTime(0, 0, 0)
        self.target_time = QTime(0, 0, 0)
        self.is_stopwatch = True  # True for Stopwatch, False for Timer
        self.mode = "stopped"  # "stopped", "running", "paused"

    def start_stopwatch(self):
        # Safely disconnect to avoid conflicts
        try:
            self.timer.timeout.disconnect(self.increment_time)  # For stopwatch
        except TypeError:
            pass  # Ignore if no connection exists
        try:
            self.timer.timeout.disconnect(self.decrement_time)  # For timer
        except TypeError:
            pass  # Ignore if no connection exists
        self.timer.timeout.connect(self.increment_time)
        self.timer.start(1000)
        self.mode = "running"

    def pause(self):
        """Pause the timer or stopwatch."""
        self.timer.stop()
        self.mode = "paused"

    def resume(self):
        """Resume the timer or stopwatch from the paused state."""
        # if self.is_stopwatch:
        #     self.timer.timeout.connect(self.increment_time)
        # else:
        #     self.timer.timeout.connect(self.decrement_time)
        self.timer.start(1000)  # Restart the timer
        self.mode = "running"  # Change state to running
    
    def stop(self):
        self.timer.stop()
        self.elapsed_time = QTime(0, 0, 0)
        self.target_time = QTime(0, 0, 0)
        self.mode = "stopped"

    def set_timer(self, hours=0, minutes=0, seconds=0):
        """Set the timer's target time."""
        self.target_time = QTime(hours, minutes, seconds)
        self.elapsed_time = QTime(0, 0, 0)  # Reset elapsed time for consistency

    def start_timer(self):
        """Start the timer countdown."""
        print("Starting timer...")  # Debug message
        self.mode = "running"
        # Safely disconnect to avoid conflicts
        try:
            self.timer.timeout.disconnect(self.increment_time)  # For stopwatch
        except TypeError:
            pass  # Ignore if no connection exists

        try:
            self.timer.timeout.disconnect(self.decrement_time)  # For timer
        except TypeError:
            pass  # Ignore if no connection exists
        self.timer.timeout.connect(self.decrement_time)
        self.timer.start(1000)

    def increment_time(self):
        """Decrement the stopwatches elapsed time."""
        self.elapsed_time = self.elapsed_time.addSecs(1)
        print(f"Time elapsed: {self.elapsed_time.toString("hh:mm:ss")}")  # Debug message

    def decrement_time(self):
        """Decrement the timer's target time."""
        if self.target_time == QTime(0, 0, 0):
            self.timer.stop()
            self.mode = "stopped"
            print("Timer reached zero!")  # Debug message
        else:
            self.target_time = self.target_time.addSecs(-1)
            print(f"Time left: {self.target_time.toString("hh:mm:ss")}")  # Debug message

    def get_display_time(self):
        if self.mode == "stopped" and self.target_time != QTime(0, 0, 0):
            return self.target_time.toString("hh:mm:ss")
        return self.elapsed_time.toString("hh:mm:ss") if self.mode != "stopped" else "00:00:00"
    
    def set_mode(self, mode):
        self.is_stopwatch = (mode == "stopwatch")
        self.stop()  # Reset the timer/stopwatch
