from django.urls import path,include    
from . import views


app_name = 'login_signup'

urlpatterns = [
    path('login/',views.login_signup,name='login_signup'),
    path('registration/',views.registration,name='registration'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('profile/addresses/',views.fetchAddresses,name='addresses'),
    path('profile/your_orders/',views.yourOrders,name='yourOrders'),
    path('profile/your_orders/selected_order/<int:order_id>',views.selectedOrder,name='selectedOrder'),
    path('profile/login_security/',views.loginSecurity,name='loginSecurity'),
    path('profile/login_security/change_password/',views.changePassword,name='changePassword'),
    #password reset
    
    # path('profile/addresses/delete_address/',views.deleteAddress,name='deleteAddress'),

    
]