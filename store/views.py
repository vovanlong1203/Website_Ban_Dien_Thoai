from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from forms import *
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
import random
import plotly.graph_objs as go
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.password_validation import validate_password
# Create your views here.

def home(request):
    category = Category.objects.filter(status=0)
    product = Product.objects.filter(status=0)
    product_trend = Product.objects.filter(trending=1)
    product = random.sample(list(product),20)


    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    # Lấy username của người dùng
        username = request.user.username
        conext = {'category':category, 'product':product,'username':username,"cart": cart,"product_trend":product_trend}
    else:
        conext = {'category':category, 'product':product,"product_trend":product_trend}

    return render(request, 'store/index.html',conext)


def contact_us(request):
    category = Category.objects.filter(status=0)
    product = Product.objects.filter(status=0)    
    

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    # Lấy username của người dùng
        # username = request.session['username']
        username = request.user.username
        conext = {'category':category, 'product':product,'username':username,"cart": cart}
    else:
        conext = {'category':category, 'product':product,}

    return render(request, 'store/contactus.html',conext)

def add_contact_us(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact()
        contact.name = name
        contact.email = email
        contact.subject = subject
        contact.message = message
        contact.save()

        return redirect('contactus')
    return render(request, 'store/contactus.html')

def about_us(request):
    category = Category.objects.filter(status=0)    
    product = Product.objects.filter(status=0)
    request.session['username'] = request.session.get('username')

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    # Lấy username của người dùng
        # username = request.session['username']
        username = request.user.username
        conext = {'category':category, 'product':product,'username':username,"cart": cart}
    else:
        conext = {'category':category, 'product':product,}
    return render(request, 'store/aboutus.html',conext)




def productdetail(request,pk):
    category = Category.objects.filter(status=0)
    product = Product.objects.get(id = pk)
    product_review = Product.objects.get(id = pk)
    reviews = Review.objects.filter(product=product_review)    
    request.session['username'] = request.session.get('username')

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        # username = request.session['username']  
        username = request.user.username
        context =   {'product': product,"cart": cart,'reviews': reviews,'username':username,'category':category}
    else:
        context = {'product': product,'reviews': reviews,'category':category}
    return render(request, 'store/product_detail.html', context)



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def category_view(request, pk):
    request.session['username'] = request.session.get('username')
    category = Category.objects.all()
    category_tmp = Category.objects.get(id=pk)
    products = Product.objects.filter(category= category_tmp)


    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        # username = request.session['username'] 
        username = request.user.username
        context = {'category':category, 'category_tmp':category_tmp, 'products': products, 'username':username,"cart": cart,}

    else:
        context = {'category':category, 'category_tmp':category_tmp, 'products': products, }


    return render(request, 'store/category.html',context)
    

def sort_increment_product(request, pk):
    request.session['username'] = request.user.username
    category = Category.objects.all()
    category_tmp = Category.objects.get(id=pk)
    products = Product.objects.filter(category= category_tmp)
    products = products.order_by('selling_price')
    if request.user.is_authenticated:
        if request.session['username']:
            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
            username = request.session['username']  
            context = {'category':category, 'category_tmp':category_tmp, 'products': products, 'username':username,"cart": cart, }
        else:
            context = {'category':category, 'category_tmp':category_tmp, 'products': products,"cart": cart, }
    else:
        context = {'category':category, 'category_tmp':category_tmp, 'products': products,}

    return render(request, 'store/category.html',context)

def sort_decrement_product(request, pk):
    request.session['username'] = request.user.username
    category = Category.objects.all()
    category_tmp = Category.objects.get(id=pk)
    products = Product.objects.filter(category= category_tmp)
    products = products.order_by('-selling_price')
    if request.user.is_authenticated:
        if request.session['username']:
            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
            username = request.session['username']
            context = {'category':category, 'category_tmp':category_tmp, 'products': products, 'username':username,"cart": cart, }
        else:
            context = {'category':category, 'category_tmp':category_tmp, 'products': products,"cart": cart, }
    else:
        context = {'category':category, 'category_tmp':category_tmp, 'products': products,}

    return render(request, 'store/category.html',context)



def login_view(request):
    category = Category.objects.filter(status=0)
    product = Product.objects.filter(status=0)
    
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        try:
            print("pass: ",pass1)
            validate_password(pass1)

            print("Mật khẩu hợp lệ")
        except Exception as e:
            conext = {'category':category, 'product':product, 'message': 'Sai mật khẩu hoặc sai tên đăng nhập!!'}
            return render(request, 'store/login.html',conext)


        user = authenticate(username=username,password=pass1)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            username = request.session['username']
            messages.success(request, "Logged In Sucessfully!!")
            conext = {'category':category, 'product':product, 'username':username}
            return redirect('home')
        else:
            conext = {'message': 'Sai mật khẩu hoặc sai tên đăng nhập!!'}
            return render(request, 'store/login.html',conext)
    return render(request, 'store/login.html',{'category':category})

def update_profile_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        fisrtname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        user = User.objects.get(username=username)
        user.first_name = fisrtname
        user.last_name =lastname
        user.email = email
        user.save()
    return redirect('profile')

def change_password_view(request):
    request.session['username'] = request.user.username
    username = request.session['username']
    username = request.user.username
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    user = User.objects.get_or_create(username=request.user.username)
    category = Category.objects.filter(status=0)
    context = {'username': username,"cart":cart,'category':category}
    return render(request, 'store/changepassword.html',context)

from django.contrib.auth import update_session_auth_hash

def update_password_user(request):
    request.session['username'] = request.user.username
    username = request.session['username']

    if request.method == 'POST':
        user = User.objects.get(username= request.user.username)
        new_pass = request.POST['new_password']
        comfirm_pass = request.POST['confirm_newpassword']
        un = user.username
        if new_pass != comfirm_pass:
            messages.error(request,"Mật khẩu không khớp")
            return redirect('changepassword_view')
        try:
            validate_password(new_pass)
            print("Mật khẩu hợp lệ")
        except Exception as e:
            messages.error(request,"thay đổi mật khẩu thất bại")
            return redirect('changepassword_view')

        user.set_password(new_pass)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request,"thay đổi mật khẩu thành công")
        return redirect('changepassword_view')

    return render(request, 'store/changepassword.html')

def signup_view(request):
    category = Category.objects.filter(status=0)
    conext = {'category':category}
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            conext = {'message': 'Username already exist! Please try some other username.'}
            return render(request,'store/signup.html',conext)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            conext = {'message': 'Email Already Registered!!.'}
            return render(request,'store/signup.html',conext)

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            conext = {'message': "Passwords didn't matched!!"}
            return render(request,'store/signup.html',conext)
        
        try:
            validate_password(pass1)
            print("Mật khẩu hợp lệ")
        except Exception as e:
            messages.error(request,"mật khẩu không hợp lệ!")
            conext = {'category':category, 'message': 'mật khẩu không hợp lệ!'}
            return render(request,'store/signup.html',conext)
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        return render(request, 'store/login.html',{'category':category,'message': 'Đăng kí tài khoản thành công!!'})

    return render(request, 'store/signup.html',{'category':category})


def signout_view(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created =CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        num_of_item = cart.num_of_items
        
        print(cartitem)
    return JsonResponse(num_of_item, safe=False)

def payment_view(request):
    cart =None
    cartitems = []
    category = Category.objects.filter(status=0)
    request.session['username'] = request.user.username
    if request.session['username']:
        if request.user.is_authenticated:
            user = User.objects.get(id = request.user.id )
            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
            cartitems = cart.cartitems.all()
            username = request.session['username']
        context = {"cart":cart, 'items':cartitems,'username':username,'category':category, 'user':user}
    else:
        context = {"cart":cart, 'items':cartitems,'category':category}

    return render(request, 'store/checkout.html', context)



def place_order(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        neworder.first_name = request.POST['firstname']
        neworder.last_name = request.POST['lastname']
        neworder.email = request.POST['email']
        neworder.address = request.POST['address']
        neworder.phone = request.POST['phonenumber']
        # neworder.zipcode = request.POST['zipcode']

        if neworder.first_name==''or neworder.last_name == ''or neworder.email == ''or neworder.address == ''or neworder.phone == '':
            return redirect('checkout')

        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        neworder.total = cart.total_price
        neworder.save()
        # cart = get_object_or_404(Cart, user=request.user)
        tmp = cart
        for item in cart.cartitems.all():
            order_item = OrderItem(order=neworder, product=item.product, quantity=item.quantity,price=item.product.selling_price, total_price= item.price)
            order_item.save()
            item.delete()

    messages.success(request,"thanh cong")
    return redirect('home')

def order(request):
    category = Category.objects.filter(status=0)
    if request.user.is_authenticated:

        # username = request.session['username']
        username = request.user.username
        cart = None
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

        try:
            orders = Order.objects.filter(user=request.user)
        except Order.DoesNotExist:
            orders = None
            
        order_items = []
        items = None
        for order in orders:
            items = OrderItem.objects.filter(order=order)
            order_items.append({'order': order, 'items': items})
        
    context = {'orders': orders, 'order_items': order_items,
               'username': username, 'cart':cart,'category':category}
    
    return render(request,'store/order.html',context)

def increment_product(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created =CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        num_of_item = cart.num_of_items
        
        print(cartitem)
    return JsonResponse(num_of_item, safe=False)


def decrement_product(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created =CartItem.objects.get_or_create(cart=cart, product=product)
        if (cartitem.quantity == 1):
            cartitem.quantity = 1
        else:
            cartitem.quantity -= 1

        cartitem.save()
        num_of_item = cart.num_of_items
        print(cartitem)

    return JsonResponse(num_of_item, safe=False)


def cart(request):
    cart =None
    cartitems = []
    category = Category.objects.filter(status=0)

    request.session['username'] = request.user.username

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()
        username = request.session['username']
        context = {"cart":cart, 'items':cartitems,'username':username,'category':category}
    else:
        context = {"cart":cart, 'items':cartitems,'category':category}

    return render(request, 'store/cart.html',context)


def search_product(request):
    category = Category.objects.filter(status=0)
    if request.user.is_authenticated:
        if request.method == 'POST':
            search = request.POST['search']
            product=Product.objects.filter(name__contains=search)
            username = request.user.username
            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        else:
            product = Product.objects.filter(status=0)
        conext = {'product':product,'username':username,'cart':cart,'category':category}
    else:
        if request.method == 'POST':
            search = request.POST['search']
            product=Product.objects.filter(name__contains=search)
        else:
            product = Product.objects.filter(status=0)
        conext = {'product':product,'category':category}
    
    return render(request, 'store/search_product.html',conext)


def Review_Rate(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        comment = request.GET['comment']
        rate = request.GET['rate']
        user = request.user
        Review(user=user,product=product,comment=comment,rate=rate).save()
        return redirect('productdetail',pk=prod_id)


def remove_product(request,pk):
    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, id=pk,)
        cart = item.cart
        item.delete()
        return redirect('cart')
    else:
        return redirect('cart')


def plus_item(request,pk):
    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, id=pk)
        item.quantity += 1
        item.save()
        return redirect('cart')
    else:
        return redirect('cart')


def minus_item(request,pk):
    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, id=pk)
        if item.quantity == 1:
            item.quantity = 1
        else:
            item.quantity -= 1
        item.save()
        return redirect('cart')
    else:
        return redirect('cart')


def profile_view(request):
    category = Category.objects.filter(status=0)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()
        username = request.user.username
        print("username : ",username)
        user = User.objects.get_or_create(username=username)
    context = {"cart":cart, 'items':cartitems,'username':username,'category':category}

    return render(request, 'store/profile.html',context)

def admin_login_view(request):
    return render(request, 'admin/adminlogin.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']     
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)  
        if user is not None:
            if user.is_superuser:
                login(request, user)
                print("admin_dashboard")
                return redirect('admin_dashboard')
            else:
                print("adminlogin")
                return redirect('adminlogin')
    else:
        return redirect('adminlogin')
    return render(request, 'admin/adminlogin.html')




# -------------------------function Admin---------------------------------


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    customercount= User.objects.all().count()
    productcount= Product.objects.all().count()
    ordercount = Order.objects.all().count()
    order= Order.objects.all()

    orders = Order.objects.all().order_by('date_ordered')
    months = [o.date_ordered.strftime('%Y-%m') for o in orders]
    amounts = [o.total for o in orders]
    data = [
        go.Bar(
            x=months,
            y=amounts,
        )
    ]
    layout = go.Layout(
        title='Monthly Order Statistics',
        xaxis=dict(title='Month'),
        yaxis=dict(title='Total Amount'),
    )
    fig = go.Figure(data=data, layout=layout)
    chart_div = fig.to_html(full_html=False)
    
    
    context = {'customercount': customercount, 'productcount': productcount,'ordercount': ordercount, 'chart_div':chart_div}

    orders = Order.objects.annotate(month=TruncMonth('date_ordered')).values('month').annotate(total_amount=Sum('total')).order_by('month')
    print("orders: ",orders)
    months = [str(o['month'])[:7] for o in orders]
    amounts = [o['total_amount'] for o in orders]

    context = {'customercount': customercount, 'productcount': productcount,'ordercount': ordercount, 'chart_div':chart_div,'months':months, 'amounts':amounts,"order":order}

    return render(request, 'admin/admin_dashboard.html', context)


def sales_chart(request):
    orders = Order.objects.annotate(month=TruncMonth('date_ordered')).values('month').annotate(total_amount=Sum('total')).order_by('month')
    print("orders: ",orders)
    months = [str(o['month'])[:7] for o in orders]
    print("month: ",months)
    amounts = [o['total_amount'] for o in orders]
    print("amounts: ",amounts)

    return JsonResponse(data={
    'labels': months,
    'values': amounts
})



@login_required(login_url='adminlogin')
def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('adminlogin')


@login_required(login_url='adminlogin')
def customer_view(request):
    customers_list= User.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(customers_list, 10)
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    context = {'customers':customers}
    return render(request, 'admin/view_customer.html',context)

@login_required(login_url='adminlogin')
def product_view(request):
    product_list= Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'products':products}
    return render(request, 'admin/view_products.html',context)


@login_required(login_url='adminlogin')
def add_product_view(request):
    cat = Category.objects.all()
    category_list = [c.name for c in cat]
    print(category_list)
    context = {'category_list':category_list}
    return render(request, 'admin/add_product_view.html',context)


@login_required(login_url='adminlogin')
def add_product_admin(request):
    if request.method == 'POST':
        product = Product()
        category = request.POST['category']
        category_tmp = Category.objects.get(name=category)
        name =  request.POST['name']
        image = request.FILES['image'] if 'image' in request.FILES else None
        if image:
            product.image = image
        quantity = request.POST['quantity']
        description = request.POST['description']
        original_price = request.POST['original_price']
        selling_price = request.POST['selling_price']
        status = request.POST.get('status')
        if status :
            status = 1
        else:
            status = 0
        trending = request.POST.get('trending')
        if trending :
            trending = 1
        else:
            trending = 0
        product.category = category_tmp
        product.name = name
        product.quantity = quantity
        product.description = description
        product.original_price = original_price
        product.selling_price =selling_price
        product.status = status
        product.trending = trending
        print("product: ", product)
        product.save()
        return redirect('product_view')
    return render(request, 'admin/view_products.html')
        
@login_required(login_url='adminlogin')
def update_product_view(request, pk):
    product = Product.objects.get(id=pk)
    category_list = [c.name for c in Category.objects.all()]
    context = {'product': product,'category_list':category_list}
    return render(request, 'admin/view_update_product.html',context)

@login_required(login_url='adminlogin')
def update_product(request):
    if request.method == 'POST':
        id_product = request.POST['id_product']
        product = Product.objects.get(id=id_product)
        category = request.POST['category']
        category_tmp = Category.objects.get(name=category)
        name =  request.POST['name']
        image = request.FILES['image'] if 'image' in request.FILES else None
        if image:
            product.image = image
        quantity = request.POST['quantity']
        description = request.POST['description']
        original_price = request.POST['original_price']
        selling_price = request.POST['selling_price']
        status = request.POST.get('status')
        if status :
            status = 1
        else:
            status = 0
        trending = request.POST.get('trending')
        if trending :
            trending = 1
        else:
            trending = 0
        product.category = category_tmp
        product.name = name
        product.quantity = quantity
        product.description = description
        product.original_price = original_price
        product.selling_price =selling_price
        product.status = status
        product.trending = trending
        print("product: ", product)
        product.save()
        return redirect('product_view')
    return render(request, 'admin/view_products.html')


@login_required(login_url='adminlogin')
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('product_view')




@login_required(login_url='adminlogin')
def customer_update_view(request,pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request, 'admin/customer_update_view.html',context)

@login_required(login_url='adminlogin')
def update_customer(request):
    id_user = request.POST['id_user']
    fisrtname = request.POST['firstname']
    lastname = request.POST['lastname']
    username = request.POST['username']
    email = request.POST['email']
    user = User.objects.get(id=id_user)
    user.first_name = fisrtname
    user.last_name =lastname
    user.email = email
    user.username = username
    user.save()
    return redirect('customer_view')
    

@login_required(login_url='adminlogin')
def delete_customer(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('customer_view')


@login_required(login_url='adminlogin')
def category_view_admin(request):
    categorys_list= Category.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(categorys_list, 5)
    try:
        categorys = paginator.page(page)
    except PageNotAnInteger:
        categorys = paginator.page(1)
    except EmptyPage:
        categorys = paginator.page(paginator.num_pages)  
    context = {'categorys':categorys}
    return render(request, 'admin/view_category.html',context)


@login_required(login_url='adminlogin')
def add_category_view(request):
    return render(request, 'admin/add_category_view.html')

@login_required(login_url='adminlogin')
def cart_view_admin(request):
    cart_list= Cart.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(cart_list, 10)
    try:
        carts = paginator.page(page)
    except PageNotAnInteger:
        carts = paginator.page(1)
    except EmptyPage:
        carts = paginator.page(paginator.num_pages)
    context = {'carts':carts}
    return render(request, 'admin/view_cart.html',context)

@login_required(login_url='adminlogin')
def cartitem_view_admin(request):
    cartitems= CartItem.objects.all()
    context = {'cartitems':cartitems}
    return render(request, 'admin/view_cartitem.html',context)

@login_required(login_url='adminlogin')
def review_view_admin(request):
    review_list= Review.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(review_list, 10)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    context = {'reviews':reviews}
    return render(request, 'admin/view_review.html',context)


@login_required(login_url='adminlogin')
def order_view_admin(request):
    order_list= Order.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(order_list, 10)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {'orders':orders}
    return render(request, 'admin/view_order.html',context)

@login_required(login_url='adminlogin')
def orderitem_view_admin(request):
    orderitem_list= OrderItem.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(orderitem_list, 10)
    try:
        orderitems = paginator.page(page)
    except PageNotAnInteger:
        orderitems = paginator.page(1)
    except EmptyPage:
        orderitems = paginator.page(paginator.num_pages)
    context = {'orderitems':orderitems}
    return render(request, 'admin/view_orderitem.html',context)

@login_required(login_url='adminlogin')
def view_update_category(request,pk):
    category = Category.objects.get(id=pk)
    context = {'category':category}    
    return render(request, 'admin/view_update_category.html',context)

@login_required(login_url='adminlogin')
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES['image'] if 'image' in request.FILES else None
        description = request.POST['description']
        status = request.POST.get('status')
        if status:
            status = 1
        else:
            status = 0
        category = Category()
        category.name = name
        category.description = description
        print("Image: ", image)
        if image:
            category.image = image
        category.status = status
        category.save()
        return redirect('category_view_admin')
    return render(request, 'admin/view_category.html')

@login_required(login_url='adminlogin')
def update_category(request):
    if request.method == 'POST':
        id_category = request.POST['id_category']
        category = Category.objects.get(id=id_category)
        name = request.POST['name']
        image = request.POST['image']
        print("image: ",image)
        image = request.FILES['image'] if 'image' in request.FILES else None
        if image:
            category.image = image
        print("image: ", image)
        description = request.POST['description']
        status = request.POST.get('status')
        if status :
            status = 1
        else:
            status = 0
        category.name = name
        category.description = description
        category.status = status
        category.save()
        return redirect('category_view_admin')
    return render(request, 'admin/view_category.html')

def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('category_view_admin')



@login_required(login_url='adminlogin')
def view_update_order(request,pk):
    status_list = [status[0] for status in Order.STATUS]

    order = Order.objects.get(id=pk)
    context = {'order':order,'status_list':status_list}
    return render(request, 'admin/view_update_order.html',context)

@login_required(login_url='adminlogin')
def update_status_order(request):
    if request.method == 'POST':
        id_order = request.POST['id_order']
        status = request.POST['status']
        order = Order.objects.get(id=id_order)
        order.status = status
        order.save()
        return redirect('order_view_admin')
    return render(request, 'admin/order_view_admin.html')

@login_required(login_url='adminlogin')
def contactus_view(request):
    contact_us_list = Contact.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(contact_us_list, 10)
    try:
        contact_us = paginator.page(page)
    except PageNotAnInteger:
        contact_us = paginator.page(1)
    except EmptyPage:
        contact_us = paginator.page(paginator.num_pages)
    context = {'contact_us': contact_us}
    return render(request, 'admin/view_contactus.html', context)