from django.urls import path
from . import views

app_name='adminrole'

urlpatterns = [
	path('adminrole_dashboard/',views.management, name='management'),
	path('view_order/<int:order_id>/',views.view_order_adminrole, name='view_order_adminrole'),
	path('order_delivered/<int:order_id>/',views.order_delivered, name='order_delivered'),
]