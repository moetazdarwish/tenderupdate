import decimal
from decimal import Decimal
from django.contrib.auth.models import Group, User
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
import csv
from account.models import AccountRequest
from employee.forms import CreateUser
from employee.models import *


def create_Employee(request):
    if request.htmx:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        salary = request.POST.get('salary')
        code = request.POST.get('code')
        username = request.POST.get('username')
        password = request.POST.get('password')
        grps = request.POST.getlist('groups')
        data = {
            'username': username,
            'password1': password,
            'password2': password,
        }
        form = CreateUser(data)

        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            EmployeeDetail.objects.create(user=user,name=name,phone=phone,salary=salary,
            urname=username,pwd=password,emp_num=code)
            for i in grps:
                groups = Group.objects.get(name=i)
                groups.user_set.add(user)
            context = {'name':name,'phone':phone,'salary':salary,
                       'code':code,'username':username,'password':password,'grps':grps }
            return render(request, 'employee/succes.html', context)
        else:
            groups = Group.objects.exclude(name='admin')
            context = {'form':form.errors,'groups':groups}
            return render(request, 'employee/error.html', context)

    groups = Group.objects.exclude(name='admin')
    context={'groups':groups}
    return render(request, 'employee/add.html',context)

def list_Employee(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'detl':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            context = {'empy': get,'sts':'edt','val':myVal}
            return render(request, 'employee/lstedit.html', context)
        if action == 'edit':
            myVal = request.POST.get('myVal')
            code = request.POST.get('code')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            urnam = request.POST.get('urnam')
            pwd = request.POST.get('pwd')
            salary = request.POST.get('salary')
            get = EmployeeDetail.objects.get(id=myVal)
            get.name=name
            get.urname=urnam
            get.pwd=pwd
            get.phone=phone
            get.salary=salary
            get.emp_num=code
            get.save()
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/lstedit.html', context)

        if action == 'inf':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/lstedit.html', context)
        if action == 'grpupt':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            grps = request.POST.getlist('groups')
            get.user.groups.clear()
            for i in grps:
                groups = Group.objects.get(name=i)
                groups.user_set.add(get.user)
            context = {'empy': get, 'sts': 'inf', 'val': myVal}
            return render(request, 'employee/lstedit.html', context)
        if action == 'prm':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            allgroups = Group.objects.exclude(name='admin')
            data = []
            for i in allgroups:
                if get.user.groups.filter(name=i.name).exclude(name='admin').exists():

                    dlt={'id':i.id,'name':i.name,'stat':True}
                else:

                    dlt = {'id': i.id, 'name': i.name, 'stat': False}
                data.append(dlt)
            context = {'groups': data,'nme':get, 'sts': 'grp','val':myVal}
            return render(request, 'employee/lstedit.html', context)
        if action == 'dlt':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            User.objects.get(id= get.user.id).delete()
            get.delete()
            empy = EmployeeDetail.objects.filter(owner=False)
            context = {'empy': empy}
            return render(request, 'employee/dlt.html', context)
    empy=EmployeeDetail.objects.filter(owner=False)
    context = {'empy':empy}
    return render(request, 'employee/list.html', context)
def salary_employee(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'inf':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'detl':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            context = {'empy': get,'sts':'sal','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'bouns':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            context = {'empy': get,'sts':'buns','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'dedct':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            context = {'empy': get,'sts':'ded','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'adv':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            context = {'empy': get,'sts':'adv','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'vtn':
            myVal = request.POST.get('myVal')
            get = EmployeeDetail.objects.get(id=myVal)
            context = {'empy': get,'sts':'vtn','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'edit':
            Today = datetime.today().date()
            myVal = request.POST.get('myVal')
            slry = request.POST.get('nw_slry')
            descp = request.POST.get('ds_slry')
            hr= request.user
            get = EmployeeDetail.objects.get(id=myVal)
            EmpolyRequest.objects.create(name=get,request_by=hr,date=Today,decription=descp,action='SALARY',
                                         status='PENDING',amount=slry)
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'bns':
            Today = datetime.today().date()
            myVal = request.POST.get('myVal')
            slry = request.POST.get('nw_slry')
            descp = request.POST.get('ds_slry')
            hr= request.user
            get = EmployeeDetail.objects.get(id=myVal)
            EmpolyRequest.objects.create(name=get,request_by=hr,date=Today,decription=descp,action='BONUS',
                                         status='PENDING',amount=slry)
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'rqadv':
            Today = datetime.today().date()
            myVal = request.POST.get('myVal')
            slry = request.POST.get('nw_slry')
            descp = request.POST.get('ds_slry')
            hr= request.user
            get = EmployeeDetail.objects.get(id=myVal)
            EmpolyRequest.objects.create(name=get,request_by=hr,date=Today,decription=descp,action='ADVANCE',
                                         status='PENDING',amount=slry)
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'vcat':
            Today = datetime.today().date()
            myVal = request.POST.get('myVal')
            decrp = request.POST.get('decrp')
            f_date = request.POST.get('f_date')
            t_date = request.POST.get('t_date')
            hr= request.user
            get = EmployeeDetail.objects.get(id=myVal)
            EmpolyRequest.objects.create(name=get,request_by=hr,date=Today,d_from=f_date,d_to=t_date,vctn=True,decription=decrp,action='VACATION',
                                         status='PENDING')
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/sal.html', context)
        if action == 'addded':
            Today = datetime.today().date()
            myVal = request.POST.get('myVal')
            slry = request.POST.get('nw_slry')
            descp = request.POST.get('ds_slry')
            hr= request.user
            get = EmployeeDetail.objects.get(id=myVal)
            EmpolyRequest.objects.create(name=get,request_by=hr,date=Today,decription=descp,action='DEDUCTION',
                                         status='CONFIRMED',amount=slry)
            emp ,creat = EmpolySalary.objects.get_or_create(name=get,date__month=Today.month)
            emp.salary=get.salary
            emp.deducte= emp.deducte + decimal.Decimal(slry)
            emp.date=Today
            emp.save()
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/sal.html', context)
    empy = EmployeeDetail.objects.filter(owner=False)
    context = {'empy': empy}
    return render(request, 'employee/salary.html', context)
def ticket_List(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'inf':
            myVal = request.POST.get('myVal')
            get = EmpolyRequest.objects.get(id=myVal)
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/tickdtl.html', context)
        if action == 'acc':
            myVal = request.POST.get('myVal')
            get = EmpolyRequest.objects.get(id=myVal)
            get.status = 'CONFIRMED'
            get.save(update_fields=['status'])
            Today = datetime.today().date()
            if get.vctn:
                for single_date in daterange(get.d_from, get.d_to):
                    EmpolyAttendence.objects.create(name=get.name,date=single_date,action='VACATION')

                context = {'empy': get, 'sts': 'inf', 'val': myVal}
                return render(request, 'employee/tickdtl.html', context)
            if get.action == 'BONUS':
                emp, creat = EmpolySalary.objects.get_or_create(name=get.name, date__month=Today.month)
                emp.bonus = emp.bonus + get.amount
                emp.date = Today
                emp.save()

                context = {'empy': get,'sts':'inf','val':myVal}
                return render(request, 'employee/tickdtl.html', context)
            if get.action == 'ADVANCE':
                emp, creat = EmpolySalary.objects.get_or_create(name=get.name, date__month=Today.month)
                emp.sal_adv = emp.sal_adv + get.amount
                emp.date = Today
                emp.save()

                context = {'empy': get,'sts':'inf','val':myVal}
                return render(request, 'employee/tickdtl.html', context)
            if get.action == 'SALARY':
                em = EmployeeDetail.objects.get(id=get.name.id)
                em.salary = get.amount
                em.save(update_fields=['salary'])
                context = {'empy': get,'sts':'inf','val':myVal}
                return render(request, 'employee/tickdtl.html', context)
        if action == 'decl':
            myVal = request.POST.get('myVal')
            get = EmpolyRequest.objects.get(id=myVal)
            get.status = 'REJECT'
            get.save(update_fields=['status'])
            if get.action == 'DEDUCTION':
                emp, creat = EmpolySalary.objects.get_or_create(name=get.name, date__month=Today.month)
                emp.deducte = (emp.deducte + get.amount)*-1
                emp.date = Today
                emp.save()

                context = {'empy': get,'sts':'inf','val':myVal}
                return render(request, 'employee/tickdtl.html', context)
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/tickdtl.html', context)
    empy = EmpolyRequest.objects.exclude(status='PENDING').order_by('-create')
    context = {'empy': empy}
    return render(request, 'employee/ticket_lst.html', context)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
def ticket_employee(request):
    if request.htmx:
        action = request.POST.get('action')
        Today = datetime.today().date()
        if action == 'inf':
            myVal = request.POST.get('myVal')
            get = EmpolyRequest.objects.get(id=myVal)
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/tickdtl.html', context)
        if action == 'acc':
            myVal = request.POST.get('myVal')
            get = EmpolyRequest.objects.get(id=myVal)
            get.status = 'CONFIRMED'
            get.save(update_fields=['status'])
            if get.vctn:
                for single_date in daterange(get.d_from, get.d_to):
                    EmpolyAttendence.objects.create(name=get.name,date=single_date,action='VACATION')

                context = {'empy': get, 'sts': 'inf', 'val': myVal}
                return render(request, 'employee/tickdtl.html', context)
            if get.action == 'BONUS':

                emp, creat = EmpolySalary.objects.get_or_create(name=get.name, date__month=Today.month)
                emp.bonus = Decimal(emp.bonus) + Decimal(get.amount)
                emp.date = Today
                emp.save()

                context = {'empy': get,'sts':'inf','val':myVal}
                return render(request, 'employee/tickdtl.html', context)
            if get.action == 'ADVANCE':
                emp, creat = EmpolySalary.objects.get_or_create(name=get.name, date__month=Today.month)
                emp.sal_adv = Decimal(emp.sal_adv) + Decimal(get.amount)
                emp.date = Today
                emp.save()

                context = {'empy': get,'sts':'inf','val':myVal}
                return render(request, 'employee/tickdtl.html', context)
            if get.action == 'SALARY':
                em = EmployeeDetail.objects.get(id=get.name.id)
                em.salary = get.amount
                em.save(update_fields=['salary'])
                context = {'empy': get,'sts':'inf','val':myVal}
                return render(request, 'employee/tickdtl.html', context)
        if action == 'decl':
            myVal = request.POST.get('myVal')
            get = EmpolyRequest.objects.get(id=myVal)
            get.status = 'REJECT'
            get.save(update_fields=['status'])
            if get.action == 'DEDUCTION':
                emp, creat = EmpolySalary.objects.get_or_create(name=get.name, date__month=Today.month)
                emp.deducte = (Decimal(emp.deducte) + Decimal(get.amount)) * -1
                emp.date = Today
                emp.save()
                context = {'empy': get,'sts':'inf','val':myVal}
                return render(request, 'employee/tickdtl.html', context)
            context = {'empy': get,'sts':'inf','val':myVal}
            return render(request, 'employee/tickdtl.html', context)
    empy = EmpolyRequest.objects.filter(status='PENDING').order_by('-create')
    context = {'empy': empy}
    return render(request, 'employee/tickets.html', context)

def attendence_employee(request):
    today = datetime.today().date()
    totime = datetime.today().time()
    if request.htmx:
        action = request.POST.get('action')
        if action == 'chk':
            key = request.POST.get('emp_id')
            empy=EmployeeDetail.objects.filter(Q(name__icontains=key) | Q(emp_num__icontains=key))
            context = {'empy': empy,'sts':'nme'}
            return render(request, 'employee/attdtl.html', context)
        if action == 'IN':
            key = request.POST.get('emp_id')
            empy=EmployeeDetail.objects.filter(Q(name__icontains=key) | Q(emp_num__icontains=key))
            if empy:
                EmpolyAttendence.objects.create(name=empy[0],date=today,in_time=totime)
                context = {'empy': empy ,'sts':'new'}
                return render(request, 'employee/attdtl.html', context)
            context = {'empy': '', 'sts': 'error'}
            return render(request, 'employee/attdtl.html', context)
        if action == 'OUT':
            key = request.POST.get('emp_id')
            empy=EmployeeDetail.objects.filter(Q(name__icontains=key) | Q(emp_num__icontains=key))
            if empy:
                tt =EmpolyAttendence.objects.filter(name=empy[0],date=today)
                if tt:
                    tt[0].out_time = totime
                    tt[0].duration = datetime.combine(today,totime) - datetime.combine(today,tt[0].in_time)
                    tt[0].save()
                context = {'empy': empy ,'sts':'new'}
                return render(request, 'employee/attdtl.html', context)
            context = {'empy': '', 'sts': 'error'}
            return render(request, 'employee/attdtl.html', context)
    context = {'empy': '','today':today,'totime':totime}
    return render(request, 'employee/attendence.html', context)
def user_attendence(request):
    today = datetime.today().date()
    totime = datetime.today().time()
    if request.htmx:
        action = request.POST.get('action')
        if action == 'chk':
            key = request.POST.get('emp_id')
            empy=EmployeeDetail.objects.filter(Q(name__icontains=key) | Q(emp_num__icontains=key))
            context = {'empy': empy,'sts':'nme'}
            return render(request, 'employee/attdtl.html', context)
        if action == 'IN':
            key = request.POST.get('emp_id')
            empy=EmployeeDetail.objects.filter(Q(name__icontains=key) | Q(emp_num__icontains=key))
            if empy:
                EmpolyAttendence.objects.create(name=empy[0],date=today,in_time=totime)
                context = {'empy': empy ,'sts':'new'}
                return render(request, 'employee/attdtl.html', context)
            context = {'empy': '', 'sts': 'error'}
            return render(request, 'employee/attdtl.html', context)
        if action == 'OUT':
            key = request.POST.get('emp_id')
            empy=EmployeeDetail.objects.filter(Q(name__icontains=key) | Q(emp_num__icontains=key))
            if empy:
                tt =EmpolyAttendence.objects.filter(name=empy[0],date=today)
                if tt:
                    tt[0].out_time = totime
                    tt[0].duration = datetime.combine(today,totime) - datetime.combine(today,tt[0].in_time)
                    tt[0].save()
                context = {'empy': empy ,'sts':'new'}
                return render(request, 'employee/attdtl.html', context)
            context = {'empy': '', 'sts': 'error'}
            return render(request, 'employee/attdtl.html', context)
    context = {'empy': '','today':today,'totime':totime}
    return render(request, 'employee/genr_attendence.html', context)


def attendenceList(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'get':
            key = request.POST.get('emp_id')
            dte = request.POST.get('mnth')
            empy=EmployeeDetail.objects.filter(Q(name__icontains=key) | Q(emp_num__icontains=key))
            if empy:
                tt = EmpolyAttendence.objects.filter(name=empy[0],date__month=dte)
            context = {'empy': tt,'sts':'nme'}
            return render(request, 'employee/attlst.html', context)
    today = datetime.today().date()
    month = today.month
    tt = EmpolyAttendence.objects.filter(date__month=month)
    context = {'empy': tt}
    return render(request, 'employee/emply_attendce.html', context)


def createAdvance(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'emply':
            empy = EmployeeDetail.objects.all()
            context = {'sts':'emply','empy': empy}
            return render(request, 'employee/sub.html', context)
        if action == 'lstslr':
            empy = EmployeeDetail.objects.all()
            context = {'sts':'lstslr','empy': empy}
            return render(request, 'employee/sub.html', context)
        if action == 'slary':
            slar = EmpolySalary.objects.all().order_by('-date')
            context = {'sts':'slary','slar': slar}
            return render(request, 'employee/sub.html', context)
        if action == 'adv':
            emp = request.POST.get('emp')
            empy = EmployeeDetail.objects.get(id=emp)
            context = {'sts':'adv','empy': empy}
            return render(request, 'employee/sub.html', context)
        if action == 'sldetl':
            emp = request.POST.get('emp')
            empy = EmployeeDetail.objects.get(id=emp)
            context = {'sts':'sldetl','empy': empy}
            return render(request, 'employee/sub.html', context)
        if action == 'detail':
            mnth = request.POST.get('mnth')
            print(mnth)
            val = request.POST.get('val')
            empy = EmployeeDetail.objects.get(id=val)
            es ,crt = EmpolySalary.objects.get_or_create(name=empy,date__month=mnth)
            adv = EmpolyAdvance.objects.filter(name=empy,status='PENDING')

            context = {'sts':'detail','empy': empy,'es':es,'adv':adv}
            return render(request, 'employee/sub.html', context)
        if action == 'adslry':
            amut = request.POST.get('amut')

            g_adv = request.POST.get('adv')
            g_es = request.POST.get('es')
            today = datetime.today().date()
            es = EmpolySalary.objects.get(id=g_es)
            es.salary = es.name.salary
            es.date = today
            es.sal_adv = amut
            es.total = Decimal(es.salary) + Decimal(es.bonus) - Decimal(es.deducte) - Decimal(es.sal_adv)
            es.save()
            try:
                adv = EmpolyAdvance.objects.get(id=g_adv)
                g_l = AdvanceAcc.objects.filter(advnce=adv).aggregate(amount=Sum('install'))['amount']
                if not g_l:
                    g_l = 0
                adv.Remaining = Decimal(adv.amount) - Decimal(g_l) - Decimal(amut)
                adv.save(update_field=['Remaining'])

                AdvanceAcc.objects.create(advnce=adv,date=today,install=amut)
            except:
                pass
            patch = 'SLR-{0}'.format(es.id)
            txt = 'SALARY  For:  {0}'.format(es.name.name)
            AccountRequest.objects.create(ref=patch, section='HR', item_id=es.id, item=txt, amount=es.total)
            slar = EmpolySalary.objects.all().order_by('-date')
            context = {'sts': 'slary', 'slar': slar}
            return render(request, 'employee/sub.html', context)

        if action == 'add':
            emp = request.POST.get('empy')
            amt = request.POST.get('amt')
            mnth = request.POST.get('mnth')

            today = datetime.today().date()
            empy = EmployeeDetail.objects.get(id=emp)
            get_emp,crt = EmpolyAdvance.objects.get_or_create(name=empy,status='PENDING')
            get_emp.date=today
            get_emp.amount= Decimal(get_emp.amount)+Decimal(amt)

            get_emp.period= Decimal(get_emp.period)+Decimal(mnth)
            tot_inst = get_emp.amount/get_emp.period
            get_emp.install = tot_inst
            get_emp.save()

            patch = 'HR-{0}'.format(get_emp.id)
            txt = 'SALARY ADVANCE For {0}'.format(empy.name)
            AccountRequest.objects.create(ref=patch,section='HR',item_id=get_emp.id,item=txt,amount=amt)


    epad = EmpolyAdvance.objects.all().order_by('-date')
    context = {'epad': epad}
    return render(request, 'employee/salr_acc.html', context)


def kitbackUp(request):

    if request.POST:
        action = request.POST.get('action')
        response = HttpResponse(content_type='text/csv')
        if action == '1':
            response['Content-Disposition'] = 'attachment; filename="EmployeeDetail.csv"'
            acc = EmployeeDetail.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '2':
            response['Content-Disposition'] = 'attachment; filename="EmpolyAttendence.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = EmpolyAttendence.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = EmpolyAttendence.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '3':
            response['Content-Disposition'] = 'attachment; filename="EmpolySalary.csv"'
            acc = EmpolySalary.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response

        if action == '4':
            response['Content-Disposition'] = 'attachment; filename="EmpolyRequest.csv"'
            acc = EmpolyRequest.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '5':
            response['Content-Disposition'] = 'attachment; filename="EmpolyAdvance.csv"'
            acc = EmpolyAdvance.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '6':
            response['Content-Disposition'] = 'attachment; filename="AdvanceAcc.csv"'
            acc = AdvanceAcc.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response




    context = {'cog': 'cog'}
    return render(request, 'account/backup.html', context)