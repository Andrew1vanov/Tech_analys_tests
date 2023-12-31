# Tech_analys_tests
Technical analys tests numpy and ML 

# Создание проекта django
Консольные команды
.\my_env\Scripts\activate - активация виртуального пространства
1. django-admin startproject mysite - создание проекта 
2. cd mysite -> python manage.py migrate - создание таблицы, ассоциированную с моделями стандартных приложений django
3. python manage.py runserver - запуск локального сервера для разработки
3.1 python manage.py runserver 127.0.0.1:8001 -- settings=mysite.settings - сообщение что нужно загрузить конкретный настроечный файл
4. python manage.py startapp blog - создаине приложения 

проект - это сам web сайт создаваемый в django; приложение - функционал, который используется в проекте

5. python manage.py makemigrations blog - создает миграции добавленные в файле блог
6. python manage.py migrate - повторная активация миграций
7. python manage.py createsuperuser - создание админа (пароль сделал 123, имя - admin)
8. python manage.py runserver - запуск сервера разработки

# Команды для работы с базой данных
>>> from blog.models import User
>>> user = User.objects.get(username = 'admin')
метод get() позволяет извлекать из базы данных только один объект
>>> post = Post(title = 'Another post', slug = 'another-post', body = 'Post body', author = user)
>>> post.save() - сохранение в базе данных (выполняет инструкцию SQL INSERT)

>>> Post.objects.create(title = 'One more post', slug = 'one-more-post', body = 'Post body', author = user) - создание еще одно поста напряму при помощи create()

# Обновление объектов базы данных
>>> post.title = 'New title'
>>> post.save() - на этот раз метод исполняет инструкцию SQL UPDATE

# Извлечение объектов
>>> all_posts = Post.objects.all() - извлекает все объекты пост из базы данных
>>> Post.objects.all() - прямой вызов базы. Выполняется мгновенно в отличие от предыдущей сточки, которя не исполняется сразу, а ожидает первого вызова переменной

# Применение метода filter()
>>> Post.objects.filter(publish__year = 2023)
>>> Post.objects.filter(publish__year = 2023, author__username = 'admin')

# Удаление объектов
>>> post = Post.objects.get(id= )
>>> post.delete()

# Порядок работы при добавление моделей, форм
1 - Создание модели 
2 - Создание для неё формы (можно и без модели, если нужен пустой функционал)
3 - Создание представления для формы
4 - Добавление в urls нового запроса по созданному представлению
5 - Создание html шаблона для прорисовки формы

После внесения в models новой модели запросов к базе данных (вместо objects теперь используется published) можно пользоваться сразу фильтрованным запросом, в данном случае был выбор по публикации
# >>> Post.published.filter(title__startswith = 'Who')

# Справка по html
{% tag %} - шаблонные теги, управляют прорисовкой шаблона
{{ variable }} - шаблонные переменные, заменяются значениями при прорисовке шаблона
{{ variable|filter}} - шаблонные фильтры, позволяют видоизменять отображаемые переменные

Конкретно к проекту 
{% load static %} - сообщает джанго, что нужно загрузить статические шаблонные теги. После их загрузки шаблонный тег {% static %} можно использовать во всем шаблоне. С помощью указанного шаблонного тега можно вставлять статические файлы, такие как файл blog.css, который находится в исходном коде данного примера в каталоге static/ приложения blog.

{% block %} - сообщают джанго, что нужно определить блок в отмеченной области. Шаблоны, которые наследуют от этого шаблона, могут заполнять блок контентом. 
{% exntends %} - сообщает джанго, что надо наследовать от шаблона blog/base.html. Затем заполняются блоки title и content базового шаблона.
{% url %} - представляемый джанго шаблонный тег, для формирования URL-адреса. Позволяет формировать адреса динамически по их имени.

<h3></h3> - внутри ставится текст. Цифра указывает на размер шрифта. Меньше цифра -> больше шрифт
<ul></ul> - создает абзацный отсутп. Все что внутри будет с этим отступом

# После обноволения основной модели необходимо применять миграции 
# python manage.py makemigrations blog -> python manage.py migrate 

С горем пополам сделал мыло, отправка не работает кстати.


## Справка блять
# 1. Экземпляр - единичный вызов класса (sc = LogisticRegression())
# 2. Обработка ошибок происходит другим образом, потому что ошибки выводятся не консоль,
# а напрямую в веб-приложение
# 3. Представление - визуализирует на шаблоне html модель или форму через вызов
# соответствующего экземпляра 

#