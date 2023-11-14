from django.db import models
from tasks.models import Task
from django.contrib.auth.models import User


class TimeEntry(models.Model):
    """
    This model is used to record specific time entries when a user has worked on a task.
    Each TimeEntry instance represents a period of time during which the user worked on a task.
    It records the start and end times of the work session and associates it with a specific task and user.
    This model is suitable for situations where you want to log and track the actual hours spent on a task, a
    llowing users to manually add or edit entries for past work sessions.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='time_entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_entries')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        # Calculate the duration in hours and minutes
        duration = self.end_time - self.start_time
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60

        return f"Task ID: {self.task_id}, Hours: {hours}, Minutes: {minutes}"


class TimeTracker(models.Model):
    """
    This model is used to manage the current state of tracking time for a task.
    It includes fields like is_running and start_time to indicate whether the user is currently
    tracking time for a task and, if so, when the tracking started.
    The TimeTracker model is useful for situations where users want
    to start and stop timers to track time in real-time.
    It allows users to easily pause and resume tracking without creating multiple time entries.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='time_tracker')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_tracker')
    is_running = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Task ID: {self.task_id}"
