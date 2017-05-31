from __future__ import unicode_literals

from django.db import models

from django.contrib import messages

import re, bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
	def validate (self, postData):
		print ("**postData from views.py***", postData)
		errors = []
		if len(postData['first_name']) < 1:
			errors.append("First name must be at least 1 character, please.")
		
		if len(postData['last_name']) < 1:
			errors.append("Last name must be at least 1 character, please.")
		
		if len(postData['alias']) < 1:
			errors.append("Alias must be at least 1 character, please.")
		elif User.objects.filter( alias = postData['alias']).exists():
			errors.append("Alias is taken, please try again, sorry :(")
		
		if len(postData['email']) < 1:
			errors.append("Email can not be blank, please.")
		elif not EMAIL_REGEX.match (postData['email']):
			errors.append("Email must be a valid email address, please.")
		elif User.objects.filter( email = postData['email']).exists():
			errors.append("Email address is already been added to the database.  Please try another.")
		
		if len(postData['password']) < 8 or len(postData['password']) > 16:			
			errors.append("Password must have more than 8 characters, please.")
		
		if postData['confirm_password'] != postData['password']:			
			errors.append("Passwords must match, please.")
		
		if len(postData['date_of_birth']) < 1:
			errors.append("Date of Birth must not be blank, please.")
		print errors
		if len(errors) == 0:
			return True
		else:
			return(False, errors)

	def login(self, postData):
		print "***************"
		print postData
		try:
			logPostData = User.objects.get(email=postData['email'])
			print logPostData.email
			print logPostData.password
		except:
			return (False, "Please try again, your password or username is not valid ")
		if logPostData.password == bcrypt.hashpw(postData['password'].encode(), logPostData.password.encode()):
			return (True, "Congrats! You successfully logged in.", logPostData.first_name)
		else:
			return (False, "Please try again, your password or username is not valid ")




class User(models.Model):
	first_name= models.CharField(max_length=255)
	last_name= models.CharField(max_length=255)
	alias= models.CharField(max_length=255)
	email= models.EmailField(max_length=255)
	password= models.CharField(max_length=255)
	date_of_birth= models.DateTimeField(auto_now_add=True)
	created_at= models.DateTimeField(auto_now_add=True)
	updated_at= models.DateTimeField(auto_now=True)
	objects= UserManager()