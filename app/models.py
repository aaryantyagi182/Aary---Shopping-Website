from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
STATE_CHOICES =(
	('Uttar Pradesh','Uttar Pradesh'),
	('Assam','Assam'),
	('Agra','Agra')
)

class Customer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	locality = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	zipcode = models.IntegerField()
	state = models.CharField(choices=STATE_CHOICES,max_length=50)
	def __str__(self):
		return str(self.id)

CATEGORY_CHOICES = (
	('M', 'Mobile'),
	('L', 'Laptop'),
	('TW','Top Wear'),
	('BW','Bottom Wear')
)
'''
SUBCATEGORY_CHOICES = (
	('S', 'small'),
	('M', 'medium'),
	('L','l"arge')
)'''
class Product(models.Model):
	title = models.CharField(max_length=200)
	selling_price = models.FloatField()
	discounted_price = models.FloatField()
	description = models.TextField()
	brand = models.CharField(max_length=100)
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
	product_image = models.ImageField(upload_to = 'productimg')
	def __str__(self):
		return str(self.id)

class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)

	@property
	def total_cost(self):
		return self.quantity * self.product.discounted_price

STATUS_CHOICE = (
	('Accepted','Accepted'),
	('Packed','Packed'),
	('On The Way','On The Way'),
	('Delivered','Delivered'),
	('Cancel','Cancel')
)
class OrderPlaced(models.Model):
	user = models.ForeignKey(User, on_delete= models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
	product = models.ForeignKey(Product, on_delete= models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	ordered_date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(choices=STATUS_CHOICE, max_length=20, default='Pending')
	
	def __str__(self):
		return str(self.id)


# coupon Engine Schema
class Coupon(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	code = models.CharField(max_length=50,unique=True)
	MinCartValue = models.IntegerField()
	ValidFrom = models.DateTimeField()
	ValidTo = models.DateTimeField()
	CouponCount = models.IntegerField()

	def __str__(self):
		return str(self.id)

class Payment(models.Model):
	coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE) 
	PaymentGateway = models.CharField(max_length=50)
	PaymentMethod = models.CharField(max_length=50)

	def __str__(self):
		return str(self.id)

COUPON_CHOICES =(
	('F','Flat'),
	('P','Percent') 
)
class Discount(models.Model):
	coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
	DiscountType = models.CharField(choices=COUPON_CHOICES, max_length=1)
	MinCartValue = models.IntegerField()
	MaxCartValue = models.IntegerField( null=True)
	DiscountValue = models.IntegerField()

	def __str__(self):
		return str(self.id)	

