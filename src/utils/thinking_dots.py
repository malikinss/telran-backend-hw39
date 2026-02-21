# ./src/utils/thinking_dots.py

import sys
import time
import threading


class ThinkingDots:
    """
    Animated "thinking..." indicator for console applications.

    Displays a label followed by a variable number of dots that cycle
    from 0 to `max_dots` to indicate ongoing processing or waiting.
    Useful for showing a user that a background task is running.

    Attributes:
        label (str): Text to display before the dots.
        interval (float): Time in seconds between dot updates.
        max_dots (int): Maximum number of dots to display.

    Example:
        >>> import time
        >>> dots = ThinkingDots("Processing")
        >>> dots.start()
        >>> time.sleep(2)  # simulate long-running task
        >>> dots.stop()
    """

    def __init__(self, label: str, interval: float = 0.5) -> None:
        """
        Initialize a ThinkingDots instance.

        Args:
            label (str): The label text displayed before the dots.
            interval (float): Delay in seconds between updates. Default is 0.5.

        Sets up internal threading and calculates line length for clearing.
        """
        self.label: str = label
        self.interval: float = interval
        self.max_dots: int = 5
        self._stop_event: threading.Event = threading.Event()
        self._thread: threading.Thread | None = None
        self._max_len: int = len(label) + self.max_dots

    def _format_line(self, dots_count: int) -> str:
        """
        Generate a single console line with the label and current dots.

        Args:
            dots_count (int): Current iteration number to determine
                              the number of dots to display.

        Returns:
            str: Formatted string ready to be printed to the console.

        Example:
            >>> td = ThinkingDots("Wait")
            >>> td._format_line(2)
            'Wait..   '
        """
        dots = "." * (dots_count % (self.max_dots + 1))
        spaces = " " * (self.max_dots - (dots_count % (self.max_dots + 1)))
        return f"{self.label}{dots}{spaces}"

    def _clear_line(self) -> None:
        """
        Clear the current console line.

        Ensures that after stopping the animation, the line is fully blanked.
        """
        sys.stdout.write("\r" + " " * self._max_len + "\r")
        sys.stdout.flush()

    def _worker(self) -> None:
        """
        Background worker that updates the dots animation.

        Cycles the number of dots every `interval` seconds.
        Stops when `self._stop_event` is set.
        Clears the line after stopping.
        """
        dots_count = 0
        while not self._stop_event.is_set():
            sys.stdout.write("\r" + self._format_line(dots_count))
            sys.stdout.flush()
            dots_count += 1
            time.sleep(self.interval)
        self._clear_line()

    def start(self) -> None:
        """
        Start the animated thinking dots in a background thread.

        If already running, this method does nothing.

        Example:
            >>> td = ThinkingDots("Thinking")
            >>> td.start()
        """
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the thinking dots animation and clear the console line.

        Waits for the background thread to terminate before returning.

        Example:
            >>> td = ThinkingDots("Thinking")
            >>> td.start()
            >>> td.stop()
        """
        if not self._thread or not self._thread.is_alive():
            return
        self._stop_event.set()
        self._thread.join()
