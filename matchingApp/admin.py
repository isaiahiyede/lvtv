from django.contrib import admin
from models import MatchParticipants, MessageCenterComment, Comment

# Register your models here.
admin.site.register(MatchParticipants)
admin.site.register(MessageCenterComment)
admin.site.register(Comment)