import datetime
import decimal
import csv
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.db.models import Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render

from account.models import AccountRequest
# Create your views here.
from inventory.models import *
from inventory.pdfcreator import render_to_pdf


def product_category(request):
    if request.htmx:
        action = request.POST.get('action')
        if action =='cat':
            context = {'sts': 'pcat'}
            return render(request, 'inventory/subadd.html',context)
        if action =='catadd':
            cate = request.POST.get('cate')
            InvCategory.objects.create(cate=cate)
            cat = InvCategory.objects.all()
            context = {'cat': cat,'sts': 'pman'}
            return render(request, 'inventory/subadd.html',context)
        if action =='catrmv':
            cate = request.POST.get('cate')
            InvCategory.objects.get(id=cate).delete()
            cat = InvCategory.objects.all()
            context = {'cat': cat,'sts': 'pman'}
            return render(request, 'inventory/subadd.html',context)
    cat = InvCategory.objects.all()
    context = {'cat': cat}
    return render(request, 'inventory/category.html', context)

def productSupplier(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'sup':
            context = {'sts': 'psup'}
            return render(request, 'inventory/subadd.html', context)
        if action == 'supadd':
            supl = request.POST.get('supl')
            phone = request.POST.get('phone')
            add = request.POST.get('add')
            RawSuppliers.objects.create(name=supl, phone=phone, add=add)
            sup = RawSuppliers.objects.all()

            context = {'sup': sup, 'sts': 'spman'}
            return render(request, 'inventory/subadd.html', context)
        if action == 'catrmv':
            cate = request.POST.get('cate')
            RawSuppliers.objects.get(id=cate).delete()
            cat = RawSuppliers.objects.all()
            context = {'sup': cat, 'sts': 'spman'}
            return render(request, 'inventory/subadd.html', context)
    sup = RawSuppliers.objects.all()
    context = {'sup': sup}
    return render(request, 'inventory/supplier.html', context)
def productCreation(request):
    if request.htmx:
        action = request.POST.get('action')
        if action =='cat':
            context = {'sts': 'cat'}
            return render(request, 'inventory/subadd.html',context)
        if action =='catadd':
            cate = request.POST.get('cate')
            InvCategory.objects.create(cate=cate)
            sup = RawSuppliers.objects.all()
            cat = InvCategory.objects.all()
            context = {'cat': cat,'suplir':sup,'sts': 'man'}
            return render(request, 'inventory/subadd.html',context)
        if action =='sup':
            context = {'sts': 'sup'}
            return render(request, 'inventory/subadd.html',context)
        if action =='supadd':
            supl = request.POST.get('supl')
            phone = request.POST.get('phone')
            add = request.POST.get('add')
            RawSuppliers.objects.create(name=supl,phone=phone,add=add)
            sup = RawSuppliers.objects.all()
            cat = InvCategory.objects.all()
            context = {'cat': cat,'suplir':sup,'sts': 'man'}
            return render(request, 'inventory/subadd.html',context)
        if action == 'prodadd':
            cate = request.POST.get('cate')
            suply = request.POST.get('suply')
            prod = request.POST.get('prod')
            unt = request.POST.get('unt')
            qty = request.POST.get('qty')
            lvl = request.POST.get('lvl')
            cat = InvCategory.objects.get(id=cate)
            sup = RawSuppliers.objects.get(id=suply)
            rp = RawProducts.objects.create(name=prod,category=cat,unit=unt,qty=qty,min_level=lvl)
            SuppliersProdList.objects.create(name=sup,product=rp)
            context = { 'sts': 'prd'}
            return render(request, 'inventory/subadd.html', context)


    sup = RawSuppliers.objects.all()
    cat = InvCategory.objects.all()
    context = {'cat': cat,'suplir':sup}
    return render(request, 'inventory/add.html', context)
def random_with_N_digits():
    try:
        obj = Inventory.objects.all().order_by('-patch')[0]
        old = obj.patch[3:]
    except:
        old = 0
    new = int(old) +  1
    return  'PO-{0}'.format(new)
def inventory(request):
    if request.htmx:
        action = request.POST.get('action')
        if action =='fltr':
            cate = request.POST.get('cate')
            cat = InvCategory.objects.get(id=cate)
            data = []
            rp = RawProducts.objects.filter(category=cat)
            for i in rp:
                qty = Inventory.objects.filter(product=i, fnsh=False).aggregate(qty=Sum('q_out'))['qty']
                av_Pr = Inventory.objects.filter(product=i, fnsh=False).aggregate(avg_prc=Avg('avg_price'))['avg_prc']
                if qty == None:
                    qty = 0
                if av_Pr == None:
                    av_Pr = 0
                raw = {
                    'name': i.name,
                    'cate': i.category.cate,
                    'qty': round(qty,2),
                    'unit': i.unit,
                    'price': round(av_Pr,2),
                    'id': i.id,
                }
                data.append(raw)
            context = { 'data': data , 'sts':'fltr'}
            return render(request, 'inventory/stk_dlt.html', context)
        if action =='prfltr':
            prdc = request.POST.get('prdc')
            data = []
            rp = RawProducts.objects.filter(name__icontains=prdc)
            if rp:
                for i in rp:
                    qty = Inventory.objects.filter(product=i, fnsh=False).aggregate(qty=Sum('q_out'))['qty']
                    av_Pr = Inventory.objects.filter(product=i, fnsh=False).aggregate(avg_prc=Avg('avg_price'))['avg_prc']
                    if qty == None:
                        qty = 0
                    if av_Pr == None:
                        av_Pr = 0
                    raw = {
                        'name': i.name,
                        'cate': i.category.cate,
                        'qty': round(qty,2),
                        'unit': i.unit,
                        'price': round(av_Pr,2),
                        'id': i.id,
                    }
                    data.append(raw)
            context = { 'data': data , 'sts':'fltr'}
            return render(request, 'inventory/stk_dlt.html', context)
        if action == 'buy':
            val = request.POST.get('val')
            sup = RawSuppliers.objects.all()
            context = {'suplir':sup,'sts':'buy','val':val }
            return render(request, 'inventory/stk_dlt.html', context)
        if action == 'crtsp':
            val = request.POST.get('val')
            context = {'sts':'adsp','val':val }
            return render(request, 'inventory/stk_dlt.html', context)
        if action == 'addsup':
            val = request.POST.get('val')
            supl = request.POST.get('supl')
            phone = request.POST.get('phone')
            add = request.POST.get('add')
            RawSuppliers.objects.create(name=supl, phone=phone, add=add)
            sup = RawSuppliers.objects.all()
            context = {'suplir':sup,'sts':'buy','val':val }
            return render(request, 'inventory/stk_dlt.html', context)
        if action == 'cnl':
            val = request.POST.get('val')
            rp = RawProducts.objects.get(id=val)
            data = []
            qty = Inventory.objects.filter(product=rp, fnsh=False).aggregate(qty=Sum('q_out'))['qty']
            av_Pr = Inventory.objects.filter(product=rp, fnsh=False).aggregate(avg_prc=Avg('avg_price'))['avg_prc']
            if qty == None:
                qty = 0
            if av_Pr == None:
                av_Pr = 0
            raw = {
                'name': rp.name,
                'cate': rp.category.cate,
                'qty': round(qty,2),
                'unit': rp.unit,
                'price': round(av_Pr,2),
                'id': rp.id,
            }
            data.append(raw)
            context = {'data': data , 'sts':'cnl'}
            return render(request, 'inventory/stk_dlt.html', context)
        if action == 'recd':
            val = request.POST.get('val')
            qty = request.POST.get('qty')
            price = request.POST.get('price')
            extr = request.POST.get('extr')
            suply = request.POST.get('suply')
            rp = RawProducts.objects.get(id=val)
            sup = RawSuppliers.objects.get(id=suply)
            em = EmployeeDetail.objects.get(user=request.user)

            amount = (decimal.Decimal(qty)*decimal.Decimal(price))+decimal.Decimal(extr)
            avg_price =amount/decimal.Decimal(qty)
            patch = random_with_N_digits()
            inv = Inventory.objects.create(entry=em,product=rp,supplier=sup,category=rp.category,q_in=qty,q_out=qty,unt_price=price,
                                     ext_cost=extr,avg_price=avg_price,amount=amount,patch=patch)
            AccountRequest.objects.create(ref=patch,section='INVENTORY',item_id=inv.id,item=rp.name,amount=amount)
            data = []
            qty = Inventory.objects.filter(product=rp, fnsh=False).aggregate(qty=Sum('q_out'))['qty']
            av_Pr = Inventory.objects.filter(product=rp, fnsh=False).aggregate(avg_prc=Avg('avg_price'))['avg_prc']
            if qty == None:
                qty = 0
            if av_Pr == None:
                av_Pr = 0
            raw = {
                'name': rp.name,
                'cate': rp.category.cate,
                'qty': round(qty,2),
                'unit': rp.unit,
                'price': round(av_Pr,2),
                'id': rp.id,
            }
            data.append(raw)
            context = {'data': data, 'sts': 'cnl'}
            return render(request, 'inventory/stk_dlt.html', context)
        if action =='dtls':
            val = request.POST.get('val')
            rp = RawProducts.objects.get(id=val)
            data = Inventory.objects.filter(product=rp)
            context = {'data': data, 'sts': 'dtil','val':val}
            return render(request, 'inventory/stk_dlt.html', context)
        if action =='cler':
            val = request.POST.get('val')

            iv = Inventory.objects.get(id=val)
            em = EmployeeDetail.objects.get(user=request.user)
            Inventory.objects.create(entry=em,product=iv.product,supplier=iv.supplier,category=iv.category,q_in=0.00,q_out=iv.q_out
                                            ,unt_price=0.00,ext_cost=0.00,avg_price=0.00,amount=0.00,patch=iv.patch,fnsh=True,action='STOCK CLEAR')
            data = Inventory.objects.filter(product=iv.product)
            context = {'data': data, 'sts': 'dtil','val':val}
            return render(request, 'inventory/stk_dlt.html', context)
    data =[]
    rp = RawProducts.objects.all()
    for i in rp:
        qty = Inventory.objects.filter(product=i, fnsh=False).aggregate(qty=Sum('q_out'))['qty']
        av_Pr = Inventory.objects.filter(product=i, fnsh=False).aggregate(avg_prc=Avg('avg_price'))['avg_prc']
        if qty == None:
            qty = 0
        if av_Pr == None:
            av_Pr = 0
        raw = {
            'name': i.name,
            'cate': i.category.cate,
            'qty': round(qty,2),
            'unit': i.unit,
            'price': round(av_Pr,2),
            'id': i.id,
        }
        data.append(raw)
    cat = InvCategory.objects.all()
    context = {'cat': cat,'data':data}
    return render(request, 'inventory/stock.html', context)


def inventoryTask(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'po':
            data = InventoryTask.objects.filter(status='PENDING')
            paginator = Paginator(data, 10)
            page = request.POST.get('page')
            fle = InventoryPO.objects.create()
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            context = {'sts':'po','data': users,'fle':fle}
            # return render(request, 'paper/po.html', context)
            return render(request, 'inventory/subreqt.html', context)
        if action == 'polst':
            data = InventoryPO.objects.all().order_by('-date')
            paginator = Paginator(data, 10)
            page = request.POST.get('page')
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            context = {'sts':'polst','data': users}
            # return render(request, 'paper/po.html', context)
            return render(request, 'inventory/subreqt.html', context)
        if action == 'poadd':

            val = request.POST.get('val')
            qty = request.POST.get('qty')
            prd = request.POST.get('prd')
            tsk = request.POST.get('tsk')
            InventoryTask.objects.filter(id=tsk).update(status='ASSIGN')
            fle = InventoryPO.objects.get(id=val)
            g_prod = RawProducts.objects.get(id=prd)
            sub = InventoryPOSub.objects.create(po=fle,product=g_prod,unit=g_prod.unit,qty=qty)
            context = {'sts':'poadd','sub':sub}

            return render(request, 'inventory/subreqt.html', context)
        if action == 'nag':
            data = InventoryTask.objects.filter(status='PENDING')
            paginator = Paginator(data, 10)
            page = request.POST.get('page')

            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            context = {'sts':'po','data': users}
            # return render(request, 'paper/po.html', context)
            return render(request, 'inventory/subreqt.html', context)
        if action == 'buy':
            val = request.POST.get('val')
            InventoryTask.objects.filter(id=val).update(status='FINISH')
    data= InventoryTask.objects.filter(status='PENDING')
    paginator = Paginator(data, 10)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context = { 'data': users}
    # return render(request, 'paper/po.html', context)
    return render(request, 'inventory/request.html', context)


def testpdf(request,pk):
    g_prod = InventoryPO.objects.get(id=pk)
    data = InventoryPOSub.objects.filter(po=g_prod)
    data = {
        'po': g_prod,
        'data': data,

    }
    response = render_to_pdf('paper/po.html', data)
    filename = "{0}_.pdf".format(g_prod.task)
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


def invbackUp(request):

    if request.POST:
        action = request.POST.get('action')
        response = HttpResponse(content_type='text/csv')

        print(action)
        if action == '1':
            response['Content-Disposition'] = 'attachment; filename="category.csv"'
            writer = csv.writer(response)
            writer.writerow(['cate'])
            acc = InvCategory.objects.all()
            for i in acc:
                writer.writerow([i.cate])
            return response

        if action == '2':
            response['Content-Disposition'] = 'attachment; filename="POS.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = RawProducts.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = RawProducts.objects.all()
            writer = csv.writer(response)
            writer.writerow(['name', 'unit', 'qty','min_level'])
            for i in acc:
                writer.writerow([i.name, i.unit, i.qty,i.min_level])
            return response
        if action == '3':
            response['Content-Disposition'] = 'attachment; filename="supplier.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = RawSuppliers.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = RawSuppliers.objects.all()
            writer = csv.writer(response)
            writer.writerow(['name', 'phone', 'add','delivery', 'pym', 'date'])
            for i in acc:
                writer.writerow([i.name, i.phone, i.add,i.delivery,i.pym, i.date])
            return response
        if action == '4':
            response['Content-Disposition'] = 'attachment; filename="POS_task.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = InventoryTask.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = InventoryTask.objects.all()
            writer = csv.writer(response)
            writer.writerow(['task', 'product', 'msg','status', 'date'])
            for i in acc:
                writer.writerow([i.task, i.product.name, i.msg,i.status,i.date])
            return response
        if action == '5':
            response['Content-Disposition'] = 'attachment; filename="POS_task.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = Inventory.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = Inventory.objects.all()
            writer = csv.writer(response)
            writer.writerow(['product', 'supplier', 'patch','q_in', 'q_out', 'unt_price', 'ext_cost','avg_price'
                                , 'amount', 'fnsh','date'])
            for i in acc:
                writer.writerow([i.product.name, i.supplier.name, i.patch,i.q_in,i.q_out,
                                 i.unt_price, i.ext_cost,i.avg_price,i.amount,i.fnsh,i.date])
            return response
        if action == '6':
            response['Content-Disposition'] = 'attachment; filename="POS_task.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = InventoryPO.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = InventoryPO.objects.all()
            writer = csv.writer(response)
            writer.writerow(['task', 'status', 'date'])
            for i in acc:
                writer.writerow([i.task, i.status, i.date])
            return response
        if action == '7':
            response['Content-Disposition'] = 'attachment; filename="POS_task.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = InventoryPOSub.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = InventoryPOSub.objects.all()
            writer = csv.writer(response)
            writer.writerow(['po', 'product', 'unit', 'qty'])
            for i in acc:
                writer.writerow([i.po.task, i.product.name, i.unit, i.qty])
            return response



    context = {'cog': 'cog'}
    return render(request, 'account/backup.html', context)