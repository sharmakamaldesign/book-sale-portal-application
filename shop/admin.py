from django.contrib import admin
from .models import Category,Product,Sub_category

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name','slug',]
	prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)

class Sub_categoryAdmin(admin.ModelAdmin):
	list_display = ['name','slug','category']
	prepopulated_fields = {'slug':('name',)}
admin.site.register(Sub_category, Sub_categoryAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ['name','category','sub_category','mrp','discount','price','stock','available','created','updated']
	list_editable = ['mrp','discount','category','sub_category','stock','available']
	prepopulated_fields = {'slug':('name',)}
	list_per_page = 20
admin.site.register(Product,ProductAdmin)