from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

#Создание просто шаблонного тега
register = template.Library() #Важная штука для создания шаблонных тегов

@register.simple_tag #регистрирует как простой тег(в скобки можно добавить желаемое имя)(возвращает строковый литерал)
def total_posts():
    '''Простой шаблонный тег, возвращающий общее количество постов'''
    return Post.published.count() #count - количество

@register.inclusion_tag('blog/post/latest_posts.html')#возвращает прорисованный шаблон
def show_latest_posts(count = 5):
    '''Отображает последние посты на боковой панели'''
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count = 5):
    '''Возвращает посты с наибольшим числом комменатриев'''
    return Post.published.annotate(total_comments = Count('comments')
                                   ).order_by('-total_comments')[:count]
#С помощью функции annotate формируется набор запросов QuerySet(ленивые запросы), 
# чтобы агрегировать общее число комментариев к каждому посту
# order_by - возвращает соритрованный массив

##СОздание шаблонного фильтра
#Регистрируются также как шаблонные теги
#Какая-то хуйня на самом деле

@register.filter(name = 'markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
#mark_safe - помечает результат как безопасный для прорисовки в шаблоне исходный код HTML
