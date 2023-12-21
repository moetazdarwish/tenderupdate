import decimal

from django.db.models import Q, Avg, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
import csv
from account.models import AccountLedger
# Create your views here.
from cart.models import *
from crm.models import CustomerDirectory, CustomerDiscount
from crm.views import custmeCode
from delivery.models import OrderDelivery, DeliveryCost
from inventory.models import Inventory
from inventory.pdfcreator import render_to_pdf
from kitchen.models import PricingSystem, kitchenTask, KitchenJobsAssign, FeatuersPrice, KitCategory, KitchenInventory



def createCart(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'inv':
            context = {'sts': 'inv'}
            return render(request, 'cart/sub.html', context)
        if action == 'dinv':
            context = {'sts': 'dinv'}
            return render(request, 'cart/sub.html', context)
        if action == 'dtsk':
            context = {'sts': 'dtsk'}
            return render(request, 'cart/sub.html', context)
        if action == 'tsk':
            context = {'sts': 'tsk'}
            return render(request, 'cart/sub.html', context)
        if action == 'donln':
            context = {'sts': 'donln'}
            return render(request, 'cart/sub.html', context)
        if action == 'onln':
            context = {'sts': 'onln'}
            return render(request, 'cart/sub.html', context)
        if action == 'new':
            prfl = request.POST.get('prfl')
            name = request.POST.get('name')
            pwd = request.POST.get('pwd')
            flat = request.POST.get('flat')
            percent = request.POST.get('percent')
            pwd2 = request.POST.get('pwd2')
            inv2 = request.POST.get('inv2')
            onlin = request.POST.get('onlin')
            task = request.POST.get('task')

            ps = PricingSystem.objects.get(id=prfl)
            cn = CartName.objects.create(name=name,pwd=pwd,flat=flat,prcnt=percent,
                                         b_pwd=pwd2,task=task,inv=inv2,online=onlin,pricing=ps)
            if inv2 == True:
                rp = RecipePrice.objects.filter(profil=ps)

                kt = kitchenTask.objects.create(for_sale=False,for_cart=True,status='PENDING')
                for i in rp:
                    CartInv.objects.create(cart=cn,recipe=i.name,pricing=i)
                    KitchenJobsAssign.objects.create(task=kt, recipe=i.name,for_sale=False,for_cart=True)
                    if i.feature:
                        fp = FeatuersPrice.objects.filter(name=i)
                        for f in fp:
                            KitchenJobsAssign.objects.create(task=kt, feat=f.extra)

            context = {'cn': cn,'sts':'crf'}
            return render(request, 'cart/sub.html', context)


    ps = PricingSystem.objects.all()
    context = {'ps': ps}
    # return render(request, 'paper/cart.html',context )
    return render(request, 'cart/creat_cart.html',context )


def posLogin(request):
    if request.POST:
        prfl = request.POST.get('prfl')
        pwd = request.POST.get('pwd')
        cr = CartName.objects.get(id=prfl)
        if cr.pwd == pwd:
            return redirect(posCash,cr.id)
    cr = CartName.objects.all()
    context = {'cr': cr}
    return render(request, 'cart/poslogin.html', context)

def posTaskLogin(request):
    if request.POST:
        prfl = request.POST.get('prfl')
        pwd = request.POST.get('pwd')
        cr = CartName.objects.get(id=prfl)
        if cr.pwd == pwd:
            return redirect(taskPOS,cr.id)
    cr = CartName.objects.all()
    context = {'cr': cr}
    return render(request, 'cart/poslogin.html', context)

def posCash(request,pk):
    if request.user.is_authenticated:
        if request.POST:
            cash= request.POST.get('cash')
            cr = CartName.objects.get(id=pk)
            Today = datetime.today()
            CartCash.objects.create(cart=cr,start=cash,t_strt=Today)
            return redirect(posPage, cr.id)
        try :
            cr = CartName.objects.get(id=pk)
            CartCash.objects.get(cart=cr, p_close=False)
            return redirect(posClose, cr.id)
        except:
            cr = CartName.objects.get(id=pk)
            context = {'cr': cr,'pk':pk}
            return render(request, 'cart/pos_acc.html', context)
def posClose(request,pk):

    if request.POST:
        cash= request.POST.get('cash')
        cr = CartName.objects.get(id=pk)
        Today = datetime.today()
        crt_ch = CartCash.objects.filter(cart=cr,p_open=True, p_close=False).first()
        crt_ch.close = cash
        crt_ch.t_end = Today
        crt_ch.p_close = True
        crt_ch.rev = True
        crt_ch.save()
        CartCash.objects.filter(cart=cr, rev=False).update(rev=True,p_close=True)
        txt = 'PSO {0} CLOSING BALANCE'.format(cr.name)
        AccountRequest.objects.create(ref='POS_CL',section='POS',item_id=crt_ch.id,item=txt,amount=cash)
        return redirect(posCash, cr.id)
    cr = CartName.objects.get(id=pk)
    outamut  = CartCash.objects.filter(cart=cr, rev=False).aggregate(amount=Sum('amt_out'))['amount']
    inamut  = CartCash.objects.filter(cart=cr, rev=False).aggregate(amount=Sum('amt_in'))['amount']
    am_strt = CartCash.objects.filter(cart=cr,p_open=True, p_close=False)
    if outamut is None:
        outamut= 0
    if inamut is None:
        inamut= 0
    total = am_strt[0].start + inamut - outamut
    context = {'cr': cr,'pk':pk,'total':total}
    return render(request, 'cart/pos_close.html', context)
def create_transaction():
    range_start = 10 ** (5 - 1)
    range_end = (10 ** 5) - 1
    timeTrans = str(datetime.now().timestamp())[:4]
    codeTrans = randint(range_start, range_end)
    transaction_id =  timeTrans +str(codeTrans)
    return transaction_id
def posPage(request,pk):
    if request.user.is_authenticated:
        if request.htmx:
            action = request.POST.get('action')
            print(action)
            if action == 'slcate':
                g_cat = request.POST.get('cate')
                code = request.POST.get('code')
                cat_id = KitCategory.objects.get(id=g_cat)
                cr = CartName.objects.get(id=pk)

                rp = RecipePrice.objects.filter(profil=cr.pricing,name__cate=cat_id)
                context = {'sts':'ctg','cr': cr, 'pk': pk, 'rp': rp, 'code': code}
                return render(request, 'cart/subpos.html', context)
            if action == 'custfnd':
                val = request.POST.get('cstnm')
                code = request.POST.get('code')
                cst = CustomerProfile.objects.filter(Q(name__icontains=val) | Q(phone__icontains=val))
                context = {'sts': 'custfnd', 'cst': cst, 'code': code,'pk':pk}
                return render(request, 'cart/task.html', context)
            if action == 'sel':
                val = request.POST.get('val')
                code = request.POST.get('code')
                cr = CartName.objects.get(id=pk)
                cst = CustomerProfile.objects.get(id=val)
                obj , create = Cart.objects.get_or_create(branch=cr,transaction_id=code,status='NEW')
                obj.customer = cst
                obj.save()

                return HttpResponse('done',status=200)
            if action == 'fnd':
                search = request.POST.get('search')
                code = request.POST.get('code')
                cr = CartName.objects.get(id=pk)
                rp = RecipePrice.objects.filter(profil=cr.pricing, name__name__icontains=search)
                context = {'sts': 'ctg', 'cr': cr, 'pk': pk, 'rp': rp, 'code': code}
                return render(request, 'cart/subpos.html', context)
            if action == 'add':
                code = request.POST.get('code')
                item = request.POST.get('item')
                cr = CartName.objects.get(id=pk)
                rp = RecipePrice.objects.get(id=item)
                obj , create = Cart.objects.get_or_create(branch=cr,transaction_id=code,status='NEW')
                prd_obj , new = CartProducts.objects.get_or_create(order=obj,product=rp)
                prd_obj.quantity +=1
                prd_obj.price =rp.price
                prd_obj.status=code
                prd_obj.save()
                context = {'sts':'add','cr': cr, 'pk': pk, 'rp': rp, 'code': code}
                return render(request, 'cart/subpos.html', context)
            if action == 'feat':
                code = request.POST.get('code')
                item = request.POST.get('item')
                extr = request.POST.get('extr')
                cr = CartName.objects.get(id=pk)
                rp = RecipePrice.objects.get(id=item)
                obj,create = Cart.objects.get_or_create(branch=cr, transaction_id=code, status='NEW')
                prd_obj ,new = CartProducts.objects.get_or_create(order=obj, product=rp)
                prd_obj.feat = True
                prd_obj.status=code
                fp = FeatuersPrice.objects.get(id=extr)
                csp , cret = CartSubProducts.objects.get_or_create(suborder=prd_obj,product=fp.extra)
                csp.quantity = csp.quantity + 1
                csp.price = decimal.Decimal(csp.price) + fp.price
                csp.save()
                prd_obj.price = prd_obj.price + fp.price
                prd_obj.save()

                context = {'sts':'add','cr': cr, 'pk': pk, 'rp': rp, 'code': code}
                return render(request, 'cart/subpos.html', context)
            if action == 'save':
                code = request.POST.get('code')
                svenm = request.POST.get('svenm')
                cr = CartName.objects.get(id=pk)
                gcrt , create = Cart.objects.get_or_create(branch=cr,transaction_id=code)
                gcrt.name = svenm
                gcrt.status = 'SAVED'
                gcrt.save()
            if action =='getsvd':
                cr = CartName.objects.get(id=pk)
                crt = Cart.objects.filter(branch=cr,status = 'SAVED')
                context = {'sts':'svd','cr': cr, 'pk': pk, 'crt': crt,}
                return render(request, 'cart/subpos.html', context)
            if action =='getpad':
                cr = CartName.objects.get(id=pk)
                crt = Cart.objects.filter(Q(status = 'PAID')|Q(status = 'READY'),branch=cr)
                context = {'sts':'getpad','cr': cr, 'pk': pk, 'crt': crt,}
                return render(request, 'cart/subpos.html', context)
            if action =='rmvsvd':
                val = request.POST.get('val')
                Cart.objects.get(id=val).delete()
                cr = CartName.objects.get(id=pk)
                crt = Cart.objects.filter(branch=cr,status = 'SAVED')
                context = {'sts':'svd','cr': cr, 'pk': pk, 'crt': crt,}
                return render(request, 'cart/subpos.html', context)
            if action =='delvsvd':
                val = request.POST.get('val')
                crt = Cart.objects.get(id=val)
                crt.status = 'READY'
                crt.save(update_fields=['status'])
                code = 'POS-{0}'.format(crt.transaction_id)
                kitchenTask.objects.filter(task=code).update(status = 'FINISH',j_end=True)
                POSTask.objects.filter(task=code).update(status = 'FINISH',j_end=True)
                cr = CartName.objects.get(id=pk)
                crt = Cart.objects.filter(Q(status = 'PAID')|Q(status = 'READY'),branch=cr)
                context = {'sts':'getpad','cr': cr, 'pk': pk, 'crt': crt,}
                return render(request, 'cart/subpos.html', context)
            if action =='slssvd':
                val = request.POST.get('val')
                cde = Cart.objects.get(id=val)
                cr = CartName.objects.get(id=pk)
                rp = RecipePrice.objects.filter(profil=cr.pricing)
                code = cde.transaction_id
                context = {'sts':'ctg','cr': cr, 'pk': pk, 'rp': rp, 'code': code}
                return render(request, 'cart/pos.html', context)
            if action =='nte':
                code = request.POST.get('code')
                txt = request.POST.get('txt')
                cr = CartName.objects.get(id=pk)
                cde , create = Cart.objects.get_or_create(branch=cr,transaction_id=code)
                cde.note = txt
                cde.save()

                return HttpResponse( status=200)
            if action =='disc':
                code = request.POST.get('code')
                amut = request.POST.get('amut')
                cr = CartName.objects.get(id=pk)
                cde = Cart.objects.get(branch=cr,transaction_id=code)
                cde.discount = amut
                cde.save()

                return HttpResponse('Done', status=200)
        cr = CartName.objects.get(id=pk)
        rp = RecipePrice.objects.filter(profil=cr.pricing)
        code = create_transaction()
        cat = KitCategory.objects.all()
        context = {'cr': cr, 'pk': pk,'rp':rp,'cat':cat,'code':code}
        return render(request, 'cart/pos.html', context)

def posMode(request,pk):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'b2c':
            cr = CartName.objects.get(id=pk)
            rp = RecipePrice.objects.filter(profil=cr.pricing)
            code = create_transaction()
            cat = KitCategory.objects.all()
            context = {'sts':'b2c','cr': cr, 'pk': pk, 'rp': rp, 'cat': cat, 'code': code}
            return render(request, 'cart/pos.html', context)
        if action == 'b2b':
            cr = CartName.objects.get(id=pk)
            rp = RecipePrice.objects.filter(profil=cr.pricing)
            code = create_transaction()
            cat = KitCategory.objects.all()
            context = {'sts':'b2b','cr': cr, 'pk': pk, 'rp': rp, 'cat': cat, 'code': code}
            return render(request, 'cart/posb2b.html', context)
def cartSubTotal(request,pk):
    if request.user.is_authenticated:
        if request.htmx:
            action = request.POST.get('action')

            if action == 'custm':

                cst = request.POST.get('cst')
                data = CustomerProfile.objects.get(id=cst)
                context = {'sts': 'custm', 'data':data }
                return render(request, 'cart/subpos.html', context)
            if action == 'cart':
                cr = CartName.objects.get(id=pk)
                code = request.POST.get('code')
                g_c = Cart.objects.filter(branch=cr,transaction_id=code).first()
                cp = CartProducts.objects.filter(order=g_c,status=code)
                context = {'sts': 'cart', 'cp': cp, 'pk': pk, 'g_c': g_c,'code':code }
                return render(request, 'cart/subpos.html', context)
            if action == 'rmv':
                cr = CartName.objects.get(id=pk)
                code = request.POST.get('code')
                val = request.POST.get('val')
                CartProducts.objects.get(id=val).delete()
                g_c = Cart.objects.filter(branch=cr,transaction_id=code).first()
                cp = CartProducts.objects.filter(order=g_c,status=code)
                context = {'sts': 'cart', 'cp': cp, 'pk': pk, 'g_c': g_c,'code':code }
                return render(request, 'cart/subpos.html', context)
            if action == 'subrmv':
                cr = CartName.objects.get(id=pk)
                code = request.POST.get('code')
                val = request.POST.get('val')
                su_c = CartSubProducts.objects.get(id=val)
                prd = CartProducts.objects.get(id=su_c.suborder.id)
                prd.price =  prd.price-(su_c.quantity * su_c.price)
                prd.save()
                su_c.delete()
                g_c = Cart.objects.filter(branch=cr,transaction_id=code).first()
                cp = CartProducts.objects.filter(order=g_c,status=code)
                context = {'sts': 'cart', 'cp': cp, 'pk': pk, 'g_c': g_c,'code':code }
                return render(request, 'cart/subpos.html', context)


def cartbusiness(request,pk):
    if request.user.is_authenticated:
        if request.htmx:
            action = request.POST.get('action')
            if action == 'add':
                code = request.POST.get('code')
                item = request.POST.get('item')
                qty = request.POST.get('qty')
                cr = CartName.objects.get(id=pk)
                rp = RecipePrice.objects.get(id=item)
                obj, create = Cart.objects.get_or_create(branch=cr, transaction_id=code, status='NEW')
                obj.big = True
                obj.save(update_fields=['big'])
                prd_obj, new = CartProducts.objects.get_or_create(order=obj, product=rp)
                prd_obj.quantity = qty
                prd_obj.price = decimal.Decimal(rp.price) * decimal.Decimal(qty)
                prd_obj.status = code
                prd_obj.save()
                context = {'sts': 'bgadd', 'prd_obj': prd_obj, 'pk': pk, 'rp': rp, 'code': code}
                return render(request, 'cart/subpos.html', context)
            if action == 'rmv':
                code = request.POST.get('code')
                item = request.POST.get('item')
                val = request.POST.get('val')

                rp = RecipePrice.objects.get(id=item)

                prd_obj = CartProducts.objects.get(id=val).delete()

                context = {'sts': 'rmv', 'pk': pk, 'rp': rp, 'code': code}
                return render(request, 'cart/subpos.html', context)
def paymnt(request,pk):
    if request.user.is_authenticated:
        if request.htmx:
            action = request.POST.get('action')

            if action == 'cash':
                code = request.POST.get('code')

                context = {'sts': 'cash', 'code':code , 'pk':pk}
                return render(request, 'cart/subpos.html', context)
            if action == 'visa':
                code = request.POST.get('code')
                context = {'sts': 'visa', 'code':code , 'pk':pk}
                return render(request, 'cart/subpos.html', context)
            if action == 'amt':
                amut = request.POST.get('amut')
                code = request.POST.get('code')

                g_c = Cart.objects.get(transaction_id=code)
                change  =decimal.Decimal(amut) -  g_c.get_cart_total
                CartCash.objects.create(cart=g_c.branch,amt_in=amut,amt_out=change,status=code)
                context = {'sts': 'chng','change':change,'code':code ,'pk':pk}
                return render(request, 'cart/subpos.html', context)
            if action == 'paid':
                code = request.POST.get('code')
                g_c = Cart.objects.get(transaction_id=code)
                if g_c.status == 'PAID' :
                    return redirect(posPage, pk=pk)
                g_c.status = 'PAID'
                g_c.save()

                return redirect(posPage,pk=pk)
            if action == 'visapaid':
                amut = request.POST.get('amut')
                code = request.POST.get('code')
                g_c = Cart.objects.get(transaction_id=code)
                g_c.status='PAID'
                g_c.ref=amut
                g_c.save()
                sts = '{0} - Visa - {1}'.format(code,amut)
                CartCash.objects.create(cart=g_c.branch, amt_in=g_c.get_cart_total,  status=sts)
                if g_c.branch.task:
                    POSTask.objects.create(task=code,pos=g_c.branch,order=g_c,status='PENDING')
                else:
                    kt = kitchenTask.objects.create(task=code, status='PENDING')
                    get_sub = CartProducts.objects.filter(order=g_c)
                    for i in get_sub:
                        KitchenJobsAssign.objects.create(task=kt,recipe=i.product.name,quantity=i.quantity,for_cart=True)
                        if i.feat:
                            feat_sub = CartSubProducts.objects.filter(suborder=i)
                            for f in feat_sub:
                                KitchenJobsAssign.objects.create(task=kt,feat=f.product,
                                                                 quantity=f.quantity,for_cart=True)
                get_sub = CartProducts.objects.filter(order=g_c)
                for i in get_sub:
                    ci = CartInv.objects.get(cart=g_c.branch,recipe=i.product.name, pricing=i.product,)
                    ci.qty= ci.qty - i.quantity
                    ci.save()
                    if i.feat:
                        feat_sub = CartSubProducts.objects.filter(suborder=i)
                        for f in feat_sub:
                            sci = CartInv.objects.get(cart=g_c.branch, feat=f.product, pricing=i.product)
                            sci.qty = sci.qty - f.quantity
                            sci.save()
                return redirect(posPage,pk=pk)

def checkDiscount(request,pk):
    code = request.POST.get('code')
    data = []
    g_c = Cart.objects.get(transaction_id=code)
    amut = g_c.get_cart_sub_total
    dis = CustomerDiscount.objects.all()
    if g_c.customer:
        nw = Cart.objects.filter(customer=g_c.customer)
        if len(nw) >= 1 :
            dis = CustomerDiscount.objects.filter(new=True,vip=False,famly=False,all=False)
            if dis:
                for i in dis:
                    amount = ((amut * i.discount) / 100) + i.flat
                    dta = {
                        'Discount': 'New Customer',
                        'amount': amount,
                    }
                    data.append(dta)
        if g_c.customer.vip:
            dis = CustomerDiscount.objects.filter(new=False,vip=True,famly=False,all=False)
            if dis:
                for i in dis:
                    amount = ((amut*i.discount)/100)+i.flat
                    dta ={
                        'Discount' : 'VIP',
                        'amount' : amount,
                    }
                    data.append(dta)
        if g_c.customer.famly:
            dis = CustomerDiscount.objects.filter(new=False,vip=False,famly=True,all=False)
            if dis:
                for i in dis:
                    amount = ((amut*i.discount)/100)+i.flat
                    dta ={
                        'Discount' : 'Family',
                        'amount' : amount,
                    }
                    data.append(dta)
        dis = CustomerDiscount.objects.filter(new=False,vip=False,famly=False,all=True)
        if dis:
            for i in dis:
                if i.direct ==  g_c.customer.direct:
                    amount = ((amut * i.discount) / 100) + i.flat
                    dta = {
                        'Discount': 'Category',
                        'amount': amount,
                    }
                    data.append(dta)

    dis = CustomerDiscount.objects.filter(site=True)
    if dis:
        for i in dis:
            amount = ((amut * i.discount) / 100) + i.flat
            dta = {
                'Discount': 'Site',
                'amount': amount,
            }
            data.append(dta)
    context = {'sts': 'disc', 'pk': pk,  'code': code,'data':data}
    return render(request, 'cart/subpos.html', context)


def checkDelivery(request,pk):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'add':
            add = request.POST.get('add')
            code = request.POST.get('code')
            print(code)
            od = OrderDelivery.objects.create(patch=code,add=add)
            area = DeliveryCost.objects.all()
            context = {'sts': 'dlvryara', 'pk': pk, 'code': code, 'od': od,'area':area}
            return render(request, 'cart/subpos.html', context)
        if action == 'addara':
            val = request.POST.get('val')
            ord = request.POST.get('ord')
            code = request.POST.get('code')
            area = DeliveryCost.objects.get(id=val)
            OrderDelivery.objects.filter(id=ord).update(area=area)
            Cart.objects.filter(transaction_id=code).update(delivery=area.price)

            return HttpResponse('<span>Done , Delivery Updated </span>',status=200)
        try:
            code = request.POST.get('code')
            print(code)
            data = Cart.objects.get(transaction_id=code)
            context = {'sts': 'delvry', 'pk': pk, 'code': code, 'data': data}
            return render(request, 'cart/subpos.html', context)
        except:
            return HttpResponse('<span>Missing Order</span>', status=200)


def taskPOS(request,pk):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'start':
            today = datetime.today()
            val = request.POST.get('val')
            tsk = POSTask.objects.get(id=val)
            tsk.status = 'START'
            tsk.start_time = today
            tsk.save(update_fields=['status','start_time'])
        if action == 'end':
            val = request.POST.get('val')
            tsk = POSTask.objects.get(id=val)
            today = datetime.today()
            tsk.status = 'FINISH'
            tsk.j_end = True
            tsk.end_time = today
            tsk.duration = (today).replace(tzinfo=None) - (tsk.start_time).replace(tzinfo=None)
            tsk.save()
        if action == 'gtsk':
            tsk = POSTask.objects.filter(j_end=False)
            context = {'sts': 'gtsk', 'task': tsk, 'pk': pk}
            return render(request, 'cart/task.html', context)

    tsk = POSTask.objects.filter(j_end = False)
    context = {'sts':'gtsk','task': tsk, 'pk':pk}
    return render(request, 'cart/tasks.html', context)


def tskrandam():
    try:
        obj = kitchenTask.objects.all().last()
        old = obj.id
    except:
        old = 0
    new = int(old) +  1
    return  'BR-{0}'.format(new)
def invPOS(request,pk):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'req':
            val = request.POST.get('val')
            inv = CartInv.objects.get(id=val)
            patch = tskrandam()
            kt = kitchenTask.objects.create(task=patch, for_sale=False, for_cart=True, status='PENDING')
            if inv.recipe:
                KitchenJobsAssign.objects.create(task=kt, recipe=inv.recipe, for_sale=False, for_cart=True)
            if inv.feat:
                KitchenJobsAssign.objects.create(task=kt, feat=inv.feat, for_sale=False, for_cart=True)
            context = {'sts': 'req', 'inv': inv, 'pk': pk}
            return render(request, 'cart/task.html', context)

        if action == 'new':
            cn = CartName.objects.get(id=pk)
            inv = CartInv.objects.filter(cart=cn)
            context = {'sts': 'new', 'inv': inv, 'pk': pk}
            return render(request, 'cart/task.html', context)
        if action == 'add':
            val = request.POST.get('val')
            rec = request.POST.get('rec')
            inv = CartInv.objects.get(id=val)
            inv.qty = inv.qty + decimal.Decimal(rec)
            inv.save()
            context = {'sts': 'add', 'inv': inv, 'pk': pk}
            return render(request, 'cart/task.html', context)
    cn = CartName.objects.get(id=pk)
    inv = CartInv.objects.filter(cart=cn)
    context = {'sts':'ginv','inv': inv, 'pk': pk}
    return render(request, 'cart/task.html', context)

def custmerOrders(request,pk):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'dtl':
            val = request.POST.get('val')
            crt = Cart.objects.get(id=pk)
            cp = CartProducts.objects.filter(order=crt)
            context = {'sts': 'orddtl', 'crt': crt,'cp':cp}
            return render(request, 'crm/sub.html', context)
    cst = CustomerProfile.objects.get(id=pk)
    crt = Cart.objects.filter(customer=cst)
    context = {'sts':'ord','crt': crt}
    return render(request, 'crm/sub.html', context)

def cartCustomer(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'custfnd':
            val = request.POST.get('cstnm')
            code = request.POST.get('code')
            cst = CustomerProfile.objects.filter(Q(name__icontains=val)|Q(phone__icontains=val))
            context = {'sts': 'custfnd', 'cst': cst,'code':code}
            return render(request, 'cart/task.html', context)
        if action == 'addnew':
            pk = request.POST.get('pk')
            code = request.POST.get('code')
            cat = CustomerDirectory.objects.all()
            context = {'sts': 'addnew', 'cat': cat,'code':code,"pk":pk}
            return render(request, 'cart/task.html', context)
        if action == 'new':
            pk = request.POST.get('pk')
            crtcode = request.POST.get('code')
            categr = request.POST.get('categr')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            date = request.POST.get('date')
            address = request.POST.get('address')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            note = request.POST.get('note')
            know_us = request.POST.get('know_us')
            vip = request.POST.get('vip')
            family = request.POST.get('family')
            cat = CustomerDirectory.objects.get(id=categr)
            code = custmeCode()
            cst=CustomerProfile.objects.create(name=name, direct=cat, addres_0=address, addres_1=address1, addres_2=address2
                                           , note=note, phone=phone, mail=email, know_us=know_us, code=code,
                                           i_date=date,
                                           vip=vip, famly=family)
            cr = CartName.objects.get(id=pk)
            obj, create = Cart.objects.get_or_create(branch=cr, transaction_id=crtcode, status='NEW')
            obj.customer = cst
            obj.save()
            return HttpResponse('done', status=200)

def cartAccount(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'cogs':
            val = request.POST.get('val')
            cr = Cart.objects.get(id=val)
            get_pr = CartProducts.objects.filter(order=cr)
            cost = decimal.Decimal(0)
            month = cr.create_date.month
            print(get_pr)
            for i in get_pr:
                ki = KitchenInventory.objects.filter(name=i.product.name,fnsh=False).first()

                cost += i.quantity * ki.cost

                if i.feat:
                    x = CartSubProducts.objects.filter(suborder=i)
                    for f in x:
                       fp =  RecipeFeatuers.objects.get(id=f.product.id)
                       if fp.raw:
                            avg = Inventory.objects.filter(product=fp.raw,date__month=month).aggregate(amount=Avg('avg_price'))['amount']
                            if avg == 0:
                                month = month - 1
                                avg = Inventory.objects.filter(product=fp.raw, date__month=month).aggregate(
                                    amount=Avg('avg_price'))['amount']
                            cost += f.quantity * avg
                       if fp.ingre:
                            avg = KitchenInventory.objects.filter(ingred=fp.ingre,date__month=month).aggregate(amount=Avg('cost'))['amount']
                            if avg == 0:
                                month = month - 1
                                avg = KitchenInventory.objects.filter(ingred=fp.ingre,date__month=month).aggregate(amount=Avg('cost'))['amount']
                            cost += f.quantity * avg
                al = AccountLedger.objects.filter(created__month=month)
                if not al :
                    month = month - 1
                    al = AccountLedger.objects.filter(created__month=month)
            context = {'sts': 'cogs', 'cr': cr,'cost':cost,'al':al}
            return render(request, 'account/ledg.html', context)
        if action == 'vrbl':
            val = request.POST.get('val')
            vrb = request.POST.get('vrb')
            cr = Cart.objects.get(id=val)
            al = AccountLedger.objects.get(id=vrb)
            month = cr.create_date.month
            tot = KitchenInventory.objects.filter(date__month=month).aggregate(amount=Sum('q_in'))[
                'amount']
            if tot == 0:
                month = month - 1
                tot = KitchenInventory.objects.filter( date__month=month).aggregate(
                    amount=Sum('q_in'))['amount']

            varib = round(al.amount/tot,2)
            context = {'sts': 'vrbl', 'cr': cr,'varib':varib}
            return render(request, 'account/ledg.html', context)
        if action == 'fixd':
            val = request.POST.get('val')
            vrb = request.POST.get('fix')
            cr = Cart.objects.get(id=val)
            al = AccountLedger.objects.get(id=vrb)
            month = cr.create_date.month
            tot = KitchenInventory.objects.filter(date__month=month).aggregate(amount=Sum('q_in'))[
                'amount']
            if tot == 0:
                month = month - 1
                tot = KitchenInventory.objects.filter( date__month=month).aggregate(
                    amount=Sum('q_in'))['amount']

            fixed = round(al.amount/tot,2)
            context = {'sts': 'fixd', 'cr': cr,'fixed':fixed}
            return render(request, 'account/ledg.html', context)

    cr = Cart.objects.filter(status='PAID')
    context = {'sts': 'invs', 'cr': cr}
    return render(request, 'account/ledg.html', context)

def businesPrint(request,pk):
    order = Cart.objects.get(transaction_id=pk)
    if order.status == 'NEW':
            order.status = 'PAID'
            order.save()
    data = CartProducts.objects.filter(order=order)
    data = {
        'order': order,
        'data': data,
    }
    response = render_to_pdf('paper/bcart.html', data)
    filename = "{0}_.pdf".format(order.invoice)
    """
    Tell browser to view inline (default)
    """
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        """
        Tells browser to initiate download
        """
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response

def cartPrint(request,pk):
    order = Cart.objects.get(id=pk)
    # if order.status == 'NEW':
    #         order.status = 'PAID'
    #         order.save()
    data = CartProducts.objects.filter(order=order)
    data = {
        'order': order,
        'data': data,
    }
    response = render_to_pdf('paper/cart.html', data)
    filename = "{0}_.pdf".format(order.invoice)
    """
    Tell browser to view inline (default)
    """
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        """
        Tells browser to initiate download
        """
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response


def posbackUp(request):

    if request.POST:
        action = request.POST.get('action')
        response = HttpResponse(content_type='text/csv')

        print(action)
        if action == '1':
            response['Content-Disposition'] = 'attachment; filename="POS_name.csv"'
            writer = csv.writer(response)
            writer.writerow(['name', 'pwd', 'b_pwd','flat', 'prcnt', 'profile','task','inv','online'])
            acc = CartName.objects.all()
            for i in acc:
                writer.writerow([i.name, i.pwd, i.b_pwd,i.flat, i.prcnt, i.pricing.point,i.task, i.inv, i.online])
            return response
        if action == '2':
            response['Content-Disposition'] = 'attachment; filename="POS_INV.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                writer = csv.writer(response)
                writer.writerow(['POS', 'recipe', 'feat','profile','qty','cost','status','date'])
                acc = CartInv.objects.filter(date__month__gte=start,date__month__lte=end)
                for i in acc:
                    writer.writerow([i.cart.name, i.recipe.name, i.feat.id,i.pricing.profil.point
                                        ,i.qty,i.cost,i.status,i.date])
                return response
            writer = csv.writer(response)
            writer.writerow(['POS', 'recipe', 'feat','profile','qty','cost','status','date'])
            acc = CartInv.objects.all()
            for i in acc:
                writer.writerow([i.cart.name, i.recipe.name, i.feat.id,i.pricing.profil.point
                                        ,i.qty,i.cost,i.status,i.date])
            return response
        if action == '3':
            response['Content-Disposition'] = 'attachment; filename="POS_cash.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                writer = csv.writer(response)
                writer.writerow(['pos', 'start', 'amt_in','amt_out', 'close','t_strt', 't_end','date'])
                acc = CartCash.objects.filter(date__month__gte=start,date__month__lte=end)
                for i in acc:
                    writer.writerow([i.cart.name, i.start, i.amt_in,i.amt_out,i.close,i.t_strt,i.t_end,i.date])
                return response
            writer = csv.writer(response)
            writer.writerow(['pos', 'start', 'amt_in','amt_out', 'close','t_strt', 't_end','date'])
            acc = CartCash.objects.all()
            for i in acc:
                writer.writerow([i.cart.name, i.start, i.amt_in,i.amt_out,i.close,i.t_strt,i.t_end,i.date])
            return response
        if action == '4':
            response['Content-Disposition'] = 'attachment; filename="POS.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = Cart.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = Cart.objects.all()
            writer = csv.writer(response)
            writer.writerow(['name', 'invoice', 'POS','cost', 'customer', 'sub_total','service','delivery'
                                    ,'tax_amount','total','note','discount','transaction_id','online','status','create_date'])
            for i in acc:
                writer.writerow([i.name, i.invoice, i.branch.name,i.customer.name,i.sub_total,i.service, i.delivery, i.tax_amount
                                 ,i.total,i.note,i.discount, i.transaction_id, i.online, i.status, i.create_date])
            return response
        if action == '5':
            response['Content-Disposition'] = 'attachment; filename="POS_products.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = CartProducts.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = CartProducts.objects.all()
            writer = csv.writer(response)
            writer.writerow(['order', 'product', 'quantity','price', 'feat', 'status','create_date'])
            for i in acc:
                writer.writerow([i.order.invoice, i.product.name, i.quantity,i.price,i.feat, i.status, i.create_date])
            return response
        if action == '6':
            response['Content-Disposition'] = 'attachment; filename="POS_task.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = POSTask.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = POSTask.objects.all()
            writer = csv.writer(response)
            writer.writerow(['task', 'pos', 'POS','order', 'start_time', 'end_time','duration','status'])
            for i in acc:
                writer.writerow([i.task, i.pos.name, i.order.invoice,i.start_time,i.end_time,i.duration, i.status])
            return response



    context = {'cog': 'cog'}
    return render(request, 'account/backup.html', context)

