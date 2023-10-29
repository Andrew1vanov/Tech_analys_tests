from django.contrib import admin
from .models import Post, Comment
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']#Лист с постами (внутри атрибуты постов)
    list_filter = ['status', 'created', 'publish', 'author']#Добваление листа с фильтрами
    search_fields = ['title', 'body']#Добваление строки поиска (в скобках объекты поиска)
    prepopulated_fields = {'slug': ('title',)}#сообщается автоматическое заполнение поля слуг из поля title
    raw_id_fields = ['author']#Изменения для поля заполнения автора в посте (теперь вместо всплывающего окна появляется строка поиска)
    date_hierarchy = 'publish' #Навигационные ссылки по иерархии дат
    ordering = ['status', 'publish']#Задаются дефолтные критерии сортировки

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']#Добваление листа с фильтрами
    search_fields = ['name', 'email', 'body']#Добваление строки поиска (в скобках объекты поиска)
