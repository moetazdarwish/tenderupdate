import decimal
from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from account.models import *
from inventory.pdfcreator import render_to_pdf
import csv

# Create your views here.


def creatAccount(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'delt':
            val = request.POST.get('val')
            AccountKeys.objects.get(id=val).delete()
        if action == 'getkey':
            key = request.POST.get('key')
            ak = AccountKeys.objects.filter(code__icontains=key)
            context = {'sts': 'dred', 'ak': ak}
            return render(request, 'account/sub.html', context)
        if action == 'edred':
            key = request.POST.get('key')
            val = request.POST.get('val')
            ak = AccountKeys.objects.filter(code__icontains=key)
            context = {'sts': 'dbedt', 'ak': ak,'val':val}
            return render(request, 'account/sub.html', context)
        if action == 'edrec':
            key = request.POST.get('key')
            val = request.POST.get('val')
            ak = AccountKeys.objects.filter(code__icontains=key)
            print(ak)
            context = {'sts': 'ecred', 'ak': ak,'val':val}
            return render(request, 'account/sub.html', context)
        if action == 'cgetkey':
            key = request.POST.get('key')
            ak = AccountKeys.objects.filter(code__icontains=key)
            context = {'sts': 'cred', 'ak': ak}
            return render(request, 'account/sub.html', context)
        if action == 'key':
            ap = AccountParent.objects.all()
            context = {'sts':'key','ap': ap}
            return render(request, 'account/sub.html', context)
        if action == 'add':
            name = request.POST.get('name')
            code = request.POST.get('code')
            prnt = request.POST.get('prnt')
            ap = AccountParent.objects.get(id=prnt)
            cd = '{0}{1}'.format(ap.code,code)
            AccountKeys.objects.create(name=name,nature=ap,code=cd)

    acc =AccountKeys.objects.all()
    context = {'acc': acc}
    return render(request, 'account/account.html', context)

def journal(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'recd':
            context = {'sts':'recd'}
            return render(request, 'account/sub.html', context)
        if action == 'reccr':
            context = {'sts':'rec'}
            return render(request, 'account/sub.html', context)
        if action == 'new':
            context = {'sts':'new'}
            return render(request, 'account/sub.html', context)
        if action == 'edit':
            val = request.POST.get('val')
            jr = JournalRef.objects.get(id=val)
            context = {'sts':'edit','jr':jr}
            return render(request, 'account/sub.html', context)
        if action == 'dbedit':
            val = request.POST.get('val')
            dkey = request.POST.get('dkey')
            damount = request.POST.get('damount')
            drf = request.POST.get('drf')
            date = datetime.today().date()
            jr = JournalRef.objects.get(id=val)
            ak = AccountKeys.objects.get(code=dkey)
            AccountJournalDebt.objects.create(ref=jr, key=ak, amount=damount, ex_ref=drf, date=date)
            context = {'sts': 'edupd', 'jr': jr}
            return render(request, 'account/sub.html', context)
        if action == 'credit':
            val = request.POST.get('val')
            dkey = request.POST.get('ckey')
            damount = request.POST.get('camount')
            drf = request.POST.get('crf')
            date = datetime.today().date()
            jr = JournalRef.objects.get(id=val)
            ak = AccountKeys.objects.get(code=dkey)
            AccountJournalCredit.objects.create(ref=jr, key=ak, amount=damount, ex_ref=drf, date=date)
            context = {'sts': 'edupd', 'jr': jr}
            return render(request, 'account/sub.html', context)
        if action == 'edred':
            val = request.POST.get('val')

            context = {'sts':'edred','val':val}
            return render(request, 'account/sub.html', context)
        if action == 'edrec':
            val = request.POST.get('val')

            context = {'sts':'edrec','val':val}
            return render(request, 'account/sub.html', context)
        if action == 'add':
            ref = request.POST.get('ref')
            date = request.POST.get('date')
            dec = request.POST.get('dec')
            dkey = request.POST.getlist('dkey')
            damount = request.POST.getlist('damount')
            drf = request.POST.getlist('drf')
            crf = request.POST.getlist('crf')
            ckey = request.POST.getlist('ckey')
            camount = request.POST.getlist('camount')

            if dkey and ckey:
                jr = JournalRef.objects.create(ref=ref,description=dec,e_date=date)
                n = 0
                for i in dkey :
                    ak  = AccountKeys.objects.get(code=i)
                    AccountJournalDebt.objects.create(ref=jr,key=ak,amount=damount[n],ex_ref=drf[n],date=date)
                    n+=1
                m=0
                for i in ckey :
                    ak  = AccountKeys.objects.get(code=i)
                    AccountJournalCredit.objects.create(ref=jr,key=ak,amount=camount[m],ex_ref=crf[m],date=date)
                    m+=1
        if action == 'fdate':
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            jrf = JournalRef.objects.filter(e_date__gte=dat1,e_date__lte=dat2).order_by('-date')
            context = {'sts':'fdate','jrf': jrf}
            return render(request, 'account/sub.html', context)
        if action == 'fref':
            key = request.POST.get('fref')
            jrf = JournalRef.objects.filter(ref__icontains=key).order_by('-date')

            context = {'sts':'fdate','jrf': jrf}
            return render(request, 'account/sub.html', context)

    data = JournalRef.objects.all().order_by('-date')
    paginator = Paginator(data, 15)
    page = request.GET.get('page', 1)
    try:
        jrf = paginator.page(page)
    except PageNotAnInteger:
        jrf = paginator.page(1)
    except EmptyPage:
        jrf = paginator.page(paginator.num_pages)
    context = {'jrf': jrf}
    return render(request, 'account/journal.html', context)

def delete(request):
    return HttpResponse(status=200)

def accRequest(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'selct':
            chek = request.POST.getlist('chek')
            Today = datetime.today().date()
            print(Today)
            arq= AccountRequest.objects.get(id=chek[0])
            ref = arq.ref
            descrip ='{0} : '.format(arq.section)
            amount = 0
            n = 1
            for i in chek:
                aq = AccountRequest.objects.get(id=i)
                aq.status = 'DONE'
                aq.save(update_fields=['status'])
                descrip += '{0} -{1},'.format(n,aq.item)
                amount +=aq.amount
                n+=1
            jr = JournalRef.objects.create(ref=ref, description=descrip, e_date=Today)
            context = {'sts': 'selct','jr':jr,'amount':amount}
            return render(request, 'account/req.html', context)
    data = AccountRequest.objects.filter(status='PENDING').order_by('-date')
    paginator = Paginator(data, 15)
    page = request.GET.get('page', 1)
    try:
        arq = paginator.page(page)
    except PageNotAnInteger:
        arq = paginator.page(1)
    except EmptyPage:
        arq = paginator.page(paginator.num_pages)
    context = {'arq': arq}
    return render(request, 'account/request.html', context)


def ledgers(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'lgkey':
            acc = AccountKeys.objects.all()
            pra = AccountParent.objects.all()
            context = {'sts': 'lgkey','acc':acc,'pra':pra}
            return render(request, 'account/ledg.html', context)
        if action == 'flty':
            flt= request.POST.get('flt')
            pra = AccountParent.objects.get(id=flt)
            acc = AccountKeys.objects.filter(nature=pra)

            context = {'sts': 'flty','acc':acc}
            return render(request, 'account/ledg.html', context)
        if action == 'comb':
            context = {'sts': 'comb'}
            return render(request, 'account/ledg.html', context)
        if action == 'cal':
            mnth= request.POST.get('mnth')
            flt= request.POST.getlist('chek')
            Today = datetime.today().date()
            if flt:
                for i in flt:
                    acc = AccountKeys.objects.get(id=i)
                    debit = AccountJournalDebt.objects.filter(key=acc,date__month=mnth).aggregate(amount=Sum('amount'))['amount']
                    credit = AccountJournalCredit.objects.filter(key=acc,date__month=mnth).aggregate(amount=Sum('amount'))['amount']
                    if debit == None:
                        debit = 0
                    if credit == None:
                        credit = 0
                    amut = debit - credit
                    AccountLedger.objects.create(name=acc.name,key=acc,amount=amut,date=Today)

        if action == 'combi':
            combin= request.POST.get('combin')
            mnth = request.POST.get('mnth')
            flt= request.POST.getlist('chek')
            Today = datetime.today().date()
            amount = decimal.Decimal(0.00)
            if flt:
                for i in flt:
                    acc = AccountKeys.objects.get(id=i)
                    debit = AccountJournalDebt.objects.filter(key=acc,date__month=mnth).aggregate(amount=Sum('amount'))['amount']
                    credit = AccountJournalCredit.objects.filter(key=acc,date__month=mnth).aggregate(amount=Sum('amount'))['amount']
                    if debit == None:
                        debit = 0
                    if credit == None:
                        credit = 0
                    amut = debit - credit
                    amount += amut
                AccountLedger.objects.create(name=combin,amount=amount,date=Today)
        if action == 'delt':
            val= request.POST.get('val')
            AccountLedger.objects.get(id=val).delete()
    data = AccountLedger.objects.all().order_by('-created')
    paginator = Paginator(data, 15)
    page = request.GET.get('page', 1)
    try:
        alg = paginator.page(page)
    except PageNotAnInteger:
        alg = paginator.page(1)
    except EmptyPage:
        alg = paginator.page(paginator.num_pages)
    context = {'alg': alg}
    return render(request, 'account/ledgers.html', context)

def invoices(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'cst':
            csot = request.POST.get('csot')
            vribl = request.POST.get('vribl')
            fxxed = request.POST.get('fxxed')
            rev = request.POST.get('rev')
            ptch = request.POST.get('ptch')
            AccountCOGS.objects.create(patch=ptch,revenue=rev,cost=csot,direct=vribl,indirect=fxxed)
        if action == 'delt':
            val = request.POST.get('val')
            AccountCOGS.objects.get(id=val).delete()

    data = AccountCOGS.objects.all().order_by('-date')
    paginator = Paginator(data, 15)
    page = request.GET.get('page', 1)
    try:
        cog = paginator.page(page)
    except PageNotAnInteger:
        cog = paginator.page(1)
    except EmptyPage:
        cog = paginator.page(paginator.num_pages)
    context = {'cog': cog}
    return render(request, 'account/invoices.html', context)


def requestPrint(request,pk):
    ac = AccountRequest.objects.get(id=pk)
    data = {
        'data': ac,
    }
    response = render_to_pdf('paper/accrec.html', data)
    filename = "{0}_.pdf".format(ac.ref)
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

def backUp(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'btn':
            context = {'sts': 'btn'}
            return render(request, 'account/bacsub.html', context)
        if action == 'allbtn':
            context = {'sts': 'allbtn'}
            return render(request, 'account/bacsub.html', context)
        if action == 'man':
            context = {'sts': 'man'}
            return render(request, 'account/bacsub.html', context)
        if action == 'pos':
            context = {'sts': 'pos'}
            return render(request, 'account/bacsub.html', context)
        if action == 'crm':
            context = {'sts': 'crm'}
            return render(request, 'account/bacsub.html', context)
        if action == 'inv':
            context = {'sts': 'inv'}
            return render(request, 'account/bacsub.html', context)
        if action == 'kit':
            context = {'sts': 'kit'}
            return render(request, 'account/bacsub.html', context)
        if action == 'hr':
            context = {'sts': 'hr'}
            return render(request, 'account/bacsub.html', context)
    if request.POST:
        action = request.POST.get('action')
        response = HttpResponse(content_type='text/csv')

        print(action)
        if action == '1':
            response['Content-Disposition'] = 'attachment; filename="Keys.csv"'
            acc = AccountKeys.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '3':
            response['Content-Disposition'] = 'attachment; filename="Request.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                writer = csv.writer(response)
                writer.writerow(['ref', 'section', 'item','amount','status','date'])
                acc = AccountRequest.objects.filter(date__month__gte=start,date__month__lte=end)
                for i in acc:
                    writer.writerow([i.ref, i.section, i.item,i.amount,i.status,i.date])
                return response
            writer = csv.writer(response)
            writer.writerow(['ref', 'section', 'item','amount','status','date'])
            acc = AccountRequest.objects.all()
            for i in acc:
                writer.writerow([i.ref, i.section, i.item,i.amount,i.status,i.date])
            return response
        if action == '4':
            response['Content-Disposition'] = 'attachment; filename="Ledger.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                writer = csv.writer(response)
                writer.writerow(['name', 'account', 'amount','date'])
                acc = AccountLedger.objects.filter(date__month__gte=start,date__month__lte=end)
                for i in acc:
                    writer.writerow([i.name, i.key.name, i.amount,i.date,i.status,i.date])
                return response
            writer = csv.writer(response)
            writer.writerow(['name', 'account', 'amount','date'])
            acc = AccountLedger.objects.all()
            for i in acc:
                writer.writerow([i.name, i.key.name, i.amount,i.date])
            return response
        if action == '5':
            response['Content-Disposition'] = 'attachment; filename="COGS.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                writer = csv.writer(response)
                writer.writerow(['patch', 'invoice', 'revenue','cost', 'direct', 'revenue','indirect','indirect'])
                acc = AccountCOGS.objects.filter(date__month__gte=start,date__month__lte=end)
                for i in acc:
                    writer.writerow([i.patch, i.invoice, i.revenue,i.cost,i.direct,i.date, i.indirect, i.date])
                return response
            writer = csv.writer(response)
            writer.writerow(['patch', 'invoice', 'revenue','cost', 'invoice', 'direct','indirect','indirect'])
            acc = AccountCOGS.objects.all()
            for i in acc:
                writer.writerow([i.patch, i.invoice, i.revenue,i.cost, i.invoice, i.direct,i.indirect, i.date])
            return response

    context = {'cog': 'cog'}
    return render(request, 'account/backup.html', context)





