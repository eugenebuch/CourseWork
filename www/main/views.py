from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
import json


def current_user(sess, request):
		sess['user_login']=request.session['user_login']
		sess['user_group']=request.session['user_group']
		sess['user_photo']=request.session['user_photo']
	

def home(request):
	database = DataBase()
	with open('main/data/cafedras.json', 'r', encoding="utf-8") as file:
		text = json.loads(file.read())
	data = text["cafedras"]
	session = {}
	try: 
		current_user(session, request)
	except: 
		print("We've got a bad news, sir")
		return redirect('auth')
	if request.method == "POST":
		photo_form = DownloadImg(request.POST, request.FILES)
		photo_form.save()
		database.users.change_photo(request.FILES['img'], request.session['user_login'])
		request.session['user_photo'] = '../media/' + str(request.FILES['img'])
		current_user(session, request)
	else:
		photo_form = DownloadImg()
	session['title'] = 'Кафедры'
	session['cafedras'] = data
	session['photo_form'] = photo_form
	return render(request, 'main/home.html', session)

def auth(request):
	data = DataBase()
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user_login = request.POST['login']
			user_pass = request.POST['password']
			current_u = data.users.auth(user_login, user_pass)
			try:
				if current_u.group == "Заблокирован":
					messages.error(request, f'Вы заблокированы в системе. Пожалуйста, свяжитесь с модерацией системы.')
				else:
					request.session['user_login'] = current_u.username
					request.session['user_group'] = current_u.group
					request.session['user_photo'] = current_u.photo
					return redirect('home')
			except:
				messages.error(request, f'Неверный логин и/или пароль!')
		else: print("Invalid form!")
	else: 
		try: 
			if request.session['user_login']: return redirect('home')
		except: form = LoginForm()
	return render(request, "main/auth.html", {'form': form, 'title': 'Авторизация'})

def achiev(request):
	session = {}
	current_user(session, request)
	session['title'] = 'Достижения студентов'
	data = DataBase()
	achieves = data.achiev.get_list()
	session["achieves"] = achieves["achieves"]
	if request.method=="POST":
		form = NewAchievment(request.POST)
		photo_form = DownloadImg(request.POST, request.FILES)
		if "agree" in request.POST.keys():
			request.POST.get("agree")
			data.achiev.check(1, int(request.POST.get("agree")), request.session['user_login'])
		elif "disagree" in request.POST.keys():
			data.achiev.check(2, int(request.POST.get("disagree")), request.session['user_login'])
		elif "delete" in request.POST.keys():
			data.achiev.delete_achieve(int(request.POST['delete']))
			session = data.achiev.get_list()
		elif "save" in request.POST.keys():
			if data.achiev.create_achieve(request.POST['title'], request.session['user_login'], request.POST['desciption']):
				messages.success(request, f'Ваше достижение успешно добавлено! Скоро его проверят...')
			else: messages.error(request, f'Вы уже добавляли это достижение...')
			session = data.users.get_list()
		elif "save_photo" in request.POST.keys():
			photo_form.save()
			data.users.change_photo(request.FILES['img'], request.session['user_login'])
			request.session['user_photo'] = '../media/' + str(request.FILES['img'])
			current_user(session, request)
	else:
		form = NewAchievment()
		photo_form = DownloadImg()
	session = data.achiev.get_list()
	session['title'] = 'Достижения студентов'
	try:
		current_user(session, request)
	except:
		print("Sounds bad!")
	session['form'] = form
	session['photo_form'] = photo_form
	return render(request, "main/achiev.html", session)

def manage(request):
	photo_form = DownloadImg()
	if request.session['user_group'] == "Модератор":
		session = {}
		try:
			current_user(session, request)
		except:
			print("Sounds bad")
		session['title'] = 'Управление пользователями'
		data = DataBase()
		users = data.users.get_list()
		session["users"] = users["users"]
		if request.method == "POST":
			form = CreationForm(request.POST)
			photo_form = DownloadImg(request.POST, request.FILES)
			if "give_student" in request.POST.keys():
				user_update = request.POST.get("give_student")
				data.users.new_group(user_update, "Студент")
				if user_update == session['user_login']: request.session['user_group'] = "Студент"
				if request.session['user_group'] != "Модератор": return redirect('home')
			elif 'give_teacher' in request.POST.keys():
				user_update = request.POST.get("give_teacher")
				data.users.new_group(user_update, "Преподаватель")
				if user_update == session['user_login']: request.session['user_group'] = "Преподаватель"
				if request.session['user_group'] != "Модератор": return redirect('home')
			elif "give_moderator" in request.POST.keys():
				user_update = request.POST.get("give_moderator")
				data.users.new_group(user_update, "Модератор")
				if request.session['user_group'] != "Модератор": return redirect('home')
			elif "lock" in request.POST.keys():
				user_update = request.POST.get("lock")
				data.users.new_group(user_update, "Заблокирован")
				if request.session['user_group'] != "Модератор": return redirect('home')
			elif "unlock" in request.POST.keys():
				user_update = request.POST.get("unlock")
				data.users.new_group(user_update, "Студент")
				if request.session['user_group'] != "Модератор": return redirect('home')
			elif "save" in request.POST.keys():
				if data.users.create_user(request.POST['username'], request.POST['password'], request.POST['group']):
					messages.success(request, f'Пользователь ' + request.POST['username'] + ' успешно добавлен!')
				else: messages.error(request, f'Такое имя уже занято!')
				session = data.users.get_list()
				return redirect('manage')
			elif "delete" in request.POST.keys():
				data.users.delete_user(request.POST['delete'])
				session = data.users.get_list()
			elif "save_photo" in request.POST.keys():
				photo_form.save()
				data.users.change_photo(request.FILES['img'], request.session['user_login'])
				request.session['user_photo'] = '../media/' + str(request.FILES['img'])
				current_user(session, request)
		else:
			form = CreationForm()
			photo_form = DownloadImg()
		session = data.users.get_list()
		session['title'] = 'Управление пользователями'
		try:
			current_user(session, request)
		except:
			print("Sounds bad!")
		session['form'] = form
	else:
		return redirect('home')
	session['photo_form'] = photo_form
	return render(request, "main/manage.html", session)

def exit(request):
	request.session.clear()
	return redirect('auth')