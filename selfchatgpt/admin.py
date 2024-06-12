from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone
from .models import ChatHistory

class CustomDateFilter(admin.SimpleListFilter):
    title = _('Custom Date Filter')
    parameter_name = 'custom_date'

    def lookups(self, request, model_admin):
        return (
            ('past_week', _('Past Week')),
            ('past_month', _('Past Month')),
            ('past_year', _('Past Year')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'past_week':
            return queryset.filter(timestamp__gte=timezone.now() - timedelta(days=7))
        elif self.value() == 'past_month':
            return queryset.filter(timestamp__gte=timezone.now() - timedelta(days=30))
        elif self.value() == 'past_year':
            return queryset.filter(timestamp__gte=timezone.now() - timedelta(days=365))

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_question', 'system_response', 'timestamp')
    list_filter = (CustomDateFilter,)

admin.site.register(ChatHistory, ChatHistoryAdmin)

