from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Project
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta


class ProjectAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = Project.objects.create(
            title='Initial Project',
            description='Initial Description',
            start_date='2023-01-01',
            end_date='2023-12-31',
            id=7
        )
        # Create a token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_list_projects_authenticated(self):
        """
        Ensure an authenticated user can retrieve the list of projects with token auth.
        """
        self.authenticate()
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_projects_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot retrieve the list of projects.
        """
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_project_detail_as_team_member(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        # Create a project in the test database with the test user as a team member
        project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
        )
        project.team_members.add(self.user)
        project.save()

        # Use the 'pk' of the new project instance to construct the URL
        url = reverse('project-detail', kwargs={'pk': project.pk})
        response = self.client.get(url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project_authenticated(self):
        """
        Ensure an authenticated user can create a new project with valid data using token auth.
        """
        self.authenticate()
        url = reverse('project-list')
        data = {
            'title': 'New Project',
            'description': 'A test project',
            'start_date': '2023-02-01',
            'end_date': '2023-11-30'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_project_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot create a new project.
        """
        url = reverse('project-list')
        data = {
            'title': 'New Project',
            'description': 'A test project',
            'start_date': '2023-02-01',
            'end_date': '2023-11-30'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_project_authenticated(self):
        """
        Ensure an authenticated user can delete an existing project with token auth.
        """
        self.project.team_members.add(self.user)
        self.authenticate()
        1
        url = reverse('project-detail', kwargs={'pk': self.project.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_project_authenticated(self):
        """
        Ensure an authenticated user can update an existing project with valid changes using token auth.
        """
        self.authenticate()
        self.project.team_members.add(self.user)
        url = reverse('project-detail', kwargs={'pk': self.project.pk})
        data = {'title': 'Updated Project Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Project Title')
