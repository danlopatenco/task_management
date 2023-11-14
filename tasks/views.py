
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from projects.models import Project
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.models import User


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset of tasks assigned to user.

        Returns:
            QuerySet: A filtered queryset of tasks.
        """
        # Get the authenticated user from the request
        user = self.request.user

        # Filter projects where the user is a team member
        queryset = Task.objects.filter(assigned_to=user)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new task assigned to the authenticated user.

        Args:
            request (HttpRequest): The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response indicating the success or failure of the task creation.
        """
        # Get the authenticated user from the request
        user = self.request.user
        user_instance = User.objects.get(pk=user.id)
        # Check if the project ID is provided in the request data
        project_id = request.data.get('project_id')

        if project_id is None:
            return Response({'error': 'Project ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the project exists and if the user is assigned to it
            project = Project.objects.get(pk=project_id)
            if user not in project.team_members.all():
                return Response({'error': 'You are not assigned to this project.'}, status=status.HTTP_403_FORBIDDEN)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Create the task and assign it to the user
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(assigned_to=[user], project=project, created_by=user_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a task if the authenticated user is the task's creator.

        Args:
            request (HttpRequest): The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response indicating the success or failure of the task deletion.
        """
        # Get the task to be deleted
        task = self.get_object()

        # Check if the authenticated user is the task's creator
        if request.user.id == task.created_by_id:
            task.delete()
            return Response({'message': 'Task deleted successfully.'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You do not have permission to delete this task.'},
                            status=status.HTTP_403_FORBIDDEN)
