from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Product
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage\

# Create your views here.
def searchResult(request):
	products = None
	query = None
	if 'q' in request.GET:
		query = request.GET.get('q')
		products = Product.objects.all().filter(Q(name__icontains=query) | Q(description__icontains=query))
	return render(request,'search.html',{'query':query, 'products':products})

def test(request):
	return HttpResponse("helloworld")

