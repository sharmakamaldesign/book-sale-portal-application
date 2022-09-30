from django.urls import path
from . import views

app_name='search_app'

urlpatterns = [
	path('srch/',views.searchResult, name='searchResult'), 
	path('test/',views.test,name="testtest")
]