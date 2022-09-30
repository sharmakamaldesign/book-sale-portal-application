from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.allProdCat,name='allProdCat'),
    path('<slug:c_slug>/',views.allProdCat,name='products_by_category'),
    path('<slug:c_slug>/<slug:s_c_slug>/',views.allProdSubCat,name='products_by_sub_category'),
    path('<slug:c_slug>/<slug:s_c_slug>/<slug:product_slug>/',views.ProdCatDetail, name='ProdCatDetail'),
    # path('ts/ts/ts/',views.t, name='ts'),
]