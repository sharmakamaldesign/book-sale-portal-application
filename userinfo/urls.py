from django.urls import path
from . import views

app_name = 'userinfo'

urlpatterns = [
    path('add_address/',views.addAddress,name='addAddress'),
    path('add_address/test/',views.test,name='test'),  #just for test , no use in porduction
    path('delete_address/',views.deleteAddress,name='deleteAddress'),
    
]