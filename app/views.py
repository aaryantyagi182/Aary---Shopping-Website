from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, Product, OrderPlaced, Customer, Coupon, Discount, Payment
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerProfileForm, CouponApplyForm
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from .serializers import CustomerSerializer


class ProductView(View):
	def get(self, request):
		topwears = Product.objects.filter(category='TW')
		bottomwears = Product.objects.filter(category='BW')
		mobiles = Product.objects.filter(category='M')
		return render(request,'app/home.html',
		{'topwears': topwears, 'bottomwears': bottomwears,
		  'mobiles':mobiles
		})


class ProductDetailView(View):
	def get(self,request, pk):
		product = Product.objects.get(pk=pk)
		return render(request,'app/productdetail.html',{'product':product})

def add_to_cart(request):
	user = request.user
	product_id = request.GET.get('prod_id')
	product = Product.objects.get(id=product_id)
	Cart(user=user,product=product).save()
	return redirect('/cart')

def show_cart(request):
	if request.user.is_authenticated:
		user=request.user
		cart=Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount=70.0
		total_amount=0.0
		cart_product=[p for p in Cart.objects.all() if p.user==user]
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity*p.product.discounted_price)
				amount+=tempamount
			total_amount=amount+shipping_amount
		return render(request,'app/addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})



def plus_cart(request):
	if request.method=='GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount=0.0
		shipping_amount=70.0
		total_amount=0.0
		cart_product=[p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity*p.product.discounted_price)
			amount+=tempamount
		total_amount=amount+shipping_amount
		data={
			'quantity':c.quantity,
			'amount':amount,
			'totalamount': total_amount
		}
		return JsonResponse(data)

def minus_cart(request):
	if request.method=='GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount=0.0
		shipping_amount=70.0
		total_amount=0.0
		cart_product=[p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity*p.product.discounted_price)
			amount+=tempamount
		total_amount=amount+shipping_amount
		data={
			'quantity':c.quantity,
			'amount':amount,
			'totalamount': total_amount
		}
		return JsonResponse(data)

def remove_cart(request):
	if request.method=='GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount=0.0
		shipping_amount=70.0
		total_amount=0.0
		cart_product=[p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity*p.product.discounted_price)
			amount+=tempamount
		total_amount=amount+shipping_amount
		data={
			'amount':amount,
			'totalamount': total_amount
		}
		return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')


def address(request):
	add = Customer.objects.filter(user=request.user)
	return render(request, 'app/address.html', {'add':add})

def orders(request):
 return render(request, 'app/orders.html')


def mobile(request, data=None):
	if data == None:
		mobiles = Product.objects.filter(category='M')
	elif data=='below':
		mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt=10000)
	elif data=='above':
		mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gt=10000)
	else:
		mobiles = Product.objects.filter(category='M').filter(brand=data)

	return render(request, 'app/mobile.html',{'mobiles': mobiles})




class CustomerRegistrationView(View):
	def get(self,request):
		form = CustomerRegistrationForm()
		return render(request,'app/customerregistration.html', {'form':form})
	def post(self,request):
		form = CustomerRegistrationForm(request.POST)
		if form.is_valid():
			messages.success(request, 'Successfully Registered')
			form.save()
		return render(request,'app/customerregistration.html', {'form':form})

class CustomerView(viewsets.ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer

'''
class ProductView(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
'''
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=user)
	request.session['coupon_id']=None
	finalamount=0.0
	amount = 0.0
	shipping_amount=70.0
	total_amount=0.0
	cart_product=[p for p in Cart.objects.all() if p.user==user]
	form = CouponApplyForm()
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity*p.product.discounted_price)
			amount+=tempamount
		total_amount=amount+shipping_amount
	return render(request, 'app/checkout.html',{'add':add, 'totalamount': total_amount, 'cart_items': cart_items, 'form':form, 'finalamount':finalamount})

def payment_done(request):
	user = request.user
	custid = request.GET('custid')
	customer = Customer.objects.get(id=custid)
	cart = Cart.objects.filter(user=user)
	for c in cart:
		OrderPlaced(user=user,customer=customer, product = c.product, quantity = c.quantity)
		c.delete()
	return redirect("orders")


class ProfileView(View):
	def get(self, request):
		form = CustomerProfileForm()
		return render(request,'app/profile.html',{'form':form, 'active': 'btn-primary'})
	def post(self,request):
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr=request.user
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, email=email, phone=phone, locality=locality,city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request,"Congratulations, Profile Updated Successfully")
			return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
	

def coupon_apply(request):
	now = timezone.now()
	form = CouponApplyForm(request.POST)
	user = request.user
	add = Customer.objects.filter(user=user)
	amount = 0.0
	shipping_amount=70.0
	total_amount=0.0
	cart_product=[p for p in Cart.objects.all() if p.user==user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity*p.product.discounted_price)
			amount+=tempamount
		total_amount=amount+shipping_amount
	if form.is_valid():
		code = form.cleaned_data['code']
		try:
			coupon = Coupon.objects.get(code__iexact=code,
			                            ValidFrom__lte=now,
						    ValidTo__gte=now,
						    CouponCount__gte = 1,
						    MinCartValue__lte = total_amount)
			request.session['coupon_id']=coupon.id
			finalamount = total_amount
			dis= [p for p in Discount.objects.all() if p.coupon==coupon]
			if dis:
				for p in dis:
					m=p.DiscountType
					if m == "F" and (finalamount>=p.MinCartValue and finalamount<=p.MaxCartValue):
						finalamount = finalamount - p.DiscountValue
					elif(finalamount>=p.MinCartValue and finalamount<=p.MaxCartValue):
						value = (finalamount)*p.DiscountValue
						value = value//100
						finalamount = finalamount - value
				if(finalamount<total_amount):
					coupon.CouponCount-=1
					coupon.save()
					messages.success(request,"Coupon Applied")
					return render(request, 'app/checkout.html',{'add':add, 'totalamount': total_amount, 'cart_items': cart_product, 'form':form, 'finalamount':finalamount})	
				else:
					request.session['coupon_id']=None
					messages.info(request,"Coupon Not Applicable")
					return redirect('checkout')
			else:
				request.session['coupon_id']=None
				messages.info(request,"Coupon Not Applicable")
				return redirect('checkout')
		except Coupon.DoesNotExist:
			request.session['coupon_id']=None
			messages.info(request, "Incorrect Coupon Code")
			return redirect('checkout')
	return redirect('checkout')
			