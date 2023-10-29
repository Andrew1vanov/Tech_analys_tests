from django import forms
from .models import Comment
#Создание формы для отображения мэйл переписки

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length = 25)#Используется для имени человека
    email = forms.EmailField()# мыло отпрваляющего 
    to = forms.EmailField()
    comments = forms.CharField(required = False, widget = forms.Textarea)#Используется для комментариев

#Создание форм из моделей
class CommentForm(forms.ModelForm):
    #базовый класс ModelForm - позволяет использовать приемущества модели Comment и компанует форму динамически
    '''Для того чтобы формировать форму из модели необходимо в классе Meta указать модель
    по которой создается компановка формы'''
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
