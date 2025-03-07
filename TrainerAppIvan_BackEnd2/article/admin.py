from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['name', 'brief_description', 'image1', 'image2', 'image3']  # Fields to display in list view
    search_fields = ['name', 'brief_description']  # Fields that can be searched in the admin interface
    list_filter = ['name']  # Filter options for the admin list view


