import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# -------------------------------------------------------------------
#  Custom User model
# -------------------------------------------------------------------
class User(AbstractUser):
    """
    Extends Django's AbstractUser to add custom fields and use UUID as primary key.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # username still required internally

    def __str__(self):
        return f"{self.email} ({self.role})"


# -------------------------------------------------------------------
#  Conversation model
# -------------------------------------------------------------------
class Conversation(models.Model):
    """
    Represents a chat thread between multiple participants.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# -------------------------------------------------------------------
#  Message model
# -------------------------------------------------------------------
class Message(models.Model):
    """
    A single message sent in a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.email}"
