from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
# Create your views here.

#Создание представления
def post_list(request, tag_slug = None):
    post_list = Post.published.all()
    
    #Добавление соритровки по тегам
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        post_list = post_list.filter(tags__in = [tag])
    
    #Постраничная разбивка (после шаблона отображения постранично разбитых ссылок)
    paginator = Paginator(post_list, 3) # 3 - число возвращаемых объектов на страницу, post_list - объекты
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        #Если номер не целое число, то возвращается первая страница
        posts = paginator.page(1)
    except EmptyPage:
        #Если pagenumber находится вне диапазона- выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag}) 
#render - функция сокращенного доступа. принимает объект request, путь к шаблону и контекстные переменный
#Возвращает объект ХТТП с прорисованным текстом (обычно исходным кодом ХТМЛ)

from django.http import Http404

def post_detail(request, year, month, day, post):
    ##Походу устаревшая версия или альтернативный способ исполнения ошибки и доступа к един. посту
    #try:
    #    post = Post.published.get(id = id)
    #except Post.DoesNotExist:
    #    raise Http404('No Post found')
    
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED, 
                             slug = post,
                             publish__year = year, 
                             publish__month = month,
                             publish__day = day)
    #Данная функция извлекает объект, соответствующий переданным параметрам, либо возвращает ошибку
    #Список активных комментариев к этому посту
    comments = post.comments.filter(active = True)
    form = CommentForm()

    #Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat = True)
    #1 - Извлечение списка идентификаторов тегов текущего посtа
    #values_list() - возвращает кортежи со значениями заданных полей
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id = post.id)
    #2 - Берутся все посты, содержащие любой из этих тегов, за исключением текущего
    similar_posts = similar_posts.annotate(same_tags = Count('tags'))\
        .order_by('-same_tags','-publish')[:4]
    # Применяется функция агрегирования count. она генерирует вычисляемое поле same_tags, 
    #которое содержит число тегов, общих со всеми запрошенными тегами


    return render(request, 
                  'blog/post/detail.html', 
                  {'post': post, 'comments': comments, 'form': form, 
                   'similar_posts': similar_posts})



class PostListView(ListView):
    '''Альтернативное представление списка постов'''
    queryset = Post.published.all()#Используется для того, чтобы иметь конкретно-прикладной набор
    #запросов QuerySet, не извлекая все объекты
    context_object_name = 'posts' #Контектская переменная используется для результатов запроса
    paginate_by = 3# Задается постраничная разбивка 
    template_name = 'blog/post/list.html'#конкретно-прикладной шаблон используется для прорисовки

#Работа с электронной почтой
from django.core.mail import send_mail

def post_share(request, post_id):
    post = get_object_or_404(Post, 
                            id = post_id, 
                            status = Post.Status.PUBLISHED)
    
    sent = False

    if request.method == 'POST':
        #Передача формы на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #ПОля формы успешно прошли валидацию
            cd = form.cleaned_data
            # ...отправка электронного письма
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} /n/n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'andrew11.12.97@mail.ru', [cd['to']])
            
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id, status = Post.Status.PUBLISHED)
    comment = None

    #Комментарий был отправлен
    form = CommentForm(data = request.POST)
    if form.is_valid():
        #Создать объект класса Comment, не сохраняя его в базе данных 
        comment = form.save(commit = False)
        #Назначить пост комментарию
        comment.post = post
        #Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form':form, 'comment':comment})