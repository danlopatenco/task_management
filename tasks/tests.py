from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Project, Task
from datetime import date


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # NOTE: create the Project instance without assigning team_members
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            start_date=date.today(),
            end_date=date.today()
        )
        # NOTE: set() to assign team_members after the Project instance has been created
        self.project.team_members.set([self.user])

        # Create the Task instance and assign the user as the creator
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Task Description',
            deadline=date.today(),
            status=Task.TaskStatus.IN_PROGRESS,
            project=self.project,
            created_by=self.user
        )
        # NOTE: Assign the user to the assigned_to ManyToManyField
        self.task.assigned_to.set([self.user])
        self.client.force_authenticate(user=self.user)

    def test_list_tasks(self):
        """
        Ensure that an authenticated user can retrieve a list of tasks.
        """
        url = reverse('task-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_task_detail(self):
        """
        Ensure that the details of a task can be retrieved by an authenticated user.
        """
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        """
        Ensure that an existing task can be updated by an authenticated user.
        """
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        data = {'status': Task.TaskStatus.COMPLETED}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.TaskStatus.COMPLETED)

    def test_delete_task(self):
        """
        Ensure that an authenticated user can delete a task.
        """
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_create_task(self):
        """
        Ensure that a task can be created by an authenticated user.
        """
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'deadline': '2023-12-31',
            'status': Task.TaskStatus.IN_PROGRESS,
            'project_id': self.project.pk
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_task = Task.objects.get(pk=response.data['id'])
        self.assertEqual(new_task.title, data['title'])
        self.assertEqual(new_task.status, data['status'])
