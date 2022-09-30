from .models import Category,Sub_category

def menu_links(request):
	obj = {}
	categories = Category.objects.all()
	for cat in categories:
		sub_categories = Sub_category.objects.filter(category = cat)
		obj[cat] = sub_categories
	return dict(categories=obj)
