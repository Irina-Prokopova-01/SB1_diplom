from django.contrib import admin

from announcements.models import Announcement, Review


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "author", "price", "created_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "announcement", "author", "created_at")
