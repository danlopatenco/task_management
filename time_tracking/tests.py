from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import TimeTracker, TimeEntry
from projects.models import Project
from tasks.models import Task


class TimeTrackerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            start_date=date.today(),
            end_date=date.today(),
            id=1
        )

        self.task = Task.objects.create(
            title='Test Task',
            description='Test Task Description',
            deadline=date.today(),
            status=Task.TaskStatus.IN_PROGRESS,
            project=self.project,
            created_by=self.user,
            id=2
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_start_tracking_no_entries(self):

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        # Ensure no TimeTracker exists
        self.assertEqual(TimeTracker.objects.filter(user=self.user, task_id=self.task.id).count(), 0)

        # Start tracking
        url = reverse('timetracker-start-tracking')
        body = {'task_id': self.task.id}

        response = self.client.post(url, data=body, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check a new TimeTracker has been created
        self.assertEqual(TimeTracker.objects.filter(user=self.user, task_id=self.task.id).count(), 1)
        time_tracker = TimeTracker.objects.get(user=self.user, task_id=self.task.id)

        # Ensure that Time Tracker is runing
        self.assertTrue(time_tracker.is_running)

    def test_stop_tracking_creates_time_entry(self):
        # Setup: Start tracking first

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        body = {'task_id': self.task.id}

        # Start tracking
        url_start = reverse('timetracker-start-tracking')
        response_start = self.client.post(url_start, data=body, headers=headers)
        self.assertEqual(response_start.status_code, status.HTTP_200_OK)

        # Stop tracking
        url_stop = reverse('timetracker-stop-tracking')
        response_stop = self.client.post(url_stop, data=body, headers=headers)
        self.assertEqual(response_stop.status_code, status.HTTP_200_OK)

        # Check a new TimeEntry has been created
        self.assertEqual(TimeEntry.objects.filter(user=self.user, task=self.task).count(), 1)

        # Check TimeTracker is stopped
        time_tracker = TimeTracker.objects.get(user=self.user, task_id=self.task.id)
        self.assertFalse(time_tracker.is_running)
