from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager 

# Create your models here.

#Создание моделей данных блога

#Создание модельных менеджеров - определяет правила извлечения объектов при запросе к базе данных
class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()\
            .filter(status = Post.Status.PUBLISHED)

#Создание модели поста
class Post(models.Model):

        #2 Добавление поля статуса
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length= 250)#charfield - поле, которое транслируется в столбец VARCHAR в базе данных SQL
    slug = models.SlugField(max_length= 250, 
        unique_for_date= 'publish')#slugfield - поле, которое -||-. СЛаг - это короткая метка 
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'blog_posts')
    #on_delete - определяет поведение, которое следует применять при удалении объекта, на который есть ссылка
    #related_name - указывает имя обратной связи
   
    body = models.TextField()# поле для хранения текста поста. TextField - поле, которое транслируется в столбец text в базе SQL
    
    #Добавление параметров даты/времени
    publish = models.DateTimeField(default= timezone.now)#Поле dateTimeField - транслируется в столбец DAtetime базы SQL
    #Используется для хранения даты и времени публикации поста
    created = models.DateTimeField(auto_now_add = True)#Будет использоваться для хранения даты и времени создания поста
    #при применении параметра auto_now_add - дата будет сохраняться автоматически во время создания объекта
    update = models.DateTimeField(auto_now = True)# будет использовано для хранения последней даты и времени обновления поста
    # при применении параметра auto_now - дата будет обновляться автоматически во время сохранения объекта
    status = models.CharField(max_length= 2, choices= Status.choices, default= Status.DRAFT)
    
    objects = models.Manager() # Менеджер применяемый по умолчанию 
    published = PublishedManager() # конкретно-прикладной менеджер
    
    #1 Определение предустановленного порядка сортировки
    class Meta: #создание метакласса, определяет метаданные модели. 
        ordering = ['-publish'] #Атрибут ordering - сообщает django что должен сортировать результаты по полю publish
        
        #добавление индекса базы данных
        indexes = [
            models.Index(fields = ['publish']), 
                   ]
    
    tags = TaggableManager()
    


    def __str__(self): # __str__ - метод, который применяется по умолчанию
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args = [self.publish.year,
                                                   self.publish.month,
                                                   self.publish.day,
                                                   self.slug])
        #reverse - формирует url адрес динамически, по имени и любым требуемым параметрам
        #именное пространство blog определено в главном файле urls.py


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, 
                             related_name= 'comments')
    #related_name - назначет имя атрибуту для связи от ассоциированного объекта назад к нему
    name = models.CharField(max_length= 80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now= True)
    active = models.BooleanField(default= True)#Позволяет деактивировать комментарии через админку

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields = ['created'])]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'