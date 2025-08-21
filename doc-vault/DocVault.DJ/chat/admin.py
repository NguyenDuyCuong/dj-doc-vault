from django.contrib import admin

from notifications.utils import get_notification_model
from .models import ChatSession, ChatSessionMember, ChatSessionMessage


admin.site.register((ChatSession, ChatSessionMember, ChatSessionMessage))


Notification = get_notification_model()
admin.site.register(Notification)
