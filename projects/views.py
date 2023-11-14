
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    basename = 'project'

    def get_queryset(self):
        """
        Get the queryset of projects where the authenticated user is a team member.

        Returns:
            QuerySet: A filtered queryset of projects.
        """
        # Get the authenticated user from the request
        user = self.request.user

        # Filter projects where the user is a team member
        queryset = Project.objects.filter(team_members=user)

        return queryset

    def perform_create(self, serializer):
        """
        Create a new project and set the creator as a team member.

        Args:
            serializer (ProjectSerializer): The serializer for creating a project.
        """

        project = serializer.save(team_members=[self.request.user])

        return Response(self.get_serializer(project).data, status=status.HTTP_201_CREATED)

    # @action(detail=False, methods=["get"])
    # def all(self):
    #     # Get the authenticated user from the request
    #     user = self.request.user

    #     # Filter projects where the user is a team member
    #     queryset = Project.objects.filter(team_members=user)

    #     return queryset
