from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]  # Fields to display in list view
    search_fields = ['id', 'name', ]  # Fields that can be searched in the admin interface
    list_filter = ['id', 'name']  # Filter options for the admin list view


