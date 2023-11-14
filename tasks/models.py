from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Task(models.Model):

    class TaskStatus(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        DELAYED = 'delayed', 'Delayed'

    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()

    status = models.CharField(max_length=20, choices=TaskStatus.choices)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks')

    def __str__(self):
        return self.title
