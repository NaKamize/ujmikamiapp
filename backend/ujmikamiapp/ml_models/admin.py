from django.contrib import admin
from .models import MLModel, MLModelLink


class MLModelLinkInline(admin.TabularInline):
    model = MLModelLink
    extra = 1


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'architecture', 'rank', 'score', 'order']
    list_filter = ['category', 'architecture', 'framework']
    search_fields = ['title', 'description', 'competition_name']
    inlines = [MLModelLinkInline]
