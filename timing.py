"""
Human Behavior Simulation Module
Mimics realistic human interaction patterns with Instagram
"""

import time
import random
import math
from typing import Optional, Callable
from datetime import datetime, timedelta
import threading


class HumanTiming:
    """
    Simulates realistic human timing patterns
    """

    def __init__(
        self,
        min_delay: float = 2.0,
        max_delay: float = 8.0,
        typing_speed_wpm: int = 40
    ):
        """
        Initialize human timing simulator
        :param min_delay: Minimum delay between actions (seconds)
        :param max_delay: Maximum delay between actions (seconds)
        :param typing_speed_wpm: Typing speed in words per minute
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.typing_speed_wpm = typing_speed_wpm
        self.last_action_time = 0

    def wait_before_action(self, action_type: str = "general"):
        """
        Wait a realistic amount of time before performing action
        :param action_type: Type of action (affects delay)
        """
        current_time = time.time()

        # Calculate time since last action
        time_since_last = current_time - self.last_action_time

        # Different actions have different minimum delays
        action_delays = {
            "login": (3.0, 7.0),
            "post": (5.0, 15.0),
            "like": (1.0, 3.0),
            "comment": (3.0, 10.0),
            "follow": (2.0, 5.0),
            "general": (self.min_delay, self.max_delay)
        }

        min_delay, max_delay = action_delays.get(action_type, action_delays["general"])

        # Calculate delay using gamma distribution for realistic variation
        # Gamma distribution creates more natural-looking delays
        delay = self._gamma_delay(min_delay, max_delay)

        # If we've already waited enough, reduce the delay
        if time_since_last < delay:
            actual_delay = delay - time_since_last
            time.sleep(actual_delay)

        self.last_action_time = time.time()

    def _gamma_delay(self, min_val: float, max_val: float) -> float:
        """
        Generate delay using gamma distribution
        Creates more natural-looking random delays
        :param min_val: Minimum delay
        :param max_val: Maximum delay
        :return: Delay in seconds
        """
        # Gamma distribution parameters
        shape = 2.0
        scale = 1.0

        # Generate gamma-distributed value
        gamma_val = random.gammavariate(shape, scale)

        # Normalize to our range
        # Gamma values typically fall between 0 and 10 with these parameters
        normalized = min(gamma_val / 10.0, 1.0)

        # Scale to our desired range
        delay = min_val + (normalized * (max_val - min_val))

        return delay

    def typing_delay(self, text: str) -> float:
        """
        Calculate realistic typing delay for text
        :param text: Text that would be typed
        :return: Delay in seconds
        """
        # Average word length in English is ~5 characters
        words = len(text) / 5.0

        # Base typing time
        base_time = (words / self.typing_speed_wpm) * 60.0

        # Add random variation (people don't type at constant speed)
        variation = random.uniform(0.8, 1.3)

        # Add thinking pauses (longer for longer text)
        thinking_pauses = random.uniform(0.5, 2.0) * (1 + math.log(len(text) + 1) / 10)

        total_time = (base_time * variation) + thinking_pauses

        return total_time

    def simulate_typing(self, text: str, callback: Optional[Callable] = None):
        """
        Simulate typing text character by character
        :param text: Text to type
        :param callback: Optional callback function called with each character
        """
        delay = self.typing_delay(text)
        chars_per_second = len(text) / delay

        for char in text:
            # Random variation in typing speed
            char_delay = (1.0 / chars_per_second) * random.uniform(0.5, 1.5)

            # Occasional longer pauses (thinking, looking at keyboard, etc.)
            if random.random() < 0.1:
                char_delay += random.uniform(0.3, 1.0)

            time.sleep(char_delay)

            if callback:
                callback(char)

    def wait_random(self, min_seconds: float, max_seconds: float):
        """
        Wait a random amount of time
        :param min_seconds: Minimum wait time
        :param max_seconds: Maximum wait time
        """
        delay = self._gamma_delay(min_seconds, max_seconds)
        time.sleep(delay)


class ActivityScheduler:
    """
    Schedules activities to mimic realistic usage patterns
    Avoids posting at suspicious times (e.g., 3 AM)
    """

    def __init__(self):
        self.active_hours_start = 8  # 8 AM
        self.active_hours_end = 23   # 11 PM
        self.timezone_offset = 0

    def is_good_time_to_post(self) -> bool:
        """
        Check if current time is realistic for posting
        :return: True if it's a good time to post
        """
        now = datetime.now()
        hour = now.hour

        # Check if within active hours
        if not (self.active_hours_start <= hour < self.active_hours_end):
            return False

        # Slightly reduce activity during typical work hours (9-5)
        if 9 <= hour < 17:
            # 70% chance to consider it a good time during work hours
            return random.random() < 0.7

        # Peak activity hours (evening)
        if 18 <= hour < 22:
            # 95% chance - this is prime social media time
            return random.random() < 0.95

        return True

    def wait_until_good_time(self, max_wait_hours: float = 12.0):
        """
        Wait until it's a realistic time to perform activity
        :param max_wait_hours: Maximum hours to wait
        """
        waited = 0
        check_interval = 300  # Check every 5 minutes

        while not self.is_good_time_to_post() and waited < max_wait_hours * 3600:
            time.sleep(check_interval)
            waited += check_interval

    def get_next_good_time(self) -> datetime:
        """
        Calculate next realistic time to post
        :return: Next good datetime
        """
        now = datetime.now()
        hour = now.hour

        # If currently in good hours, return now
        if self.is_good_time_to_post():
            return now

        # If before active hours, wait until start
        if hour < self.active_hours_start:
            next_time = now.replace(
                hour=self.active_hours_start,
                minute=random.randint(0, 59)
            )
        else:
            # After active hours, wait until tomorrow
            tomorrow = now + timedelta(days=1)
            next_time = tomorrow.replace(
                hour=self.active_hours_start,
                minute=random.randint(0, 59)
            )

        return next_time

    def schedule_posts(
        self,
        num_posts: int,
        spread_hours: float = 8.0
    ) -> list:
        """
        Schedule multiple posts across time period
        :param num_posts: Number of posts to schedule
        :param spread_hours: Hours to spread posts across
        :return: List of datetime objects
        """
        schedule = []
        start_time = self.get_next_good_time()

        for i in range(num_posts):
            # Calculate offset for this post
            offset_hours = (spread_hours / num_posts) * i

            # Add random variation
            offset_hours += random.uniform(-0.5, 0.5)

            # Calculate post time
            post_time = start_time + timedelta(hours=offset_hours)

            # Adjust if outside active hours
            while not (self.active_hours_start <= post_time.hour < self.active_hours_end):
                post_time += timedelta(hours=1)

            schedule.append(post_time)

        return sorted(schedule)


class RateLimiter:
    """
    Intelligent rate limiting to avoid detection
    """

    def __init__(
        self,
        max_requests_per_hour: int = 60,
        max_posts_per_day: int = 10
    ):
        """
        Initialize rate limiter
        :param max_requests_per_hour: Maximum API requests per hour
        :param max_posts_per_day: Maximum posts per day
        """
        self.max_requests_per_hour = max_requests_per_hour
        self.max_posts_per_day = max_posts_per_day

        self.request_times = []
        self.post_times = []

        self.lock = threading.Lock()

    def wait_if_needed(self, action_type: str = "request"):
        """
        Wait if rate limit would be exceeded
        :param action_type: Type of action ("request" or "post")
        """
        with self.lock:
            now = time.time()

            if action_type == "request":
                # Remove requests older than 1 hour
                self.request_times = [t for t in self.request_times if now - t < 3600]

                # Check if we're at limit
                if len(self.request_times) >= self.max_requests_per_hour:
                    # Wait until oldest request is 1 hour old
                    oldest = min(self.request_times)
                    wait_time = 3600 - (now - oldest) + random.uniform(1, 10)
                    if wait_time > 0:
                        time.sleep(wait_time)

                # Record this request
                self.request_times.append(time.time())

            elif action_type == "post":
                # Remove posts older than 24 hours
                self.post_times = [t for t in self.post_times if now - t < 86400]

                # Check if we're at limit
                if len(self.post_times) >= self.max_posts_per_day:
                    # Wait until oldest post is 24 hours old
                    oldest = min(self.post_times)
                    wait_time = 86400 - (now - oldest) + random.uniform(60, 300)
                    if wait_time > 0:
                        time.sleep(wait_time)

                # Record this post
                self.post_times.append(time.time())

    def get_stats(self) -> dict:
        """
        Get current rate limit statistics
        :return: Dictionary with stats
        """
        now = time.time()

        # Clean old records
        self.request_times = [t for t in self.request_times if now - t < 3600]
        self.post_times = [t for t in self.post_times if now - t < 86400]

        return {
            "requests_last_hour": len(self.request_times),
            "posts_last_24h": len(self.post_times),
            "requests_remaining": self.max_requests_per_hour - len(self.request_times),
            "posts_remaining": self.max_posts_per_day - len(self.post_times)
        }
