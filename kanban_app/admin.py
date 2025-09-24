from django.contrib import admin
from .models import Board

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "member_count", "ticket_count")
    search_fields = ("title", "owner__email")
    list_filter = ("owner",)
