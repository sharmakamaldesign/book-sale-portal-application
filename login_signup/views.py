from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from userinfo.models import User_address
from order.models import Order, OrderItem
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.template import Context
from django.template.loader import render_to_string

# Create your views here.
def login_signup(request):
	if request.method=='POST':
		username = request.POST['email']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('/')
		else:
			messages.info(request,'Invalid username or password')
			return render(request,'login_signup.html')

	else:	
		return render(request,'login_signup.html')

def registration(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['email']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		if password1 == password2 and password1 != "":
			if User.objects.filter(username=username).exists():
				print("=================email address is already registered===========")
				messages.info(request,'This E-mail is already registered.')
				return redirect('login_signup:registration')	
			else:
				user = User.objects.create_user(username = username, password=password1, email=email, first_name=first_name, last_name=last_name)
				user.save()
				print("==============================User created=====================")
			
		else:
			print("==============================password is not matching=========")
			messages.info(request,'passwrods are not matching')
			return redirect('login_signup:registration')
		return redirect('login_signup:login_signup')
	else:
		return render(request,'registration.html')


def logout(request):
	auth.logout(request)
	return redirect('/')

def profile(request):
	return render(request,'profile.html')


def fetchAddresses(request):
	userId = request.user.id
	print("user id is ___________________",userId)
	addresses = User_address.objects.all().filter(user_id = userId)
	print("====================All addresses are =========",addresses)
	return 	render(request,'addresses.html',{'addresses':addresses})
	
def yourOrders(request):
	order_objects = Order.objects.all().filter(emailAddress = request.user.email)
	# print(order_objects)
	return render(request,'your_orders.html',{'orders':order_objects})

def selectedOrder(request,order_id):
	order_items = OrderItem.objects.all().filter(order=order_id)
	print(order_items)
	return render(request,'selected_order.html',{'order_items':order_items,'order_id':order_id})



def loginSecurity(request):
	return render(request,'login_security.html')

def changePassword(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # print("-----------------------------till here here------------")
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            print("password successfully changed")
            return render(request,'password_changed.html')
        else:
            messages.error(request, 'Please enter correct values.')
            return redirect('.')
            
    else:
        form = PasswordChangeForm(request.user)
        return render(request,'change_password.html', {
        'form': form
    })