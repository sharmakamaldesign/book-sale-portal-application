from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Category, Product,Sub_category
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
from .forms import SignUpForm


# Create your views here.
def index(request):
	text_var = "This is my first django app web page."
	return HttpResponse(text_var)

#Category view

def allProdCat(request, c_slug=None):
	c_page = None
	products_list = None
	if c_slug != None:
		c_page = get_object_or_404(Category, slug=c_slug)
		products_list = Product.objects.filter(category=c_page,available=True)
	else:
		products_list = Product.objects.all().filter(available=True)

	'''Paginator code'''
	paginator = Paginator(products_list,6)
	try:
		page = int(request.GET.get('page','1'))
	except:
		page = 1
	try:
		products = paginator.page(page)
	except(EmptyPage,InvalidPage):
		products = paginator.page(paginator.num_pages)

	return render(request, 'shop/category.html',{'category':c_page,'products':products})


def allProdSubCat(request,c_slug=None, s_c_slug=None):
	c_page = None
	s_c_page = None
	products_list = None
	if c_slug != None:
		c_page = get_object_or_404(Category, slug=c_slug)
		s_c_page = get_object_or_404(Sub_category, slug=s_c_slug)
		products_list = Product.objects.filter(sub_category=s_c_page,available=True)
	else:
		products_list = Product.objects.all().filter(available=True)
	'''Paginator code'''
	paginator = Paginator(products_list,6)
	try:
		page = int(request.GET.get('page','1'))
	except:
		page = 1
	try:
		products = paginator.page(page)
	except(EmptyPage,InvalidPage):
		products = paginator.page(paginator.num_pages)

	return render(request, 'shop/category.html',{'category':c_page, 'sub_category':s_c_page, 'products':products})

def ProdCatDetail(request, c_slug, s_c_slug, product_slug):
	try:
		product = Product.objects.get(category__slug=c_slug, sub_category__slug=s_c_slug, slug=product_slug)
		print("--------------------------6767",)
	except Exception as e:
		raise e
	else:
		print("=========product user id is ",request.user.id)
		return render(request, 'shop/product.html',{'product':product})


def t(request):
	return HttpResponse("helloworld")

def defaultRedirect(request):
	return redirect('/')




