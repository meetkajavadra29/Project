from django.shortcuts import render,redirect
from myapp.models import CustomeUser,Product,Cartitem,Cart,Flavour,Categories,Order,Order_details,Payment,Feedback,Gallery
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from cakeshope import settings
import razorpay
from datetime import date
# Create your views here.
def home(request):
    products= Product.objects.all()
    flavour=Flavour.objects.all()
    categories=Categories.objects.all()

    if request.method=="POST":
        category=request.POST.getlist('category')
        flav=request.POST.getlist('flavour')
        price_filter=request.POST.getlist('price')
        if 'Allprice' not in price_filter:
            if "400_above" in price_filter:
                products = products.filter(p_price__gte=400)
            elif "Below_400" in price_filter:
                products = products.filter(p_price__lte=400)
            elif "Below_300" in price_filter:
                products = products.filter(p_price__lte=300)
            elif "Below_200" in price_filter:
                products = products.filter(p_price__lte=200)
            

        if "Allflaver" not in flav:
           flavs=Flavour.objects.filter(flavour_name__in=flav)
           products=products.filter(flavour__in=flavs)

        if "Allcategory" not in category:
            cate=Categories.objects.filter(category_name__in=category)
            products=products.filter(category__in=cate)
        

    paginator=Paginator(products,6) 
    page_number=request.GET.get('page')
    data=paginator.get_page(page_number) 
    return render(request,'Home.html',{'product':data,'flavour':flavour,'categories':categories})   
    

def Registration(request):
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        add=request.POST.get('add')
        password=request.POST.get('pass')
        if(CustomeUser.objects.filter(username=username).exists() or CustomeUser.objects.filter(u_mobile=phone).exists() or CustomeUser.objects.filter(email=email).exists()):
            if CustomeUser.objects.filter(email=email).exists():
                messages.success(request,"Email id is already exist")
                return redirect('Registration')
            if CustomeUser.objects.filter(u_mobile=phone).exists():
                messages.success(request,"phone number is already exist")
                return redirect('Registration')
            if CustomeUser.objects.filter(username=username).exists():
                messages.success(request,"user is already exist")
                return redirect('Registration')
        user=CustomeUser.objects.create_user(username=username,email=email,password=password)
        user.first_name=fname
        user.last_name=lname
        user.u_mobile=phone
        user.u_address=add
        user.save()
        return redirect('/loginuser')
    return render(request,'Registration.html')

def loginuser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.success(request,'invalid datails')
            return redirect('loginuser')
    return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect('/loginuser')

def forgotpass(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if CustomeUser.objects.filter(username=username).exists():
            user=CustomeUser.objects.get(username=username)
            user.set_password(password)
            user.save()
            return redirect('/loginuser')
        else:
            messages.success(request,'User not found')
            return redirect('/forgotpass')
    return render(request,'Forgotpass.html')

def about(request):
    return render(request,'about.html')

def cart(request,product_id):
    if request.user.is_anonymous:
        return redirect('/loginuser')
    try:
        cart_data=Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart_data=Cart(user=request.user)
        cart_data.save()
    product_data=Product.objects.get(id=product_id)
    if Cartitem.objects.filter(cart=cart_data,product=product_id):
        cart=Cartitem.objects.get(cart=cart_data,product=product_id)
        cart.quantity+=1
        cart.save()
    else:
        prod_item=Cartitem(cart=cart_data,product=product_data)
        prod_item.save()
    
    return redirect('/')
def addtocart(request):
    error=''
    total=0
    if request.user.is_anonymous:
        return redirect('/loginuser')
    try:
        cart_data=Cart.objects.get(user=request.user)
        if Cartitem.objects.filter(cart=cart_data):
            cart_item=Cartitem.objects.filter(cart=cart_data)
            for item in cart_item:
                total+=item.product.p_price*item.quantity
            tax=(total*5)/100
            subtotal=total+tax
            return render(request,'addtocart.html',{'cart_item':cart_item,'total':total,'tax':tax,'subtotal':subtotal})
        else:
            error="Cart Item Not Found"
        # for item in cart_item:
        #     prod=item.product
        #     product.append(Product.objects.get(id=prod.id))
    except Cart.DoesNotExist:
        error='Cart Item Not Found'
    return render(request,'addtocart.html',{'error':error})

def increase(request,product_id):
        cart_data=Cart.objects.get(user=request.user)
        cart_item=Cartitem.objects.get(cart=cart_data,product=product_id)
        cart_item.quantity+=1
        cart_item.save()
        return redirect('addtocart')

def decrease(request,product_id):
        cart_data=Cart.objects.get(user=request.user)
        cart_item=Cartitem.objects.get(cart=cart_data,product=product_id)
        cart_item.quantity-=1
        cart_item.save()
        return redirect('addtocart')

def remove(request,product_id):  
    cart_data=Cart.objects.get(user=request.user)
    cart_item=Cartitem.objects.get(cart=cart_data,product=product_id)
    cart_item.delete()
    return redirect('addtocart')

def buynow(request):
    if request.user.is_anonymous:
        return redirect('/loginuser')
    item=[]
    if request.method=='POST':
        product=0
        if request.POST.getlist('item'):
            i_id=request.POST.getlist('item')
            for i in i_id:
                item.append(Cartitem.objects.get(id=i))
            for c_item in item:
                product+=c_item.product.p_price*c_item.quantity
            tax=(product*5)/100
            total=product+tax
            return render(request,'buy.html',{'item':item,'tax':tax,'total':total})
    
        if request.POST.get('product'):
            id=request.POST.get('product')
            quty=int(request.POST.get('quantity'))
            prod=Product.objects.get(id=id)
            prod_price=prod.p_price*quty
            tax=(prod_price*5)/100
            total=prod_price+tax
            return render(request,'buy.html',{'prod':prod,'tax':tax,'total':total,'qty':quty})
    return render(request,'buy.html')

def palce_order(request):
    if request.method=='POST':
        id=[]
        payment_method=request.POST.get('payment_method')
        total=request.POST.get('total')
        product_id=request.POST.get('product_id')
        cart_item=request.POST.getlist('cart')
        qty=request.POST.get('qty')
        # print("id=",product_id)
        # print("cart=",cart_item)
        Order.objects.create(u_id=request.user,total_amount=total)
        o_id=Order.objects.filter(u_id=request.user).order_by("-id")
        for i in o_id:
            id.append(i.id)
        last_id=id[0] 
        l_oid=Order.objects.get(id=last_id)   
        if request.POST.getlist('cart'):
            items=Cartitem.objects.filter(id__in=cart_item)
            for item in items:
                Order_details.objects.create(o_id=l_oid,product_id=item.product,quantity=item.quantity)
        if request.POST.get('product_id'):
            product=Product.objects.get(id=product_id)
            Order_details.objects.create(o_id=l_oid,product_id=product,quantity=qty)

        if payment_method=="online":
            amount = int(float(total)) * 100   # In paise  
            client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
            })
            context = {
            "order": order,
            "key_id": settings.RAZORPAY_KEY_ID,
            "amount": amount,
            'order1':l_oid,
            'method':payment_method,
            
            }

            Payment.objects.create(u_id=request.user,o_id=l_oid,payment_type=payment_method,transition_id=order['id'],payment_status="Done",payment_amount=total)
            return render(request,'buy.html',context)
            
        else:
            Payment.objects.create(u_id=request.user,o_id=l_oid,payment_type=payment_method,payment_status="Pandding",payment_amount=total)
    return render(request,'order_succes.html',{'order1':l_oid,'method':payment_method})

def order_succes(request):
    oid=request.GET.get('oid')
    l_oid=Order.objects.get(id=oid)  
    mehtod=request.GET.get('method')
    return render(request,'order_succes.html',{'order1':l_oid,'method':mehtod})

def order(request):
    if request.user.is_anonymous:
        return redirect('/loginuser')
    order_details=[]
    orders=Order.objects.filter(u_id=request.user).order_by('-id')#10,11,12,13,14
    order_details=Order_details.objects.filter(o_id__in=orders) #using this [2,3,1,4]
    #this return <QuerySet [<Order_details: Order_details object (3)>, <Order_details: Order_details object (4)>, <Order_details: Order_details object (5)>, <Order_details: Order_details object (6)>, <Order_details: Order_details object (7)>, <Order_details: Order_details object (8)>, <Order_details: Order_details object (9)>]>

    #for order in orders: #using this o_id=order [] 10->id(2,3)[[2,3],[1],[4]] 
    #   order_details.append(Order_details.objects.filter(o_id=order))
    #print(order_details)
    #this is return [<QuerySet [<Order_details: Order_details object (3)>, <Order_details: Order_details object (4)>]>, <QuerySet [<Order_details: Order_details object (5)>]>, <QuerySet [<Order_details: Order_details object (6)>]>, <QuerySet [<Order_details: Order_details object (7)>]>, <QuerySet [<Order_details: Order_details object (8)>, <Order_details: Order_details object (9)>]>]

    
    return render(request,'order.html',{'orders':orders,'order_detalis':order_details})

def order_details(request):
    feedback_product_id=[]
    if request.method=="POST":
        order_id=request.POST.get('order_id')
    sutotal=0
    orders=Order.objects.get(id=order_id)
    payment=Payment.objects.get(o_id=orders)
    items=Order_details.objects.filter(o_id=orders)
    feedbacks=Feedback.objects.filter(u_id=request.user)
    for feedback in feedbacks:
        feedback_product_id.append(feedback.product_id.id)
    for item in items:
        sutotal+=item.product_id.p_price*item.quantity
    tax=sutotal*5/100
    return render(request,'order_details.html',{'order':orders,'payment':payment,'items':items,'subtotal':sutotal,'tax':tax,'feedback_product_id':feedback_product_id})

def product_details(request):
    product=Product.objects.all()
    paginator=Paginator(product,3)
    page=request.GET.get('page')
    data=paginator.get_page(page)
    id=request.GET.get('product')
    prod=None
    if id:
        prod=Product.objects.get(id=id)
        feedback=Feedback.objects.filter(product_id=prod)
        gallery=Gallery.objects.filter(product_id=prod)
        return render(request,'product_details.html',{'prod':prod,'product':data,'feedback':feedback,'gallerys':gallery})
    return render(request,"product_details.html",{'product':data})

def feedback(request,product_id):
    #product_id=request.GET.get('product_id')
    if request.method=="POST":
        detail=request.POST.get('message')
        star=request.POST.get('rating')
        p_id=Product.objects.get(id=product_id)
        Feedback.objects.create(u_id=request.user,product_id=p_id,feedback_details=detail,feedback_star=star)
        return redirect('/order')
    
    return render(request,'feedback.html')

def edit_feedback(request,product_id):
    #product_id=request.GET.get('product_id')
    p_id=Product.objects.get(id=product_id)
    feedback=Feedback.objects.get(u_id=request.user,product_id=p_id)
    print('feedback',feedback)
    if request.method=="POST":
        detail=request.POST.get('message')
        star=request.POST.get('rating')
        feedback.feedback_details=detail
        feedback.feedback_star=star
        feedback.feedback_date=date.today()
        feedback.save()
        return redirect('/order')
    
    return render(request,'feedback.html',{'feedback':feedback})

