from django.contrib.sitemaps import Sitemap
from .models import Post

#Определение конкретно-прикладной карты сайта
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        '''Набор запросов, подлежащих включению в карту сайта'''
        return Post.published.all()
    
    def lastmod(self, obj):
        '''получает каждый возвращаемый методом items объект и 
        возвращает время послденего изменения'''
        return obj.updated
    
