from django.shortcuts import render, redirect
from models import User
from django.contrib import messages
import bcrypt


def index(request):
	# check = User.objects.get(email="pass@word.com")
	# print check
	return render(request, "belt3_app/index.html")

def register(request):
	print ("**FORM DATA**", request.POST)
	is_validated = User.objects.validate(request.POST)

	if is_validated == True:
		user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],alias=request.POST['alias'],email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()),date_of_birth=request.POST['date_of_birth'])
		print ("************************************************************",user)
		request.session['first_name'] = request.POST['first_name']
		messages.success(request, "Congrats! You successfully registered.")
		return redirect('/success')
	else:
		print is_validated
		errors = is_validated[1]
		print ("^^ERRORS^^", errors)
		for error in errors:
			messages.error(request, error)
		return redirect('/')

def login(request):
	print request.POST
	result= User.objects.login(request.POST)
	if result[0] == False:
		messages.error(request, result[1])
		return redirect('/')
	else:
		request.session['first_name']=result[2]
		messages.success(request, result[1])
		return redirect('/success')


	return redirect('/')

def success(request):
	
	return render(request, "belt3_app/success.html")

def quote(request):
	 return render(request, "belt3_app/quote.html")

def logout(request):
	request.session.clear()

	messages.success(request, "You logged out.  Enjoy your day!")

	return redirect('/')
