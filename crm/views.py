from django.http import HttpResponse
from django.shortcuts import render

from crm.models import *
import csv

# Create your views here.

def custmeCode():
    try:
        obj = CustomerProfile.objects.all().order_by('-code')[0]
        old = obj.code[3:]
    except:
        old = 0
    new = int(old) +  1
    return  'CS-{0}'.format(new)
def customerList(request):
    if request.user.is_authenticated:
        if request.htmx:
            action = request.POST.get('action')
            if action == 'addcst':
                cat = CustomerDirectory.objects.all()
                context = {'sts': 'addcst','cat':cat}
                return render(request, 'crm/sub.html', context)
            if action == 'cat':
                context = {'sts': 'cat'}
                return render(request, 'crm/sub.html', context)
            if action == 'catadd':
                cate = request.POST.get('cate')
                CustomerDirectory.objects.create(name=cate)
                cat = CustomerDirectory.objects.all()
                context = {'sts': 'addcst', 'cat': cat}
                return render(request, 'crm/sub.html', context)
            if action == 'detl':
                Val = request.POST.get('Val')
                cust = CustomerProfile.objects.get(id=Val)
                context = {'sts': 'detl', 'cst': cust}
                return render(request, 'crm/sub.html', context)
            if action == 'del':
                Val = request.POST.get('Val')
                cust = CustomerProfile.objects.get(id=Val).delete()

            if action == 'new':
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
                CustomerProfile.objects.create(name=name,direct=cat,addres_0=address,addres_1=address1,addres_2=address2
                                               ,note=note,phone=phone,mail=email,know_us=know_us,code=code,i_date=date,
                                               vip=vip,famly=family)
    cust = CustomerProfile.objects.all()
    cat = CustomerDirectory.objects.all()
    context = {'cust': cust,'cat': cat}
    return render(request, 'crm/list.html', context)

def customerAdd(request):
    if request.user.is_authenticated:
        if request.htmx:
            action = request.POST.get('action')
            if action == 'cat':
                context = {'sts':'cat'}
                return render(request, 'crm/sub.html', context)
            if action == 'catadd':
                cate = request.POST.get('cate')
                CustomerDirectory.objects.create(name=cate)
    cat = CustomerDirectory.objects.all()
    context = {'cat': cat}
    return render(request, 'crm/list.html', context)

def createDiscount(request):
    if request.user.is_authenticated:
        if request.htmx:
            action = request.POST.get('action')
            if action == 'add':
                nme = request.POST.get('nme')
                cat = request.POST.get('cat')
                flt = request.POST.get('flt')
                percent = request.POST.get('percent')
                new = request.POST.get('new')
                vip = request.POST.get('vip')
                fmly = request.POST.get('fmly')
                site = request.POST.get('site')
                categr = request.POST.get('categr')
                cag = CustomerDirectory.objects.get(id=cat)
                CustomerDiscount.objects.create(name=nme,direct=cag,vip=vip,famly=fmly,new=new,
                        all=categr,site=site,discount=percent,flat=flt)
            if action == 'disc':
                cag = CustomerDirectory.objects.all()
                context = { 'sts':'disc','cag': cag}
                return render(request, 'crm/sub.html', context)
            if action == 'delt':
                val = request.POST.get('val')
                CustomerDiscount.objects.get(id=val).delete()

    dis = CustomerDiscount.objects.all()
    context = {'dis': dis }
    return render(request, 'crm/discount.html', context)

def crmbackUp(request):

    if request.POST:
        action = request.POST.get('action')
        response = HttpResponse(content_type='text/csv')
        if action == '1':
            response['Content-Disposition'] = 'attachment; filename="customer.csv"'
            writer = csv.writer(response)
            writer.writerow(['name', 'uuid', 'addres_0','addres_1', 'addres_2', 'note','phone','mail','know_us'
                             ,'code','i_date','vip','famly','date'])
            acc = CustomerProfile.objects.all()
            for i in acc:
                writer.writerow([i.name, i.uuid, i.addres_0,i.addres_1, i.addres_2, i.note,i.phone, i.mail, i.know_us
                                 ,i.code,i.i_date, i.vip, i.famly, i.date])
            return response
        if action == '2':
            response['Content-Disposition'] = 'attachment; filename="discount.csv"'
            writer = csv.writer(response)
            writer.writerow(['name', 'code', 'vip','famly','new','all','site','area_ds',
                             'discount','flat','date'])
            acc = CustomerDiscount.objects.all()
            for i in acc:
                writer.writerow([i.name, i.code, i.vip,i.famly
                                        ,i.new,i.all,i.site,i.area_ds,i.discount,i.flat,i.date])
            return response
    context = {'cog': 'cog'}
    return render(request, 'account/backup.html', context)