from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    # path('',views.order,name='order'),
    path('selectAddress/',views.selectAddress,name='selectAddress'),
    path('selectAddress/saveAddressAndDeliver',views.saveAddressAndDeliver,name='saveAddressAndDeliver'),
    path('selectAddress/addAddress',views.addAddress,name='addAddress'),
    path('selectAddress/shippingDetails/',views.shippingDetails,name='shippingDetails'),
    path('selectAddress/shippingDetails/orderPlace/',views.orderPlace,name='orderPlace'),
    path('test_email/',views.emailTemplate,name='emailTemplate'),
    path('history/',views.orderHistory,name='order_history'),
    path('<int:order_id>/',views.viewOrder,name='order_detail'),
    path('cancel/<int:order_id>/',views.cancelOrder,name='cancel_order'),
    path('payment/upi/handlerequest/', views.handlerequest, name='handlerequest'),
    
]