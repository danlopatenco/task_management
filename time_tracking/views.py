from django.utils import timezone
from rest_framework import viewsets, permissions, status
from .models import TimeEntry, TimeTracker
from .serializers import TimeEntrySerializer, TimeTrackerSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer
    permission_classes = [permissions.IsAuthenticated]


class TimeTrackerViewSet(viewsets.ModelViewSet):
    queryset = TimeTracker.objects.all()
    serializer_class = TimeTrackerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["POST"])
    def start_tracking(self, request):
        user = request.user
        task_id = request.data.get('task_id')

        try:
            # Check if a TimeTracker for this user and task already exists
            time_tracker = TimeTracker.objects.get(user=user, task_id=task_id)

            if not time_tracker.is_running:
                # If the tracker is not running, start it
                time_tracker.is_running = True
                time_tracker.start_time = timezone.now()
                time_tracker.save()

                return Response({'message': 'Tracking started.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Tracking is already running.'}, status=status.HTTP_200_OK)

        except TimeTracker.DoesNotExist:
            # If a TimeTracker doesn't exist for this user and task, create one
            TimeTracker.objects.create(user=user, task_id=task_id, is_running=True, start_time=timezone.now())

            return Response({'message': 'Tracking started.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def stop_tracking(self, request):
        user = request.user
        task_id = request.data.get('task_id')

        try:
            # Check if a TimeTracker for this user and task exists
            time_tracker = TimeTracker.objects.get(user=user, task_id=task_id)

            if time_tracker.is_running:
                # If the tracker is running, stop it and create a TimeEntry
                time_tracker.is_running = False
                time_tracker.save()

                start_time = time_tracker.start_time
                end_time = timezone.now()

                TimeEntry.objects.create(user=user, task_id=task_id, start_time=start_time, end_time=end_time)

                return Response({'message': 'Tracking stopped and time entry created.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Tracking is not running.'}, status=status.HTTP_200_OK)

        except TimeTracker.DoesNotExist:
            return Response({'message': 'No active tracking session for this user and task.'}, status=status.HTTP_200_OK)
