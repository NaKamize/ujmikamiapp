from django.contrib import admin
from .models import Project, ProjectLink, Tag


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'created_at']
    list_filter = ['category', 'tags']
    search_fields = ['title', 'description']
    inlines = [ProjectLinkInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
