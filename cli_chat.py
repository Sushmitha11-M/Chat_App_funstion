import sys
import os

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

import django
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from chat_app.models import Conversation, Message
def start_chat(user1, user2):
    try:
        user1_obj = User.objects.get(username=user1)
        user2_obj = User.objects.get(username=user2)
    except User.DoesNotExist:
        print("Error: One or both users do not exist.")
        sys.exit(1)

    conversation, created = Conversation.objects.get_or_create(user1=user1_obj, user2=user2_obj)
    return conversation

def send_message(conversation, sender,  content):
    message = Message.objects.create(conversation=conversation, sender=sender,content=content)
    return message
#sender=sender,
def display_messages(conversation):
    messages = Message.objects.filter(conversation=conversation)
    for message in messages:
        timestamp_local = timezone.localtime(message.timestamp)
        print(f"{message.sender}: {message.content} ({timestamp_local})")

def main():
    if len(sys.argv) != 3:
        print("Usage: python cli_chat.py <user1> <user2>")
        sys.exit(1)

    user1 = sys.argv[1]
    user2 = sys.argv[2]

    print(f"Conversation started between {user1} and {user2}")

    conversation = start_chat(user1, user2)

    try:
        while True:
            sender = input("Enter your name (type 'exit' to quit): ")
            if sender.lower() == 'exit':
                break

            content = input("Enter your message (press Enter to exit): ")
            if not content:
                break

            send_message(conversation, sender, content)
            display_messages(conversation)
    except KeyboardInterrupt:
        print("\nScript interrupted. Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
