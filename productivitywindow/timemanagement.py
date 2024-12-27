from PyQt6.QtCore import QTime, QTimer


class TimeManagement:
    def __init__(self):
        self.timer = QTimer()
        self.elapsed_time = QTime(0, 0, 0)
        self.target_time = QTime(0, 0, 0)
        self.timer_elapsed = False  # True if Timer is elapsed
        self.is_work_phase = True
        self.pomodoro_work_time = QTime(0, 25, 0)
        self.pomodoro_break_time = QTime(0, 25, 0)
        self.selected_timer = "pomodoro"  # "pomodoro", "timer", "stoppwatch"
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

    def set_pomodoro_time(self):
        """Set the time based on the current phase and manual input."""
        if self.is_work_phase:
            self.set_timer(self.pomodoro_work_time.hour(),
                           self.pomodoro_work_time.minute(),
                           self.pomodoro_work_time.second())
        else:
            self.set_timer(self.pomodoro_break_time.hour(),
                           self.pomodoro_break_time.minute(),
                           self.pomodoro_break_time.second())
    
    def start_pomodoro(self):
        """Starts the pomodoro-timer."""
        self.is_work_phase = True  # start with work phase
        self.set_pomodoro_time()
        self.start_timer()

    def switch_pomodoro_phase(self):
        """Switches between work- and breakphase."""
        self.is_work_phase = not self.is_work_phase
        print(f"Pomodoro: switched to {"work" if self.is_work_phase else "break"}")  # Debug message
        self.set_pomodoro_time()
        self.start_timer()

    def increment_time(self):
        """Decrement the stopwatches elapsed time."""
        self.elapsed_time = self.elapsed_time.addSecs(1)
        print(f"Time elapsed: {self.elapsed_time.toString("hh:mm:ss")}")  # Debug message

    def decrement_time(self):
        """Decrement the timer's target time."""
        if self.target_time == QTime(0, 0, 0):
            if self.selected_timer == "pomodoro":
                self.switch_pomodoro_phase()
            else:
                self.timer.stop()
                self.mode = "stopped"
                self.timer_elapsed = True
                print("Timer reached zero!")  # Debug message
        else:
            self.target_time = self.target_time.addSecs(-1)
            print(f"Time left: {self.target_time.toString("hh:mm:ss")}")  # Debug message

    def pause(self):
        """Pause the timer or stopwatch."""
        self.timer.stop()
        self.mode = "paused"

    def resume(self):
        """Resume the timer or stopwatch from the paused state."""
        self.timer.start(1000)  # Restart the timer
        self.mode = "running"  # Change state to running
    
    def stop(self):
        self.timer.stop()
        self.elapsed_time = QTime(0, 0, 0)
        self.target_time = QTime(0, 0, 0)
        self.mode = "stopped"

    def get_display_time(self):
        if self.mode == "stopped" and self.target_time != QTime(0, 0, 0):
            return self.target_time.toString("hh:mm:ss")
        return self.elapsed_time.toString("hh:mm:ss") if self.mode != "stopped" else "00:00:00"
    
    def set_mode(self, timer_mode):
        self.selected_timer = timer_mode
        self.stop()  # Reset the timer/stopwatch
