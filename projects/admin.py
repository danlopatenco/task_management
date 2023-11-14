from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Project
from django import forms
from tasks.models import Task


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=FilteredSelectMultiple('Tasks', False),
        required=False)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ("pk", 'title', 'description', 'start_date', 'end_date', 'team_members_display', 'tasks_display')

    def team_members_display(self, obj):
        return ', '.join([user.username for user in obj.team_members.all()])

    team_members_display.short_description = 'Team Members'

    # Define formfield_overrides to use FilteredSelectMultiple for team_members
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('Team Members', False)},
    }

    def tasks_display(self, obj):
        return ', '.join([task.title for task in obj.tasks.all()])
