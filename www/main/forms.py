from django import forms
from .models import *

class LoginForm(forms.Form):
	login = forms.CharField(label="Логин", required=True, widget = forms.TextInput(attrs={'placeholder': "Введите ваш логин..."}), max_length=50 )
	password = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput(attrs={'placeholder': "Введите ваш пароль..."}), max_length=150)

class CreationForm(forms.Form):
	username = forms.CharField(label="Логин", required=True, widget = forms.TextInput(attrs={'placeholder': "Логин пользователя..."}), max_length=50)
	password = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput(attrs={'placeholder': "Пароь пользователя..."}), max_length=150)
	group = forms.ChoiceField(label = "Группа бзопасности", widget = forms.Select(), choices = ([('Студент','Студент'), ('Преподаватель','Преподаватель'),('Модератор','Модератор'), ]), required = True)

class NewAchievment(forms.Form):
	title = forms.CharField(label="Наименование достижения", required=True, max_length=50, widget = forms.TextInput(attrs={'placeholder': "Полное наименование достижения..."}),)
	desciption = forms.CharField(label="Описание достижения", max_length = 500, required=True, 
		widget=forms.Textarea(attrs={'rows': 5, 'placeholder': "Где, когда и за что получили достижение..."}))

class DownloadImg(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(DownloadImg, self).__init__(*args, **kwargs)
		self.fields['img'].label = "Новое изображение профиля (180px X 180px)"
	class Meta:
		model = ImageDownload
		fields=['img']