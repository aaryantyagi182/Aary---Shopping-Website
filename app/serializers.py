from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ('user','name','phone','email','locality','city','zipcode','state')

''''
class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ( 'title', 'selling_price', 'discounted_price', 'description','brand','category','product_image')
'''