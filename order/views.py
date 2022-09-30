from django.shortcuts import render,redirect,HttpResponse
from userinfo.models import User_address
from shop.models import Product
from cart.models import Cart, CartItem
from cart import views
from .models import Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum


from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.template import Context
from django.template.loader import render_to_string
from django.http import JsonResponse



MERCHANT_KEY = ''; #PAYTM MERCHANT KEY
# Create your views here.
@login_required(login_url='login_signup:login_signup')
def selectAddress(request):
	userId = request.user.id
	if request.method=='GET':
		address = User_address.objects.all().filter(user_id = userId) # all address
		return render(request, 'select_address.html',{'addresses':address,'type':1})#type 1 for cart
	else:
		product_id = request.POST['product_id']
		quantity = request.POST['quantity']
		address = User_address.objects.all().filter(user_id = userId)
		return render(request, 'select_address.html',{'addresses':address,'product_id':product_id,'quantity':quantity,'type':0}) #type 0 for product

@login_required(login_url='login_signup:login_signup')
def saveAddressAndDeliver(request,total = 0):
    current_user_id = request.user.id
    if request.method=='POST':
        full_name = request.POST['full_name']
        mobile_number = request.POST['mobile_number']
        pincode = request.POST['pin_code']
        streetAddress = request.POST['streetAddress']
        landmark = request.POST['landmark']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']

        user_address = User_address.objects.create(
			fullName=full_name,
			mobileNumber=mobile_number,
			pincode=pincode,
			streetAddress=streetAddress,
			landmark=landmark,
			city=city,
			state=state,
			country=country,
			user_id=current_user_id)
        user_address.save()
        t = int(request.POST['type'])
        print("-------------------------------------",type(t))
        if t == 1:
            address = user_address # added address
            cart = Cart.objects.get(cart_id=views._cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
            delivery_charge=40
            grand_total=total+delivery_charge
            return render(request, 'shipping_details.html',{'address':address, 'products':cart_items, 'total':total,'delivery_charge':delivery_charge,'grand_total':grand_total,'cart':cart,'type':1})
        else:
            # print("---------------------------------Product")
            product_id = request.POST['product_id']
            product_quantity = int(request.POST['quantity'])
            address = user_address #added address
            products = Product.objects.all().filter(id=product_id)
            # print(products)
            for product in products:
                total += (product.price * product_quantity)
            delivery_charge = 40
            grand_total = total+delivery_charge
            return render(request, 'shipping_details.html',{'address':address,'products':products, 'quantity':product_quantity, 'total':total, 'delivery_charge':delivery_charge,'grand_total':grand_total,'product_id':product_id,'type':0})




def shippingDetails(request,total=0):
	if request.method=='POST':
		t = int(request.POST['type'])
		# print("-------------------------------------",type(t))
		if t == 1:
			address_id = request.POST['address_id']
			address = User_address.objects.get(id = address_id) # first address
			cart = Cart.objects.get(cart_id=views._cart_id(request))
			cart_items = CartItem.objects.filter(cart=cart, active=True)
			for cart_item in cart_items:
				total += (cart_item.product.price * cart_item.quantity)
			delivery_charge=40
			grand_total=total+delivery_charge
			return render(request, 'shipping_details.html',{'address':address, 'products':cart_items, 'total':total,'delivery_charge':delivery_charge,'grand_total':grand_total,'cart':cart,'type':1})
		else:
			address_id = request.POST['address_id']
			# print("---------------------------------Product")
			product_id = request.POST['product_id']
			product_quantity = int(request.POST['quantity'])
			address = User_address.objects.get(id = address_id)
			products = Product.objects.all().filter(id=product_id)
			# print(products)
			for product in products:
				total += (product.price * product_quantity)
			delivery_charge = 40
			grand_total = total+delivery_charge
			# print("-------------------ppppppppp")
			return render(request, 'shipping_details.html',{'address':address,'products':products, 'quantity':product_quantity, 'total':total, 'delivery_charge':delivery_charge,'grand_total':grand_total,'product_id':product_id,'type':0})
def orderPlace(request):
	if request.method == 'POST':
		t = int(request.POST['type'])
		if t == 1: # order by card
			cart_id  = request.POST['cart_id']
			cart = Cart.objects.get(cart_id=views._cart_id(request))
			cart_items = CartItem.objects.filter(cart=cart_id, active=True)
		else: # order by any individual product
			product_id = request.POST['product_id']
			products = Product.objects.all().filter(id=product_id)
			quantity = int(request.POST['quantity'])
		address_id = request.POST['address_id']
		total = request.POST['total']
		delivery_charge = request.POST['delivery_charge']
		grand_total = request.POST['grand_total']
		payment_method = request.POST['payment_method']
		is_cod = True
		if payment_method == "cod":
			is_cod = True
		else:
			is_cod = False

		address = User_address.objects.get(id = address_id)
		fullName = address.fullName
		mobileNumber = address.mobileNumber
		pincode = address.pincode
		streetAddress = address.streetAddress
		landmark = address.landmark
		city = address.city
		state = address.state
		country = address.country
		
		

		# print("email id is ",request.user.email)
		try:
			order_object = Order.objects.create(
				total = total,
				deliveryCharge = delivery_charge,
				emailAddress = request.user.email,
				shippingFullName = fullName,
				shippingMobileNumber = mobileNumber,
				shippingPinCode = pincode,
				shippingStreetAddress = streetAddress,
				shippinglandmark = landmark,
				shippingCity = city,
				shippingState = state,
				shippingCountry = country,
				cod = is_cod
			)
			# print("test order-----------------------")
			order_object.save()
			
			if t==1:
				for cart_item in cart_items:
					order_item = OrderItem.objects.create(
						product = cart_item.product,
						quantity = cart_item.quantity,
						price = cart_item.product.price,
						order = order_object
					)
					order_item.save()
					# reduce quanties
					products = Product.objects.get(id=cart_item.product.id)
					products.stock = int(cart_item.product.stock - cart_item.quantity)
					products.save()
					# cart_item.delete()
				print("The order has been created")
				# order_confirm_mail(order_object.emailAddress,address,request.user.first_name,cart_items,total,delivery_charge, grand_total,t,cart_item.quantity)
			else:
				for product in products:
					order_item = OrderItem.objects.create(
						product = product,
						quantity = quantity,
						price = product.price,
						order = order_object
					)
					order_item.save()

					# reduce quanties
					product.stock = int(product.stock - quantity)
					product.save()
				print("The order has been created with product")

			if payment_method == "cod":
				try:
					order_object.order_successful = True
					order_object.save()
				except Exception as e:
					print("exception in order confirm with COD",e)
				else:
					print("cod Successful")

					order_details_for_mail = Order.objects.get(id = order_object.id)
					print("allllllll orders==========",order_details_for_mail)
					order_address_for_mail = {

						"fullName" : order_details_for_mail.shippingFullName,
						"streetAddress" : order_details_for_mail.shippingStreetAddress,
						"landmark" : order_details_for_mail.shippinglandmark,
						"city" : order_details_for_mail.shippingCity,
						"state" : order_details_for_mail.shippingState,
						"pincode" : order_details_for_mail.shippingPinCode,
						"country" : order_details_for_mail.shippingCountry,
						"mobileNumber" : order_details_for_mail.shippingMobileNumber
						}
					products_for_mail = OrderItem.objects.all().filter(order_id = order_details_for_mail.id)
					print("products for mail",products_for_mail[0].product)
					print("order details for mail", order_details_for_mail.total)
					print(order_address_for_mail)

					order_confirm_mail(
						order_details_for_mail.emailAddress,
						order_address_for_mail,
						request.user.first_name,
						products_for_mail,
						order_details_for_mail.total,
						order_details_for_mail.deliveryCharge,
						order_details_for_mail.total + order_details_for_mail.deliveryCharge
						)
					messages.success(request, 'Your order has been placed!')
					return render(request,'order_success.html')
				finally:
					pass
			
		
			else:
			# return render(request,'order_success.html')
			#request paytm to transfer the amoount to your account after payment by user


				param_dict = {

					'MID': '', #PAYTM MERCHANT ID
					'ORDER_ID': str(order_object.id),
					'TXN_AMOUNT': str(grand_total),
					'CUST_ID': str(order_object.emailAddress),
					'INDUSTRY_TYPE_ID': 'Retail',
					'WEBSITE': 'WEBSTAGING',
					'CHANNEL_ID': 'WEB',
					'CALLBACK_URL': 'http://localhost:8000/tbd/usr/order/payment/upi/handlerequest/',


				}
				param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
				return render(request,'paytm.html',{'param_dict':param_dict})
			
		except Exception as e:
			print("error in place order",e)
			return render('.')
		else:
			pass


def shippingAddress(request):
	userId = request.user.id
	print("user id is ___________________",userId)
	addresses = User_address.objects.all().filter(user_id = userId)
	print("====================All addresses are =========",addresses)
	return 	render(request,'addresses.html',{'addresses':addresses})


def order_confirm_mail(receiver_email,address,first_name, products,total,delivery_charge,grand_total):
    print("mail test----------------------")
    merge_data = {
		'user_name': first_name,
		'address': address,
		'products':products,
		'total':total,
		'delivery_charge':delivery_charge,
		'grand_total':grand_total,
		}
    print("total is",total)
    
    plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
    subject = 'Your thebookdepot.in order.'
    email_from = settings.EMAIL_HOST_USER
    
    text_body = render_to_string("message_body.txt", merge_data)
    html_body = render_to_string("emailTemplate.html", merge_data)
    
    msg = EmailMultiAlternatives(subject, text_body, email_from,[receiver_email],)
    msg.attach_alternative(html_body, "text/html")
    
    
    msg.send()
    # print("-------------------test")
    # print("-----------------------email sent----------------------------")

def emailTemplate(request):
	print("hit the emailTemplate method")
	cart = Cart.objects.get(cart_id=views._cart_id(request))
	cart_items = CartItem.objects.filter(cart=cart, active=True)
	# print(cart_items)
	return render(request,'emailTemplate.html',{'cart_items':cart_items})


def addAddress(request):
    current_user_id = request.user.id
    if request.method=='POST':
        full_name = request.POST['full_name']
        mobile_number = request.POST['mobile_number']
        pincode = request.POST['pin_code']
        streetAddress = request.POST['streetAddress']
        landmark = request.POST['landmark']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country'] 
        if current_user_id is not None:
            user_address = User_address.objects.create(fullName=full_name,mobileNumber=mobile_number,pincode=pincode,streetAddress=streetAddress,landmark=landmark,city=city,state=state,country=country,user_id=current_user_id)
            user_address.save()
            print("----------------address saved")
            return redirect('login_signup:addresses')
        else:
            messages.info(request,'Please Login first')
            return redirect('order:addAddress')
    else:
        return render(request,'addAddress.html')


@login_required()
def orderHistory(request):
	if request.user.is_authenticated:
		email = str(request.user.email)
		order_details = Order.objects.filter(emailAddress=email)
	return render(request,'order/orders_list.html',{'order_details':order_details})

@login_required()
def viewOrder(request, order_id):
	if request.user.is_authenticated:
		email = str(request.user.email)
		order = Order.objects.get(id=order_id, emailAddress=email)
		order_items = OrderItem.objects.filter(order=order)
	return render(request,'order/order_details.html',{'order':order,'order_items':order_items})

@login_required()
def cancelOrder(request, order_id):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_object = Order.objects.get(id=order_id)
        order_object.canceled = 1
        order_object.canceledDate = datetime.now()
        order_object.save()
    return redirect('order:order_history')

@csrf_exempt
def handlerequest(request):
	#paytm will send you post request here.
	print(request.user.id)
	form = request.POST
	response_dict = {}
	print("---------from ",form)
	for i in form.keys():
		print('----',i,'-----',form[i])
		response_dict[i] = form[i]
		if i == 'CHECKSUMHASH':
			checksum = form[i]

	varify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
	if varify:
		if response_dict['RESPCODE'] == '01':

			order_id = response_dict['ORDERID']
			order_object = Order.objects.get(id=order_id)
			try:
				order_object.order_successful = True
				order_object.txn_id = response_dict['TXNID']
				order_object.txn_date = response_dict['TXNDATE']
				order_object.txn_amount = response_dict['TXNAMOUNT']
				order_object.save()
				
			except Exception as e:
				print("error in prepaid order------------=",e)
			else:
				print("Order pre paid Successful")
				order_details_for_mail = order_object
				print("allllllll orders==========",order_details_for_mail)
				order_address_for_mail = {

					"fullName" : order_details_for_mail.shippingFullName,
					"streetAddress" : order_details_for_mail.shippingStreetAddress,
					"landmark" : order_details_for_mail.shippinglandmark,
					"city" : order_details_for_mail.shippingCity,
					"state" : order_details_for_mail.shippingState,
					"pincode" : order_details_for_mail.shippingPinCode,
					"country" : order_details_for_mail.shippingCountry,
					"mobileNumber" : order_details_for_mail.shippingMobileNumber
					}
				products_for_mail = OrderItem.objects.all().filter(order_id = order_id)
				print(order_details_for_mail)
				print(order_address_for_mail)
				
				

				order_confirm_mail(
					order_details_for_mail.emailAddress,
					order_address_for_mail,
					"	User",
					#request.user.first_name,
					products_for_mail,
					order_details_for_mail.total,
					order_details_for_mail.deliveryCharge,
					order_details_for_mail.total + order_details_for_mail.deliveryCharge
					)
				messages.success(request, 'Your order has been placed!')
				return render(request,'order_success.html')
			finally:
				pass
			
		else:
			messages.success(request, 'Your order has been failed!')
			print("order was not successful because "+ response_dict['RESPMSG'])

	return render(request,'order_failed.html',{'response':response_dict})
	pass

