from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.db import models
from .models import Task


class AssignedToAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # Correct usage of queryset
        widget=FilteredSelectMultiple('Assigned to', False),
        required=False)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("pk", "created_by", 'title', 'description', 'deadline', 'status', 'project', 'assigned_task_to')

    form = AssignedToAdminForm

    def assigned_task_to(self, obj):
        assigned_users = obj.assigned_to.all()
        return ', '.join([user.username for user in assigned_users])

    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('Assigned to', False)},
    }


# class TaskInline(admin.TabularInline):
#     model = Task
#     extra = 1  # Number of empty forms to display
#     formfield_overrides = {
#         models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': 10})},
#     }

# class ProjectAdminForm(forms.ModelForm):
#     team_members = forms.ModelMultipleChoiceField(
#         queryset=User.objects.all(),
#         widget=forms.SelectMultiple(attrs={'size': 10}),
#     )

#     class Meta:
#         model = Project
#         fields = '__all__'

# class ProjectAdmin(admin.ModelAdmin):
#     form = ProjectAdminForm
#     list_display = ('title', 'description', 'start_date', 'end_date')
#     filter_horizontal = ('team_members',)
#     inlines = [
#         TaskInline,
#     ]

#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related('tasks')

# admin.site.register(Project, ProjectAdmin)


# class UserAdmin(UserAdmin):
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    # list_filter = ('is_staff', 'is_active', 'groups', 'user_permissions')
    # search_fields = ('username', 'email', 'first_name', 'last_name')
    # filter_horizontal = ('groups', 'user_permissions')

    # def get_projects(self, obj):
    #     return ", ".join([project.title for project in obj.projects.all()])

    # get_projects.short_description = 'Projects'

    # def get_tasks(self, obj):
    #     return ", ".join([task.title for task in obj.assigned_tasks.all()])

    # get_tasks.short_description = 'Assigned Tasks'

    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    #     ('Projects and Tasks', {'fields': ('get_projects', 'get_tasks')}),
    # )

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
