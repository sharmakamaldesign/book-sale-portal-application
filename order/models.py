from django.db import models
from shop.models import Product

# Create your models here.
class Order(models.Model):
	tocken = models.CharField(max_length=250, blank=True)
	total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='GBP Order Total')
	deliveryCharge = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
	emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
	created = models.DateTimeField(auto_now_add=True)
	billingName = models.CharField(max_length=250,blank=True)
	billingAddress1 = models.CharField(max_length=250,blank=True)
	billingCity = models.CharField(max_length=250,blank=True)
	billingPostcode = models.CharField(max_length=10,blank=True)
	billingCountry = models.CharField(max_length=200,blank=True)
	shippingFullName = models.CharField(max_length=250,blank=True)
	shippingMobileNumber = models.CharField(max_length=15,blank=True)
	shippingPinCode = models.CharField(max_length=10,blank=True)
	shippingStreetAddress = models.CharField(max_length=250,blank=True)
	shippinglandmark = models.CharField(max_length=250,blank=True)
	shippingCity = models.CharField(max_length=250,blank=True)
	shippingState = models.CharField(max_length=250,blank=True)
	shippingCountry = models.CharField(max_length=200,blank=True)
	delivered = models.BooleanField(default=False)
	deliveredDate = models.DateTimeField(blank=True, null=True)
	canceled = models.BooleanField(default=False)
	canceledDate = models.DateTimeField(blank=True, null=True)
	cod = models.BooleanField(default=True)
	order_successful = models.BooleanField(default=False)
	dispatched = models.BooleanField(default=False)
	txn_id = models.CharField(max_length=250,blank=True)
	txn_date = models.DateTimeField(blank=True, null=True)
	txn_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)

	class Meta:
		db_table = 'Order'
		ordering = ['-created']
	
	def total_paid(self):
		return self.total + self.deliveryCharge

	def __str__(self):
		return str(self.id)

class OrderItem(models.Model):
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	# product = models.CharField(max_length=250)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=10,decimal_places=2, verbose_name='GBP Price')
	order = models.ForeignKey(Order,on_delete=models.CASCADE)

	class Meta:
		db_table = 'OrderItem'

	def sub_total(self):
		return self.quantity * self.price

	def __str__(self):
		return self.product
