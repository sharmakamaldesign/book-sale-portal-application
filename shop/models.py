from django.db import models 
from django.urls import reverse

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length= 250, unique=True)
	slug = models.SlugField(max_length=250, unique=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='category', blank=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
	 	return '{}'.format(self.name)

	def get_url(self):
		return reverse('shop:products_by_category',args=[self.slug])

class Sub_category(models.Model):
	name = models.CharField(max_length= 250, unique=True)
	slug = models.SlugField(max_length=250, unique=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'sub_category'
		verbose_name_plural = 'sub_categories'

	def __str__(self):
	 	return '{}'.format(self.name)

	def get_url(self):
		return reverse('shop:products_by_sub_category',args=[self.category.slug,self.slug])


class Product (models.Model):
	name = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=250, unique=True)
	description = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
	mrp = models.DecimalField(max_digits=10, decimal_places=2)
	discount = models.DecimalField(max_digits=10, decimal_places=2)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='product', blank=True)
	stock = models.IntegerField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)
	publisher = models.CharField(max_length=250, blank=True, null=True)
	language = models.CharField(max_length=50, blank=True, null=True)
	isbn_10 = models.CharField(max_length=50, blank=True, null=True)
	isbn_13 = models.CharField(max_length=50, blank=True, null=True)
	pages = models.IntegerField(null=True, blank=True)
	length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	def save(self, *args, **kwargs): 
		self.price = self.mrp - (self.mrp * self.discount / 100)
		super(Product, self).save(*args, **kwargs)
        

	class Meta:
		ordering = ('name',)
		verbose_name = 'product'
		verbose_name_plural = 'products'

	def get_url(self):
		return reverse('shop:ProdCatDetail',args=[self.category.slug, self.sub_category.slug, self.slug])
	

	def __str__(self):
		return '{}'.format(self.name)