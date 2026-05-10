from django.contrib import admin
from myapp.models import*
from django.utils.html import mark_safe,format_html

# Register your models here.
@admin.register(CustomeUser)
class customeuser(admin.ModelAdmin):
    list_display=('username','first_name','last_name','email','u_mobile')
admin.site.register(Categories)
admin.site.register(Flavour)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','p_name','category','flavour','p_name','p_weight','p_price','p_desc','image_pre')
    search_fields=('p_name',
                   'category__category_name',
                   'flavour__flavour_name',
                   'p_name',
                   'p_weight',
                   'p_price')
    @admin.display(description='Image')
    def image_pre(self,obj):
        if obj.p_img:
            return format_html('<img src="{}" width="50px" height="50px";/>',obj.p_img.url)
        return 'No Image Found'
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','u_id','o_date','total_amount','o_status')

@admin.register(Order_details)
class Order_detailsAdmin(admin.ModelAdmin):
    list_display=('o_id','product_id','quantity')

@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list_display=('u_id','o_id','payment_type','transition_id','payment_date','payment_status','payment_amount')
    search_fields=('u_id','o_id','payment_type','transition_id','payment_date','payment_status','payment_amount')

@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    list_display=('u_id','product_id','feedback_date','feedback_details','feedback_star')
    search_fields=('u_id__username','product_id__p_name','feedback_date')
    
    
@admin.register(Gallery)
class Gallery(admin.ModelAdmin):
    list_display=('product_id','image_pre1','image_pre2','image_pre3')
    def image_pre1(self,obj):
        if obj.img_p1:
            return mark_safe(f'<img src="{obj.img_p1.url}" width="50px" height="50px">')
        return 'No Image Found'
    def image_pre2(self,obj):
        if obj.img_p2:
            return mark_safe(f'<img src="{obj.img_p2.url}" width="50px" height="50px">')
        return 'No Image Found'
    def image_pre3(self,obj):
        if obj.img_p3:
            return mark_safe(f'<img src="{obj.img_p3.url}" width="50px" height="50px">')
        return 'No Image Found'

@admin.register(Cart)
class register(admin.ModelAdmin):
    list_display=('user','created_at')

@admin.register(Cartitem)
class cartitem(admin.ModelAdmin):
    list_display=('cart','product','quantity')