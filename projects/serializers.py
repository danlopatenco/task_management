from rest_framework import serializers
from .models import Project
from core.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):

    team_members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

    # title = serializers.CharField(required=False)
    # start_date = serializers.DateField(required=False)
    # end_date = serializers.DateField(required=False)
    # description = serializers.CharField(required=False)
