from django.db import models
import json
import hashlib
import datetime

class DataBase:
	def __init__(self):
		self.users = Users()
		self.achiev = Achievements()

class User:
	def __init__(self, id, username, password, group, photo):
		self.id = id
		self.username = username
		self.password = password
		self.group = group #student/teacher/moderator
		self.photo = photo

class Users:
	def __init__(self):
		self.path = 'main/data/users.json'
		self.users = []
		self.load_js()
	def save(self):
		with open(self.path, 'w', encoding="utf-8") as file: json.dump(self.get_list(), file)
	def load_js(self):
		with open(self.path, 'r', encoding="utf-8") as file:
			text = json.loads(file.read())
		for each in text["users"]: self.users.append(User(each["id"],each["username"],each["password"],each["group"],each["photo"]))
	def auth(self, username, password):
		password = password[:int(len(password)/2)] + str(username) + password[int(len(password)/2):]
		byted = bytes(password, "utf-8")
		hashed = hashlib.sha1(byted)
		password = hashed.hexdigest()
		for user in self.users:
			if (user.username == username) and (user.password == password): return user
	def create_user(self, username, password, group):
		password = password[:int(len(password)/2)] + str(username) + password[int(len(password)/2):]
		byted = bytes(password, "utf-8")
		hashed = hashlib.sha1(byted)
		password = hashed.hexdigest()
		ids = []
		users = self.get_list()["users"]
		photo = '../media/default.jpg'
		for each in users: ids.append(each["id"])
		if len(ids) == 0: user_id = 0
		else: user_id = max(ids)+1
		for each in self.users:
			if username == each.username:
				return False
		else:
			self.users.append(User(user_id, username, password, group, photo))
			self.save()
			return True
	def get_list(self):
		data=[]
		for each in self.users:
			data.append({"id": each.id, "username": each.username, "password": each.password, "group": each.group, "photo": each.photo})
		return {"users": data}
	def new_group(self, username, newGroup):
		for each in self.users:
			if each.username == username:
				each.group = newGroup
				self.save()
				return each.group
	def delete_user(self, username):
		for each in self.users:
			if each.username == username:
				self.users.remove(each)
				self.save()
				break
	def change_photo(self, photo, username):
		new_photo = '../media/' + str(photo)
		for each in self.users:
			if each.username == username:
				each.photo = new_photo
				self.save()
				return each.photo

class ImageDownload(models.Model):
	img = models.ImageField(upload_to='')

class Achievment:
	def __init__(self, id, title, date, author, flag, checker, description):
		self.id = id
		self.title = title
		self.date = date
		self.author = author
		self.flag = flag
		self.checker = checker
		self.description = description

class Achievements:
	def __init__(self):
		self.path = 'main/data/achieves.json'
		self.achieves = []
		self.load_js()
	def save(self):
		with open(self.path, 'w', encoding="utf-8") as file: json.dump(self.get_list(), file)
	def load_js(self):
		with open(self.path, 'r', encoding="utf-8") as file:
			text = json.loads(file.read())
		for each in text["achieves"]: self.achieves.append(Achievment(each["id"],each["title"],each["date"],each["author"],each["flag"],each["checker"],each["description"]))
	def create_achieve(self, title, author, description):
		today = datetime.datetime.today()
		date = today.strftime("%d/%m/%Y %H:%M:%S")
		ids = []
		achieves = self.get_list()["achieves"]
		for each in achieves: ids.append(each["id"])
		if len(ids) == 0: achieve_id = 0
		else: achieve_id = max(ids)+1
		for each in self.achieves:
			if title == each.title and author==each.author:
				return False
		else:
			self.achieves.append(Achievment(achieve_id, title, date, author, 0, 0, description))
			self.save()
			return True
	def delete_achieve(self, id):
		for each in self.achieves:
			if each.id == id:
				self.achieves.remove(each)
				self.save()
				break
	def get_list(self):
		data=[]
		for each in self.achieves:
			data.append({"id": each.id, "title": each.title, "date": each.date, "author": each.author, "flag": each.flag, "checker": each.checker, "description": each.description})
		return {"achieves": data}
	def check(self, flag, id, checker):
		for each in self.achieves:
			if each.id == id:
				each.flag = flag
				each.checker = checker
				self.save()
				break