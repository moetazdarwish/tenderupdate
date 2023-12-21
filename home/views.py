from random import randint

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
import uuid
import json
from cart.models import Cart, CartProducts, CartName
from crm.models import CustomerProfile
from delivery.models import DeliveryCost
from home.models import HomePage
from kitchen.models import KitCategory, KitchenRecipe, PricingSystem, RecipePrice
from tender import settings

from django.contrib import messages
# Create your views here.

def home(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'catg':
            xx = request.COOKIES.get('user')
            val = request.POST.get('val')
            cate = KitCategory.objects.get(id=val)
            pric = PricingSystem.objects.get(point='Main')
            recipe = RecipePrice.objects.filter(profil=pric,name__cate=cate)
            context = {'sts': 'catg', 'recipe': recipe}
            return render(request, 'home/sub.html', context)

        if action == 'add':
            val = request.POST.get('val')
            usr = request.COOKIES.get('user_id')
            code = request.COOKIES.get('cart')
            cp = CustomerProfile.objects.get(id=usr)
            rp = RecipePrice.objects.get(id=val)
            cn = CartName.objects.filter(online=True).first()
            obj, create = Cart.objects.get_or_create(branch=cn,customer=cp, transaction_id=code, status='NEW')
            prd_obj, new = CartProducts.objects.get_or_create(order=obj, product=rp)
            prd_obj.quantity += 1
            prd_obj.price = rp.price
            prd_obj.status = code
            prd_obj.save()
            return redirect(home)
    cn = CartName.objects.filter(online=True).first()
    cate = KitCategory.objects.all()
    recipe = RecipePrice.objects.filter(profil=cn.pricing)
    context = {'cate':cate,'recipe':recipe}
    response =  render(request, 'home/index.html', context)
    if  request.COOKIES.get('user_id'):
        xx = request.COOKIES.get('user_id')
        cp = CustomerProfile.objects.get(id=xx)
        try :
            obj = Cart.objects.get(customer=cp, status='NEW')
            count = obj.cart_items
            response.set_cookie(key='count', value=count)
            return response
        except:
            ct_code = create_transaction()
            response.set_cookie(key='cart', value=ct_code)
            response.set_cookie(key='count', value=0)
            return response
    else:
        code = uuid.uuid4()
        ct_code = create_transaction()
        cp = CustomerProfile.objects.create(uuid=code)
        response.set_cookie(key='user', value=code)
        response.set_cookie(key='user_id', value=cp.id)
        response.set_cookie(key='count', value=0)
        response.set_cookie(key='cart', value=ct_code)
        return response


def about(request):
    title = HomePage.objects.get(name='ab_title')
    about = HomePage.objects.get(name='about')
    context = {'title':title,'about':about}
    return render(request, 'home/about.html', context)

def create_transaction():
    range_start = 10 ** (5 - 1)
    range_end = (10 ** 5) - 1
    timeTrans = str(datetime.now().timestamp())[:4]
    codeTrans = randint(range_start, range_end)
    transaction_id =  timeTrans +str(codeTrans)
    return transaction_id


def addCartItem(request):
    val = request.POST.get('val')
    usr = request.COOKIES.get('user_id')
    code = request.COOKIES.get('cart')
    cp = CustomerProfile.objects.get(id=usr)
    rp = RecipePrice.objects.get(id=val)
    cn = CartName.objects.filter(online=True).first()
    obj, create = Cart.objects.get_or_create(branch=cn,customer=cp, transaction_id=code, status='NEW')
    prd_obj, new = CartProducts.objects.get_or_create(order=obj, product=rp)
    prd_obj.quantity += 1
    prd_obj.price = rp.price
    prd_obj.status = code
    prd_obj.save()
    count = obj.cart_items
    context = {'sts': 'cut', 'count': count}
    return render(request, 'home/sub.html', context)
    # return HttpResponse(status=200, headers={
    #     'hx-trigger': 'hi'
    # })

def cartDetails(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'add':
            val = request.POST.get('val')
            prd_obj= CartProducts.objects.get(id=val)
            prd_obj.quantity += 1
            prd_obj.save(update_fields=['quantity'])
            obj= Cart.objects.get(id=prd_obj.order.id,)
            area = DeliveryCost.objects.all()
            context = {'sts': 'chcart','obj':obj, 'area': area}
            return render(request, 'home/sub.html', context)
        if action == 'fnd':
            phone = request.POST.get('phone')
            cp = CustomerProfile.objects.filter(phone__icontains=phone).first()
            code = request.COOKIES.get('cart')
            obj= Cart.objects.get(transaction_id=code)
            obj.customer=cp
            obj.save(update_fields=['customer'])
            context = {'sts': 'cust','cp':cp}
            response =  render(request, 'home/sub.html', context)
            response.set_cookie(key='user_id', value=cp.id)
            return response
        if action == 'pay':
            val = request.POST.get('val')
            obj = Cart.objects.get(id=val)
            if obj.customer.phone:
                obj.status = 'PAID'
                obj.online = True
                obj.save()
                messages.success(request, "ONLINE ORDER")

                context = {'sts': 'confirm'}
                return render(request, 'home/sub.html', context)
            context = {'sts': 'error'}
            return render(request, 'home/sub.html', context)
        if action == 'paycut':
            val = request.POST.get('val')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            mail = request.POST.get('mail')
            date = request.POST.get('date')
            know = request.POST.get('know')
            note = request.POST.get('note')
            add1 = request.POST.get('add1')
            add2 = request.POST.get('add2')
            add3 = request.POST.get('add3')
            cp = CustomerProfile.objects.create(name=name,addres_0=add1,addres_1=add2,addres_2=add3,note=note,
                                                phone=phone,mail=mail,know_us=know,i_date=date)

            obj= Cart.objects.get(id=val)
            obj.customer=cp
            obj.save(update_fields=['customer'])
            context = {'sts': 'netcust','cp':cp}
            response =  render(request, 'home/sub.html', context)
            response.set_cookie(key='user_id', value=cp.id)
            return response
        if action == 'mins':

            val = request.POST.get('val')
            prd_obj= CartProducts.objects.get(id=val)
            prd_obj.quantity -= 1
            prd_obj.save(update_fields=['quantity'])
            ordr = prd_obj.order.id
            if prd_obj.quantity == 0:
                prd_obj.delete()
            obj = Cart.objects.get(id=ordr, )
            area = DeliveryCost.objects.all()
            context = {'sts': 'chcart', 'obj': obj, 'area': area}
            return render(request, 'home/sub.html', context)
        if action == 'ara':
            val = request.POST.get('val')
            slarea = request.POST.get('slarea')
            area = DeliveryCost.objects.get(id=slarea)
            crt= Cart.objects.get(id=val)
            crt.delivery = area.price
            crt.save(update_fields=['delivery'])
            context = {'sts': 'ara','area': area}
            return render(request, 'home/sub.html', context)

    usr = request.COOKIES.get('user_id')
    code = request.COOKIES.get('cart')
    cp = CustomerProfile.objects.get(id=usr)

    cn = CartName.objects.filter(online=True).first()
    obj , cret = Cart.objects.get_or_create(branch=cn,customer=cp,transaction_id=code, status='NEW')
    area = DeliveryCost.objects.all()
    context = {'sts': 'cut','obj':obj,'area':area ,'cp':cp}
    return render(request, 'home/cart.html', context)

def userlogin(request):
    if request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            get_user = User.objects.get(username=user)
            group = None
            if get_user.groups.exists():
                group = get_user.groups.all()[0].name
                if group == 'Hr':
                        return redirect('ticket_employee')
                if group == 'Account':
                        return redirect('accRequest')
                if group == 'Inventory':
                        return redirect('inventoryTask')
                if group == 'Kitchen':
                        return redirect('task')
                if group == 'POS Manager':
                        return redirect('posLogin')
                if group == 'POS Task':
                        return redirect('posLogin')
                if group == 'admin':
                        return redirect('ticket_employee')
                return redirect(userlogin)
        #
        #     return redirect('login')
        else:
            messages.error(request, 'Username or Password is incorrect')
    context = {'sts': 'cut'}
    return render(request, 'home/login.html', context)


def logout_view(request):
    print('hellll')
    logout(request)
    return redirect(userlogin)

def adminPage(request):
    context = {'sts': 'cut'}
    return render(request, 'home/dash.html', context)