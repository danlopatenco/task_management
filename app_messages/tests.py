from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Conversation
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class MessagingAPITests(APITestCase):

    def setUp(self):
        # Create two users for the conversation
        self.user1 = User.objects.create_user(username='user1', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', password='testpassword2')

        # Create tokens for each user (if you're using token authentication)
        self.token_user1 = Token.objects.create(user=self.user1)
        self.token_user2 = Token.objects.create(user=self.user2)

        refresh_user_1 = RefreshToken.for_user(self.user1)
        refresh_user_2 = RefreshToken.for_user(self.user2)

        self.access_token_user_1 = str(refresh_user_1.access_token)
        self.access_token_user_2 = str(refresh_user_2.access_token)

    def test_create_conversation(self):

        headers = {
            'Authorization': f'Bearer {self.access_token_user_1}'
        }

        # User1 starts a conversation with User2
        url = reverse('conversation-list')  # Ensure you have set the correct name for the url
        data = {'recipient_id': self.user2.id, 'initial_message': 'Hello!'}
        response = self.client.post(url, data=data, headers=headers)

        # Check that the conversation was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 1)
        self.assertEqual(Conversation.objects.get().participants.count(), 2)

    def test_reply_to_conversation(self):
        headers = {
            'Authorization': f'Bearer {self.access_token_user_2}'
        }

        # First, create a conversation between user1 and user2
        conversation = Conversation.objects.create()
        conversation.participants.set([self.user1, self.user2])

        # Now user2 replies to the conversation
        url = reverse('message-list')  # Ensure you have set the correct name for the url
        data = {'conversation': conversation.id, 'content': 'Hi there!'}
        response = self.client.post(url, data=data, headers=headers)

        # Check that the message was created as a reply
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(conversation.messages.count(), 1)
        self.assertEqual(conversation.messages.first().content, 'Hi there!')
        self.assertEqual(conversation.messages.first().sender, self.user2)
