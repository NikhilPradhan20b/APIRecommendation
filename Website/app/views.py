from http.client import HTTPResponse
from urllib import request
from urllib.parse import urljoin
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .models import customer,productDetail,cart,orderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm, CommentForm, Comment
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import requests
import json
from app.recommended import get_recommendation


class ProductView(View):
    def get(self,request):
        # recommendation = get_recommendation(self,request)
        # print(recommendation)
        # products = []
        # for i in range(len(recommendation)):
        #     products.append(productDetail.objects.filter(title = recommendation[i]))
        # for i in range(len(recommendation)):
        #    new = products[i]
        #    for a in new:
        #       print(a.title)
        #       print(a.price)
        #       print(a.description)
        Boots = productDetail.objects.filter(category='b')
        Heels = productDetail.objects.filter(category='h')
        Sneakers = productDetail.objects.filter(category='s')
        return render(request, 'app/home.html', {'Boots':Boots, 'Heels':Heels, 'Sneakers':Sneakers})
class Recommended(View):
    def get(self,request):
        recommendation = get_recommendation(self,request)
        print(recommendation)
        products = []
        for i in range(len(recommendation)):
            products.append(productDetail.objects.filter(title = recommendation[i]))
        for i in range(len(recommendation)):
           new = products[i]
           for a in new:
              print(a.title)
            #   print(a.price)
            #   print(a.description)
        return render(request, 'app/recommended.html',{'new':products})


class ProductDetailView(View):
    def get(self,request,pk):
        product = productDetail.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',{'product':product})

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = productDetail.objects.get(id=product_id)
 cart(user=user,product=product).save()
 return redirect('/cart')

# def recommended(user,request):
# #    url_1 = 'http://127.0.0.1:8000/popularity'
# #    url_2 = 'http://127.0.0.1:8000/user-recommendation'
# #    user = request.user
# #    if request.user.is_authenticated:
# #         commentData = Comment.objects.filter(user=user)
# #         details_arr = []
# #         for a in commentData:
# #             new_dict={'productId': a.product.title,'userId':'A061','Rating':a.rating}
# #             details_arr.append(new_dict)
# #             #print(details_arr)
# #         no_of_products = len(details_arr)
# #         #print(no_of_products)
# #         if no_of_products>4:
# #             user_rating_data = json.dumps(details_arr)
# #             response1 = requests.post(url_2,data = user_rating_data)
# #             user_recommendation = response1.json()
# #             print(user_recommendation)
# #         else:
# #             response = requests.get(url_1)
# #             popular_recommendation = response.json()
# #             print(popular_recommendation)
# #    else:
# #         response = requests.get(url_1)
# #         popular_recommendation = response.json()
# #         print(popular_recommendation)
#    return redirect('/recommended')
            

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        Cart = cart.objects.filter(user=user)
        # print(Cart)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.00
        cart_product = [p for p in cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
             temp_amount = (p.quantity * p.product.price)   
             amount += temp_amount
             totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':Cart , 'totalamount': totalamount, 'amount':amount})
        else:
         return render(request, 'app/emptycart.html')
      

def plus_cart(request):    
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
              temp_amount = (p.quantity * p.product.price)   
              amount += temp_amount
            data = {
                 'quantity': c.quantity,
                 'amount': amount,
                 'totalamount': amount + shipping_amount 
                }
            return JsonResponse(data)
def minus_cart(request):    
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
              temp_amount = (p.quantity * p.product.price)   
              amount += temp_amount
            data = {
                 'quantity': c.quantity,
                 'amount': amount,
                 'totalamount': amount + shipping_amount 
                }
            return JsonResponse(data)
def remove_cart(request):    
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.price)   
            amount += temp_amount
        data = {   
            'amount': amount,
            'totalamount': amount + shipping_amount 
            }
        return JsonResponse(data)
def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 add = customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required()
def orders(request):
    op = orderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def Boots(request, data=None):
 if data == None:
  Boots = productDetail.objects.filter(category='b')
 return render(request, 'app/Boots.html',{'Boots':Boots})

def Sneakers(request, data=None):
 if data == None:
  Sneakers = productDetail.objects.filter(category='s')
 return render(request, 'app/Sneakers.html',{'Sneakers':Sneakers})

def Heels(request, data=None):
 if data == None:
  Heels = productDetail.objects.filter(category='h')
 return render(request, 'app/Heels.html',{'Heels':Heels})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Successfully registered ')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})
@login_required
def checkout(request):
    user = request.user
    add = customer.objects.filter(user=user)
    cart_items = cart.objects.filter(user=user)
    amount = 0.0
    shipping_samount = 70.0
    totalamount = 0.0
    cart_product = [p for p in cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.price)   
            amount += temp_amount
        totalamount= amount + shipping_samount
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount,'cart_items':cart_items})

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    Customer = customer.objects.get(id=custid)
    Cart = cart.objects.filter(user=user)
    for c in Cart:
        orderPlaced(user=user , customer=Customer, product=c.product,quantity=c.quantity ).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})

    def post(self, request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
        usr = request.user
        name= form.cleaned_data['name']
        address= form.cleaned_data['address']
        reg = customer(user=usr, name=name, address=address) 
        reg.save()
        messages.success(request,'Profile Updated Successfully')
      return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})

def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment= form.cleaned_data['comment']
            data.rating = form.cleaned_data['rating']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product = productDetail.objects.get(id=id)
            current_user = request.user
            data.user = current_user
            data.save()
            messages.success(request, "Your review has been sent. Thank you for your request.")
            return HttpResponseRedirect(url)
        else:
            print(form.errors)
    return HttpResponseRedirect(url)