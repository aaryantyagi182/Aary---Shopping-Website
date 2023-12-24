from django.contrib import admin
from .models import (Customer, Product, OrderPlaced, Cart, Coupon, Payment, Discount)
# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'name', 'phone', 'email','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'customer','product','quantity','ordered_date','status']

@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'cart', 'code','MinCartValue','ValidFrom','ValidTo','CouponCount']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
	list_display = ['id','coupon','PaymentGateway','PaymentMethod']

@admin.register(Discount)
class DiscountModelAdmin(admin.ModelAdmin):
	list_display = ['id','coupon','DiscountType','MinCartValue','MaxCartValue','DiscountValue']


