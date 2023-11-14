from rest_framework import serializers
from .models import Message, Conversation
from django.contrib.auth import get_user_model
from django.db import transaction


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages']


class CreateConversationSerializer(serializers.ModelSerializer):
    initial_message = serializers.CharField(write_only=True)
    recipient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Conversation
        fields = ['initial_message', 'recipient_id']

    def validate_recipient_id(self, value):
        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Recipient user does not exist.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            initial_message_content = validated_data.pop('initial_message')
            recipient_id = validated_data.pop('recipient_id')
            recipient = User.objects.get(pk=recipient_id)
            sender = self.context['request'].user

            # Create the conversation instance without setting participants
            conversation = Conversation.objects.create()

            # Now use set() to establish the many-to-many relationship
            conversation.participants.set([sender, recipient])

            # Create the initial message
            Message.objects.create(
                conversation=conversation,
                sender=sender,
                content=initial_message_content
            )
            return conversation
