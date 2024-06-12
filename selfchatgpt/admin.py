from django.contrib import admin
from .models import *

@admin.register(TalkItem)
class TalkItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'time')