# time_tracking/admin.py

from django.contrib import admin
from .models import TimeEntry, TimeTracker

admin.site.register(TimeEntry)
admin.site.register(TimeTracker)
