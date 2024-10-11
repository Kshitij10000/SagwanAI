from django.contrib import admin
from .models import FyersCredentials

@admin.register(FyersCredentials)
class FyersCredentialsAdmin(admin.ModelAdmin):
    list_display = ('user', 'broker', 'client_id', 'created_at', 'updated_at')
    search_fields = ('user__username', 'client_id')
    list_filter = ('broker', 'created_at')
    readonly_fields = ('created_at', 'updated_at')  # Prevent editing timestamps

