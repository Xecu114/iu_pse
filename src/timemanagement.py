from PyQt6.QtCore import QTime, QTimer


class TimeManagement:
    def __init__(self):
        self.selected_timer = "pomodoro"  # "pomodoro", "timer", "stoppwatch"
        self.mode = "stopped"  # "stopped", "running", "paused"
        self.timer = QTimer()
        self.elapsed_time = QTime(0, 0, 0)
        self.target_time = QTime(0, 0, 0)
        self.remaining_time = QTime(0, 0, 0)
        self.is_work_phase = True
        self.pomodoro_work_time = QTime(0, 25, 0)
        self.pomodoro_break_time = QTime(0, 5, 0)
        self.productiv_minutes = 0

    def start_stopwatch(self):
        # Safely disconnect to avoid conflicts
        try:
            self.timer.timeout.disconnect(self.increment_time)  # For stopwatch
        except TypeError:
            pass  # Ignore if no connection exists
        self.timer.timeout.connect(self.increment_time)
        self.timer.start(1000)
        self.mode = "running"

    def set_timer(self, hours=0, minutes=0, seconds=0):
        """Set the timer's target time."""
        self.target_time = QTime(hours, minutes, seconds)
        self.elapsed_time = QTime(0, 0, 0)  # Reset elapsed time for consistency
        self.remaining_time = self.target_time

    def start_timer(self):
        """Start the timer countdown."""
        # print("Starting timer...")  # Debug message
        # Safely disconnect to avoid conflicts
        try:
            self.timer.timeout.disconnect(self.increment_time)  # For stopwatch
        except TypeError:
            pass  # Ignore if no connection exists
        self.timer.timeout.connect(self.increment_time)
        self.timer.start(1000)
        self.mode = "running"

    def set_pomodoro_time(self, wh=0, wm=25, ws=0, bh=0, bm=5, bs=0):
        """Set the time based on the current phase and manual input."""
        self.pomodoro_work_time = QTime(wh, wm, ws)
        self.pomodoro_break_time = QTime(bh, bm, bs)
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
        self.start_timer()

    def switch_pomodoro_phase(self):
        """Switches between work- and breakphase."""
        self.is_work_phase = not self.is_work_phase
        print(f"Pomodoro: switched to {"work" if self.is_work_phase else "break"}")  # Debug message
        if self.is_work_phase:
            self.set_timer(self.pomodoro_work_time.hour(),
                           self.pomodoro_work_time.minute(),
                           self.pomodoro_work_time.second())
        else:
            self.set_timer(self.pomodoro_break_time.hour(),
                           self.pomodoro_break_time.minute(),
                           self.pomodoro_break_time.second())
        self.start_timer()

    def increment_time(self):
        """Increment the stopwatches elapsed time."""
        self.elapsed_time = self.elapsed_time.addSecs(1)
        print(f"Time elapsed: {self.elapsed_time.toString("hh:mm:ss")}")  # Debug message
        if self.elapsed_time.second() == 0:  # 1 minute passed
            self.productiv_minutes += 1
        if self.selected_timer != "stopwatch":
            self.update_remaining_time()
            if self.remaining_time == QTime(0, 0, 0):
                if self.selected_timer == "pomodoro":
                    self.switch_pomodoro_phase()
                elif self.selected_timer == "timer":
                    self.timer.stop()
                    self.mode = "stopped"
                    print("Timer reached zero!")

    def update_remaining_time(self):
        remaining_seconds = self.target_time.msecsSinceStartOfDay() // 1000 - \
                            self.elapsed_time.msecsSinceStartOfDay() // 1000
        if remaining_seconds < 0:
            remaining_seconds = 0
        self.remaining_time = QTime(0, 0, 0).addSecs(remaining_seconds)
        # print(f"Remaining time: {self.remaining_time.toString('hh:mm:ss')}")

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
        self.remaining_timem = QTime(0, 0, 0)
        self.mode = "stopped"
  
    def set_timer_mode(self, timer_mode: str):
        """Set the timer mode to either 'pomodoro', 'timer' or 'stopwatch'."""
        self.selected_timer = timer_mode
        self.stop()  # Reset the timer/stopwatch
