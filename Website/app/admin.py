from django.contrib import admin

from django.contrib import admin
from .models import (
    customer,
    productDetail,
    cart,
    orderPlaced,
    Comment
)
@admin.register(customer)
class customerModelAdmin(admin.ModelAdmin):
 list_display =['id','user','name','address'] 

@admin.register(productDetail)  
class productDetailModelAdmin(admin.ModelAdmin):
 list_display = ['id','title','price','description','category','product_image']

 @admin.register(cart)
 class cartModelAdmin(admin.ModelAdmin):
    list_display=['id','quantity','product','user']
@admin.register(orderPlaced)
class orderPlacedModelAdmin(admin.ModelAdmin):
   list_display=['id','quantity','ordered_date','status','customer','product','user']

@admin.register(Comment)
class commentModelAdmin(admin.ModelAdmin):
  list_display=['user','product','subject','comment','rating','create_at']