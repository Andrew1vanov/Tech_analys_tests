from django.urls import path
from . import views
from .feeds import LatestPostsFeed

#Добавление шаблонов URL-адресов представлений
#Позволяют соотносить URL-адреса с представлениями
app_name = 'blog'

#Шаблон адреса состоит из строкового шаблона, представления и имени, которое позволяет именовать 
# адрес в масштабе всего проекта

urlpatterns = [
    #Представления поста
    path('', views.post_list, name = 'post_list'),
    #path('', views.PostListView.as_view(), name = 'post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name = 'post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name = 'post_detail'),
    path('<int:post_id>/share/', views.post_share, name = 'post_share'),
    path('<int:post_id>/comment/', views.post_comment, name = 'post_comment'), 
    path('feed/', LatestPostsFeed(), name = 'post_feed'),

]

