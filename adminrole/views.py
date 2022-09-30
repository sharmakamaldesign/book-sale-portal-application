from django.shortcuts import render, redirect
from order.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
@login_required()
def management(request):
	allOrders = Order.objects.all();
	print(allOrders)

	return render(request,'adminrole.html',{'all_orders':allOrders})

@login_required()
def view_order_adminrole(request, order_id):
	pass
	if request.user.is_authenticated:
		order = Order.objects.get(id=order_id)
		order_items = OrderItem.objects.filter(order=order)
	return render(request,'order_details_adminrole.html',{'order':order,'order_items':order_items})


@login_required()
def order_delivered(request, order_id):
	pass
	if request.user.is_authenticated:
		order = Order.objects.get(id=order_id)
		order.delivered = 1
		order.delivered_date = datetime.now()
		order.save()
	return redirect('adminrole:management')