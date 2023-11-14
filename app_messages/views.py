from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer, CreateConversationSerializer
from .permisions import IsParticipant


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    basename = 'conversations'

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateConversationSerializer
        return ConversationSerializer

    def get_queryset(self):
        # Only return conversations where the user is a participant.
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    basename = 'messages'

    def get_queryset(self):
        # Only return messages where the user is a participant of the conversation.
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(conversation__in=user_conversations)

    def perform_create(self, serializer):
        # Check if the conversation is between the sender and exactly one other user.
        conversation = serializer.validated_data['conversation']
        if len(conversation.participants.all()) != 2 or self.request.user not in conversation.participants.all():
            raise ValidationError("You can only send messages within a two-person conversation.")
        serializer.save(sender=self.request.user)
