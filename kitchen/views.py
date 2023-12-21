import decimal

from django.db.models import Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
# Create your views here.
from inventory.models import Inventory, InventoryTask
from kitchen.models import *
import csv
# ingerdients
def ingInventorylc(ingredient):
    data = []
    for i in ingredient:
        qty = KitchenInventory.objects.filter(ingred=i, fnsh=False).aggregate(qty=Sum('q_out'))['qty']
        av_Pr = KitchenInventory.objects.filter(ingred=i, fnsh=False).aggregate(avg_prc=Avg('cost'))['avg_prc']
        if qty == None:
            qty = 0
        if av_Pr == None:
            av_Pr = 0
        raw = {
            'name': i.name,
            'qty': round(qty, 2),
            'unit': i.unit,
            'price': round(av_Pr, 2),
            'id': i.id,
        }
        data.append(raw)
    return data
def ingredient(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'srch':
            prdc = request.POST.get('prdc')
            g_ing = Ingredients.objects.filter(name__icontains=prdc)
            ing = ingInventorylc(g_ing)
            context = {'ing': ing}
            return render(request, 'kitchen/ingredient.html', context)
        if action =='btn_add':
            context = {'sts': 'btn_add'}
            return render(request, 'kitchen/sub.html', context)
        if action == 'add':
            name = request.POST.get('name')
            qty = request.POST.get('qty')
            descrip = request.POST.get('descrip')
            weight = request.POST.get('weight')
            unit = request.POST.get('unit')
            lvl = request.POST.get('lvl')
            ing = Ingredients.objects.create(name=name,receipt=descrip,quantity=qty,weight=weight,unit=unit,min_level=lvl)
            raw = RawProducts.objects.all()
            context = {'sts': 'prod','val':ing.id,'raw':raw}
            return render(request, 'kitchen/sub.html', context)
        if action =='sub':
            val = request.POST.get('val')
            qty = request.POST.get('qty')
            raw_id = request.POST.get('raw')
            raw = RawProducts.objects.get(id=raw_id)
            ing = Ingredients.objects.get(id=val)
            sub = SubIngredients.objects.create(sub=ing,items=raw,quantity=qty)
            context = {'sts': 'rawsl', 'sub': sub}
            return render(request, 'kitchen/sub.html', context)
        if action == 'rmv':
            val = request.POST.get('val')
            prd = request.POST.get('prd')
            sub = SubIngredients.objects.get(id=val)
            val = sub.sub.id
            sub.delete()
            raw = RawProducts.objects.get(id=prd)
            context = {'sts': 'sbraw', 'raw': raw,'val':val}
            return render(request, 'kitchen/sub.html', context)
        if action == 'rmving':
            val = request.POST.get('val')
            prd = request.POST.get('prd')
            sub = SubIngredients.objects.get(id=val)
            val = sub.sub.id
            sub.delete()
            raw = Ingredients.objects.get(id=prd)
            context = {'sts': 'ingraw', 'raw': raw,'val':val}
            return render(request, 'kitchen/sub.html', context)
        if action == 'pdcat':
            val = request.POST.get('val')
            ing = Ingredients.objects.get(id=val)
            sub = SubIngredients.objects.filter(sub=ing.id,ingre__isnull=True)
            print(sub)
            if sub:

                names_to_exclude = [o.items.id for o in sub]
                data =  RawProducts.objects.exclude(id__in=names_to_exclude)
                print(data)
                context = {'sts': 'pdcat', 'data': data,'sub':sub,'val': val}
                return render(request, 'kitchen/sub.html', context)
            data = RawProducts.objects.all()
            context = {'sts': 'pdcat', 'data': data, 'sub': sub, 'val': val}
            return render(request, 'kitchen/sub.html', context)
        if action == 'ing':
            val = request.POST.get('val')
            ing = Ingredients.objects.get(id=val)
            sub = SubIngredients.objects.filter(sub=ing.id,items__isnull=True)

            if sub:
                names_to_exclude = [o.ingre.id for o in sub]
                data =  Ingredients.objects.exclude(id__in=names_to_exclude)

                context = {'sts': 'ing', 'ingdata': data,'sub':sub,'val': val}
                return render(request, 'kitchen/sub.html', context)
            data = Ingredients.objects.all()
            context = {'sts': 'ing', 'ingdata': data, 'sub': sub, 'val': val}
            return render(request, 'kitchen/sub.html', context)
        if action == 'ingsub':
            val = request.POST.get('val')
            qty = request.POST.get('qty')
            raw_id = request.POST.get('raw')
            raw = Ingredients.objects.get(id=raw_id)
            ing = Ingredients.objects.get(id=val)
            sub = SubIngredients.objects.create(sub=ing, ingre=raw, quantity=qty)
            context = {'sts': 'rawing', 'sub': sub}
            return render(request, 'kitchen/sub.html', context)
        if action == 'info':
            val = request.POST.get('val')
            raw = Ingredients.objects.get(id=val)
            sub = SubIngredients.objects.filter(sub=raw,)
            context = {'sts': 'info', 'sub': sub,'raw':raw}
            return render(request, 'kitchen/sub.html', context)
        if action == 'delete':
            val = request.POST.get('val')
            raw = Ingredients.objects.get(id=val).delete()
            g_ing = Ingredients.objects.all()
            ing = ingInventorylc(g_ing)
            context = {'ing': ing}
            return render(request, 'kitchen/ingredient.html', context)
        if action == 'stock':
            val = request.POST.get('val')
            g_ing = Ingredients.objects.get(id=val)
            ing = KitchenInventory.objects.filter(ingred=g_ing)
            context = {'ing': ing,'sts':'dtil'}
            return render(request, 'kitchen/sub.html', context)
        if action == 'cler':
            val = request.POST.get('val')
            ing = KitchenInventory.objects.get(id=val)
            ing.status='WASTE REQUEST'
            ing.fnsh=True
            ing.save(update_fields=['status','fnsh'])
            ing = KitchenInventory.objects.filter(ingred=ing.ingred)
            context = {'ing': ing,'sts':'clract'}
            return render(request, 'kitchen/sub.html', context)


    g_ing = Ingredients.objects.all()
    ing = ingInventorylc(g_ing)
    context = {'ing': ing}
    return render(request, 'kitchen/ingredient.html', context)

def invtTask(qty,sub,subtsk):
    data = []
    for i in sub:
        if i.items:
            rq_qty = i.quantity * qty
            while rq_qty != 0:
                x = Inventory.objects.filter(product=i.items, fnsh=False).order_by('date').first()

                if x:
                    if x.q_out > rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, raw=x, quantity=rq_qty)
                        x.q_out = x.q_out - rq_qty
                        x.save(update_fields=['q_out'])
                        rq_qty = 0
                        stat = 'Stock Available'
                    elif x.q_out == rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, raw=x, quantity=rq_qty)
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        rq_qty = 0
                        stat = 'Stock Available'
                    elif x.q_out < rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, raw=x, quantity=rq_qty)
                        rq_qty = rq_qty - x.q_out
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        stat = 'Stock Available'

                else:

                    KitchenSubTask.objects.create(job=subtsk, raw=x, quantity=rq_qty)
                    InventoryTask.objects.create( product=i.items, msg='ITEM STOCK FINISH', status='PENDING')
                    stat = 'Purchase Request'
                    rq_qty = 0
            rq_qty = i.quantity * qty
            dlt = {
                'item': i.items.name,
                'type': 'RAW',
                'qty': rq_qty,
                'stats': stat,
            }
            data.append(dlt)
        if i.ingre:
            rq_qty = i.quantity * qty
            while rq_qty != 0:
                x = KitchenInventory.objects.filter(ingred=i.items, fnsh=False).order_by('date').first()
                print(x)
                if x:
                    if x.q_out > rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, ingrd=x, quantity=rq_qty)
                        x.q_out = x.q_out - rq_qty
                        x.save(update_fields=['q_out'])
                        rq_qty = 0
                        stat = 'Stock Available'
                    elif x.q_out == rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, ingrd=x, quantity=rq_qty)
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        rq_qty = 0
                        stat = 'Stock Available'
                    elif x.q_out < rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, ingrd=x, quantity=rq_qty)
                        rq_qty = rq_qty - x.q_out
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        stat = 'Stock Available'
                else:
                    y = KitchenInventory.objects.filter(ingred=i.items,).order_by('date').first()

                    KitchenSubTask.objects.create(job=subtsk, ingrd=y, quantity=rq_qty)
                    kt = kitchenTask.objects.create(  status='PENDING')
                    KitchenJobsAssign.objects.create(task=kt,ingrd=y,descrp='ITEM STOCK FINISH')
                    stat = 'Task Request'
                    rq_qty = 0
            rq_qty = i.quantity * qty
            dlt = {
                'item': i.ingre.name,
                'type': 'Ingredient',
                'qty': rq_qty,
                'stats': stat,

            }
            data.append(dlt)
    return data
def task_kitchen(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'tsk':
            val = request.POST.get('val')
            ing = Ingredients.objects.get(id=val)
            context = {'ing':ing , 'sts':'tsk'}
            return render(request, 'kitchen/subtsk.html', context)
        if action == 'nwtsk':
            val = request.POST.get('val')
            inv = request.POST.get('inv')
            qty = request.POST.get('qty')

            invt = True
            if inv == '2':
                invt = False
            ing = Ingredients.objects.get(id=val)
            tsk = kitchenTask.objects.create(for_sale=invt,status='PENDING')
            qty = decimal.Decimal(qty)

            subtsk = KitchenJobsAssign.objects.create(task=tsk,ingrd=ing,quantity=qty,for_sale=invt)
            sub = SubIngredients.objects.filter(sub=ing)
            data = invtTask(qty,sub,subtsk)
            context = {'sts':'new','patch': tsk.task,'data':data}
            return render(request, 'kitchen/subtsk.html', context)
        if action == 'extsk':
            val = request.POST.get('val')

            tsk = kitchenTask.objects.filter(status='PENDING')
            context = {'sts': 'extsk', 'tsk': tsk,'val':val }
            return render(request, 'kitchen/subtsk.html', context)
        if action == 'addext':
            val = request.POST.get('val')
            tsk = request.POST.get('tsk')
            inv = request.POST.get('inv')
            qty = request.POST.get('qty')

            ing = Ingredients.objects.get(id=val)
            tsk = kitchenTask.objects.get(id=tsk)
            qty = decimal.Decimal(qty)
            invt = True
            if inv =='2':
                invt = False
            subtsk = KitchenJobsAssign.objects.create(task=tsk,ingrd=ing,quantity=qty,for_sale=invt)
            sub = SubIngredients.objects.filter(sub=ing)
            data = invtTask(qty,sub,subtsk)
            context = {'sts':'new','patch': tsk.task,'data':data}
            return render(request, 'kitchen/subtsk.html', context)
        if action == 'chek':
            val = request.POST.get('val')
            ing = Ingredients.objects.get(id=val)
            context = {'sts': 'chek',  'ing': ing}
            return render(request, 'kitchen/subtsk.html', context)
        if action == 'chkrsl':
            val = request.POST.get('val')
            qty = request.POST.get('qty')
            ing = Ingredients.objects.get(id=val)
            data = ingr_Invcheck(ing, int(qty))
            print(data)
            context = {'sts': 'chkrsl', 'data': data, 'val': val}
            return render(request, 'kitchen/subtsk.html', context)

# Recipt

def kitCategory(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'add':
            context = {'sts': 'categ'}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'mnadd':
            context = {'sts': 'mncat'}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'delt':
            val = request.POST.get('val')
            KitCategory.objects.get(id=val).delete()

        if action == 'inpt':
            val = request.POST.get('adcat')

            KitCategory.objects.create(cate=val)
            cat = KitCategory.objects.all()
            context = {'sts': 'getcat','cat':cat}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'mninpt':
            val = request.POST.get('adcat')
            KitCategory.objects.create(cate=val)

    cat = KitCategory.objects.all()
    context = {'sts': 'allcat', 'cat': cat}
    return render(request, 'kitchen/recisub.html', context)


def reciptInventorylc(recipt):
    data = []
    for i in recipt:
        qty = KitchenInventory.objects.filter(name=i, fnsh=False).aggregate(qty=Sum('q_out'))['qty']
        av_Pr = KitchenInventory.objects.filter(name=i, fnsh=False).aggregate(avg_prc=Avg('cost'))['avg_prc']
        if qty == None:
            qty = 0
        if av_Pr == None:
            av_Pr = 0
        raw = {
            'name': i.name,
            'qty': round(qty, 2),
            'unit': i.unit,
            'price': round(av_Pr, 2),
            'id': i.id,
        }
        data.append(raw)
    return data
def reciptls(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'srch':
            prdc = request.POST.get('prdc')
            g_ing = KitchenRecipe.objects.filter(name__icontains=prdc)
            ing = reciptInventorylc(g_ing)
            context = {'ing': ing}
            return render(request, 'kitchen/recipt.html', context)
        if action == 'btn_add':
            cat = KitCategory.objects.all()
            context = {'sts': 'btn_add','cat':cat}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'add':
            name = request.POST.get('name')
            qty = request.POST.get('qty')
            cate = request.POST.get('cat')
            s_descrip = request.POST.get('s_descrip')
            l_descrip = request.POST.get('l_descrip')
            weight = request.POST.get('weight')
            unit = request.POST.get('unit')
            lvl = request.POST.get('lvl')
            photo = request.FILES.get('photo')
            cat = KitCategory.objects.get(id=cate)
            ing = KitchenRecipe.objects.create(name=name,cate=cat, s_descrip=s_descrip,l_descrip=l_descrip,
                                               quantity=qty, weight=weight, unit=unit,
                                             min_level=lvl,photo=photo)
            raw = RawProducts.objects.all()
            context = {'sts': 'prod', 'val': ing.id, 'raw': raw}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'sub':
            val = request.POST.get('val')
            qty = request.POST.get('qty')
            raw_id = request.POST.get('raw')
            raw = RawProducts.objects.get(id=raw_id)
            ing = KitchenRecipe.objects.get(id=val)
            sub = SubKitchenRecipe.objects.create(sub=ing, raw=raw, quantity=qty)
            context = {'sts': 'rawsl', 'sub': sub}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'rmv':
            val = request.POST.get('val')
            prd = request.POST.get('prd')
            sub = SubKitchenRecipe.objects.get(id=val)
            val = sub.sub.id
            sub.delete()
            raw = RawProducts.objects.get(id=prd)
            context = {'sts': 'sbraw', 'raw': raw, 'val': val}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'rmving':
            val = request.POST.get('val')
            prd = request.POST.get('prd')
            sub = SubKitchenRecipe.objects.get(id=val)
            val = sub.sub.id
            sub.delete()
            raw = Ingredients.objects.get(id=prd)
            context = {'sts': 'ingraw', 'raw': raw, 'val': val}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'pdcat':
            val = request.POST.get('val')
            ing = KitchenRecipe.objects.get(id=val)
            sub = SubKitchenRecipe.objects.filter(sub=ing.id, ingredient__isnull=True)
            if sub:
                names_to_exclude = [o.raw.id for o in sub]
                data = RawProducts.objects.exclude(id__in=names_to_exclude)
                context = {'sts': 'pdcat', 'data': data, 'sub': sub, 'val': val}
                return render(request, 'kitchen/recisub.html', context)
            data = RawProducts.objects.all()
            context = {'sts': 'pdcat', 'data': data, 'sub': sub, 'val': val}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'ing':
            val = request.POST.get('val')
            ing = KitchenRecipe.objects.get(id=val)
            sub = SubKitchenRecipe.objects.filter(sub=ing.id, raw__isnull=True)
            if sub:
                names_to_exclude = [o.ingredient.id for o in sub]
                data = Ingredients.objects.exclude(id__in=names_to_exclude)
                context = {'sts': 'ing', 'ingdata': data, 'sub': sub, 'val': val}
                return render(request, 'kitchen/recisub.html', context)
            data = Ingredients.objects.all()
            context = {'sts': 'ing', 'ingdata': data, 'sub': sub, 'val': val}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'ingsub':
            val = request.POST.get('val')
            qty = request.POST.get('qty')
            raw_id = request.POST.get('raw')
            raw = Ingredients.objects.get(id=raw_id)
            ing = KitchenRecipe.objects.get(id=val)
            sub = SubKitchenRecipe.objects.create(sub=ing, ingredient=raw, quantity=qty)
            context = {'sts': 'rawing', 'sub': sub}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'info':
            val = request.POST.get('val')
            raw = KitchenRecipe.objects.get(id=val)
            sub = SubKitchenRecipe.objects.filter(sub=raw, )
            context = {'sts': 'info', 'sub': sub, 'raw': raw}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'delete':
            val = request.POST.get('val')
            raw = KitchenRecipe.objects.get(id=val).delete()
            g_ing = KitchenRecipe.objects.all()
            ing = reciptInventorylc(g_ing)
            context = {'ing': ing}
            return render(request, 'kitchen/recipt.html', context)
        if action == 'stock':
            val = request.POST.get('val')
            g_ing = KitchenRecipe.objects.get(id=val)
            ing = KitchenInventory.objects.filter(name=g_ing)
            context = {'ing': ing, 'sts': 'dtil'}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'cler':
            val = request.POST.get('val')
            g_ing = KitchenInventory.objects.get(id=val)
            g_ing.status = 'WASTE REQUEST'
            g_ing.fnsh = True
            g_ing.save(update_fields=['fnsh','status'])
            ing = KitchenInventory.objects.filter(name=g_ing.name)
            context = {'ing': ing, 'sts': 'clract'}
            return render(request, 'kitchen/recisub.html', context)
        if action == 'cook':
            val = request.POST.get('val')
            ing = KitchenRecipe.objects.get(id=val)
            raw = RawProducts.objects.all()
            context = {'sts': 'prod', 'val': ing.id, 'raw': raw}
            return render(request, 'kitchen/recisub.html', context)
    g_ing = KitchenRecipe.objects.all()
    ing = reciptInventorylc(g_ing)
    context = {'ing': ing}
    return render(request, 'kitchen/recipt.html', context)

def recipeTask(qty,sub,subtsk):
    data = []
    for i in sub:
        if i.raw:
            rq_qty = i.quantity * qty
            while rq_qty != 0:
                x = Inventory.objects.filter(product=i.raw, fnsh=False).order_by('date').first()

                if x:
                    if x.q_out > rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, raw=x, quantity=rq_qty)
                        x.q_out = x.q_out - rq_qty
                        x.save(update_fields=['q_out'])
                        rq_qty = 0
                        stat = 'Stock Available'
                    elif x.q_out == rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, raw=x, quantity=rq_qty)
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        rq_qty = 0
                        stat = 'Stock Available'
                    elif x.q_out < rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, raw=x, quantity=rq_qty)
                        rq_qty = rq_qty - x.q_out
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        stat = 'Stock Available'

                else:

                    KitchenSubTask.objects.create(job=subtsk, raw=x, quantity=rq_qty)
                    InventoryTask.objects.create( product=i.raw, msg='ITEM STOCK FINISH', status='PENDING')
                    stat = 'Purchase Request'
                    rq_qty = 0
            rq_qty = i.quantity * qty
            dlt = {
                'item': i.raw.name,
                'type': 'RAW',
                'qty': rq_qty,
                'stats': stat,
            }
            data.append(dlt)
        if i.ingredient:
            rq_qty = i.quantity * qty

            while rq_qty != 0:
                x = KitchenInventory.objects.filter(ingred=i.ingredient, fnsh=False).order_by('date').first()
                if x:
                    if x.q_out > rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, ingrd=x, quantity=rq_qty)
                        x.q_out = x.q_out - rq_qty
                        x.save(update_fields=['q_out'])
                        rq_qty = 0
                        stat = 'Stock Available'
                    elif x.q_out == rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, ingrd=x, quantity=rq_qty)
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        rq_qty = 0
                        stat = 'Stock Available'
                    elif x.q_out < rq_qty:
                        KitchenSubTask.objects.create(job=subtsk, ingrd=x, quantity=rq_qty)
                        rq_qty = rq_qty - x.q_out
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        stat = 'Stock Available'
                else:

                    KitchenSubTask.objects.create(job=subtsk, ingrd=x, quantity=rq_qty)
                    kt = kitchenTask.objects.create(  status='PENDING')
                    KitchenJobsAssign.objects.create(task=kt,ingrd=i.ingredient,descrp='ITEM STOCK FINISH')
                    stat = 'Task Request'
                    rq_qty = 0
            rq_qty = i.quantity * qty
            dlt = {
                'item': i.ingredient.name,
                'type': 'Ingredient',
                'qty': rq_qty,
                'stats': stat,
            }
            data.append(dlt)
    return data

def task_Recipe(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'tsk':
            val = request.POST.get('val')
            ing = KitchenRecipe.objects.get(id=val)
            context = {'ing':ing , 'sts':'tsk'}
            return render(request, 'kitchen/reciptask.html', context)
        if action == 'nwtsk':
            val = request.POST.get('val')
            inv = request.POST.get('inv')
            qty = request.POST.get('qty')

            invt = True
            if inv == '2':
                invt = False
            ing = KitchenRecipe.objects.get(id=val)
            tsk = kitchenTask.objects.create(for_sale=invt,status='PENDING')
            qty = decimal.Decimal(qty)
            subtsk = KitchenJobsAssign.objects.create(task=tsk,recipe=ing,quantity=qty,for_sale=invt)
            sub = SubKitchenRecipe.objects.filter(sub=ing)
            data = recipeTask(qty,sub,subtsk)
            context = {'sts':'new','patch': tsk.task,'data':data}
            return render(request, 'kitchen/reciptask.html', context)
        if action == 'extsk':
            val = request.POST.get('val')

            tsk = kitchenTask.objects.filter(status='PENDING')
            context = {'sts': 'extsk', 'tsk': tsk,'val':val }
            return render(request, 'kitchen/reciptask.html', context)
        if action == 'addext':
            val = request.POST.get('val')
            tsk = request.POST.get('tsk')
            inv = request.POST.get('inv')
            qty = request.POST.get('qty')
            ing = KitchenRecipe.objects.get(id=val)
            tsk = kitchenTask.objects.get(id=tsk)
            qty = decimal.Decimal(qty)
            invt = True
            if inv =='2':
                invt = False
            subtsk = KitchenJobsAssign.objects.create(task=tsk,recipe=ing,quantity=qty,for_sale=invt)
            sub = SubKitchenRecipe.objects.filter(sub=ing)
            data = recipeTask(qty,sub,subtsk)
            context = {'sts':'new','patch': tsk.task,'data':data}
            return render(request, 'kitchen/reciptask.html', context)
        if action == 'chek':
            val = request.POST.get('val')
            ing = KitchenRecipe.objects.get(id=val)
            context = {'sts': 'chek',  'ing': ing}
            return render(request, 'kitchen/reciptask.html', context)
        if action == 'chkrsl':
            val = request.POST.get('val')
            qty = request.POST.get('qty')
            ing = KitchenRecipe.objects.get(id=val)
            data = recipe_Invcheck(ing, int(qty))
            print(data)
            context = {'sts': 'chkrsl', 'data': data, 'val': val}
            return render(request, 'kitchen/reciptask.html', context)



def recipe_Invcheck(obj, n):
    get_sub = SubKitchenRecipe.objects.filter(sub=obj)
    data = []
    if get_sub:
        for i in get_sub:
            try:
                get_p = RawProducts.objects.get(id=i.raw.id)
                get_inv = Inventory.objects.filter(product=get_p).aggregate(rem_stk=Sum('q_out'))['rem_stk']
                if get_inv is None:
                    get_inv = 0
            except:
                get_p = Ingredients.objects.get(id=i.ingredient.id)
                get_inv = KitchenInventory.objects.filter(ingred=get_p).aggregate(rem_stk=Sum('q_out'))['rem_stk']
                if get_inv is None:
                    get_inv = 0
            if get_inv >= i.quantity * n:
                r = {
                    'prod': get_p.name,
                     'rslt' :'Available',
                }
                data.append(r)
            else:
                r={
                    'prod':get_p.name,
                    'rslt': 'Missing',
                }
                data.append(r)
    return data
def ingr_Invcheck(obj, n):
    get_sub = SubIngredients.objects.filter(sub=obj)
    data = []
    if get_sub:
        for i in get_sub:
            try:
                get_p = RawProducts.objects.get(id=i.items.id)
                get_inv = Inventory.objects.filter(product=get_p).aggregate(rem_stk=Sum('q_out'))['rem_stk']
                if get_inv is None:
                    get_inv = 0
            except:
                get_p = Ingredients.objects.get(id=i.ingre.id)
                get_inv = KitchenInventory.objects.filter(ingred=get_p).aggregate(rem_stk=Sum('q_out'))['rem_stk']
                if get_inv is None:
                    get_inv = 0
            if get_inv >= i.quantity * n:
                r = {
                    'prod': get_p.name,
                     'rslt' :'Available',
                }
                data.append(r)
            else:
                r={
                    'prod':get_p.name,
                    'rslt': 'Missing',
                }
                data.append(r)
    return data

# task
def kit_serial():
    try:
        obj = KitchenInventory.objects.all().order_by('-patch')[0]
        old = obj.patch[3:]
    except:
        old = 0
    new = int(old) +  1
    return  'KT-{0}'.format(new)
def task(request):
    if request.htmx:
        action = request.POST.get('action')
        if action == 'inginfo':
            val = request.POST.get('val')
            raw = Ingredients.objects.get(id=val)
            sub = SubIngredients.objects.filter(sub=raw, )
            context = {'sts': 'inginfo', 'sub': sub, 'raw': raw}
            return render(request, 'kitchen/tsk_sub.html', context)
        if action == 'info':
            val = request.POST.get('val')
            raw = KitchenRecipe.objects.get(id=val)
            sub = SubKitchenRecipe.objects.filter(sub=raw, )
            context = {'sts': 'info', 'sub': sub, 'raw': raw}
            return render(request, 'kitchen/tsk_sub.html', context)
        if action == 'start':
            today = datetime.today()
            val = request.POST.get('val')
            tsk = kitchenTask.objects.get(id=val)
            tsk.status = 'START'
            tsk.start_time = today
            tsk.save(update_fields=['status','start_time'])
        if action == 'end':
            val = request.POST.get('val')
            tsk = kitchenTask.objects.get(id=val)
            today = datetime.today()
            tsk.status = 'FINISH'
            tsk.j_end = True
            tsk.end_time = today
            tsk.duration = (today).replace(tzinfo=None) - (tsk.start_time).replace(tzinfo=None)
            tsk.save()
            sub = KitchenJobsAssign.objects.filter(task=tsk)
            for i in sub:
                if i.recipe:
                    patch = kit_serial()
                    cost = kitchCost(i)
                    KitchenInventory.objects.create(patch=patch,name=i.recipe,cate=i.recipe.cate,cost=cost,
                                                    q_in=i.quantity,q_out=i.quantity,status='IN')
                if i.ingrd:
                    patch = kit_serial()
                    cost = kitchCost(i)
                    KitchenInventory.objects.create(patch=patch, ingred=i.ingrd,  cost=cost,
                                                    q_in=i.quantity, q_out=i.quantity, status='IN')

    tsk = kitchenTask.objects.filter(j_end = False)
    context = {'task': tsk, }
    return render(request, 'kitchen/task.html', context)

def kitchCost(sub):
    su_tsk = KitchenSubTask.objects.filter(job=sub)
    cost = 0
    for i in su_tsk:
        if i.raw:

            x = decimal.Decimal(i.raw.avg_price) * decimal.Decimal(i.quantity)

            cost += decimal.Decimal(i.raw.avg_price) * decimal.Decimal(i.quantity)
        if i.ingrd:
            cost += decimal.Decimal(i.ingrd.cost) * decimal.Decimal(i.quantity)
    return cost

# pricing
def pricing(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'adprf':

            context = {'sts': 'adprf'}
            return render(request, 'kitchen/price.html', context)
        if action == 'prf':
            adprc = request.POST.get('adprc')
            print(adprc)
            PricingSystem.objects.create(point=adprc)
            prc = PricingSystem.objects.all()
            context = {'sts': 'prf','prc': prc}
            return render(request, 'kitchen/price.html', context)
        if action == 'price':
            val = request.POST.get('val')
            inprice = request.POST.get('inprice')
            syst = request.POST.get('syst')
            rp = KitchenRecipe.objects.get(id=val)
            sys = PricingSystem.objects.get(id=syst)
            price , create = RecipePrice.objects.get_or_create(profil=sys,name=rp,)
            price.price=inprice
            price.save()
            return redirect(reciptls)
        if action == 'feat':
            val = request.POST.get('val')
            inprice = request.POST.get('inprice')
            syst = request.POST.get('syst')
            rp = KitchenRecipe.objects.get(id=val)
            rp.feature=True
            rp.save(update_fields=['feature'])
            sys = PricingSystem.objects.get(id=syst)
            price , create = RecipePrice.objects.get_or_create(profil=sys,name=rp,)
            price.price=inprice
            price.feature=True
            price.save()
            data = RawProducts.objects.all()
            context = {'sts': 'feat', 'data': data,'prce':price.id}
            return render(request, 'kitchen/price.html', context)
        if action == 'gtraw':
            prce = request.POST.get('prce')
            data = RawProducts.objects.all()
            context = {'sts': 'gtraw', 'data': data, 'prce': prce}
            return render(request, 'kitchen/price.html', context)

        if action == 'featraw':
            prce = request.POST.get('prce')
            raw = request.POST.get('raw')
            qty = request.POST.get('qty')
            prc = request.POST.get('prc')
            rp = RecipePrice.objects.get(id=prce)
            graw = RawProducts.objects.get(id=raw)
            rf = RecipeFeatuers.objects.create(name=rp.name,raw=graw,quantity=qty)
            fp = FeatuersPrice.objects.create(name=rp,extra=rf,price=prc)
            context = {'sts': 'featraw', 'rf': rf, 'fp': fp}
            return render(request, 'kitchen/price.html', context)

        if action == 'gting':
            prce = request.POST.get('prce')
            data = Ingredients.objects.all()
            context = {'sts': 'gting', 'data': data, 'prce': prce}
            return render(request, 'kitchen/price.html', context)

        if action == 'feating':
            prce = request.POST.get('prce')
            raw = request.POST.get('raw')
            qty = request.POST.get('qty')
            prc = request.POST.get('prc')
            rp = RecipePrice.objects.get(id=prce)
            graw = Ingredients.objects.get(id=raw)
            rf = RecipeFeatuers.objects.create(name=rp.name, ingre=graw, quantity=qty)
            fp = FeatuersPrice.objects.create(name=rp, extra=rf, price=prc)
            context = {'sts': 'featraw', 'rf': rf, 'fp': fp}
            return render(request, 'kitchen/price.html', context)


        val = request.POST.get('val')
        rp = KitchenRecipe.objects.get(id=val)
        prc = PricingSystem.objects.all()
        context = {'prc': prc,'val':val,'rp':rp , 'sts':'prcsys'}
        return render(request, 'kitchen/price.html', context)


def btn_price(request):
    if request.htmx:
        action = request.POST.get('action')
        print(action)
        if action == 'srch':
            syst = request.POST.get('syst')
            prf = PricingSystem.objects.get(id=syst)
            pr = RecipePrice.objects.filter(profil=prf ,pause=False)
            context = {'pr': pr,'sts':'list','val':prf.id }
            return render(request, 'kitchen/prcdsp.html', context)

        if action == 'remv':
            syst = request.POST.get('syst')
            val = request.POST.get('val')
            prf = PricingSystem.objects.get(id=syst)
            RecipePrice.objects.get(id=val).update(pause=True)
            pr = RecipePrice.objects.filter(profil=prf ,pause=False)
            context = {'pr': pr,'sts':'list','val':prf.id }
            return render(request, 'kitchen/prcdsp.html', context)
        if action == 'upd':
            syst = request.POST.get('syst')
            val = request.POST.get('val')
            prc = request.POST.get('prc')
            prf = PricingSystem.objects.get(id=syst)
            RecipePrice.objects.filter(id=val).update(price=prc)
            pr = RecipePrice.objects.filter(profil=prf,pause=False)
            context = {'pr': pr, 'sts': 'list', 'val': prf.id}
            return render(request, 'kitchen/prcdsp.html', context)
        if action == 'fetupd':
            syst = request.POST.get('syst')
            val = request.POST.get('val')
            prc = request.POST.get('sbprc')
            prf = PricingSystem.objects.get(id=syst)
            FeatuersPrice.objects.filter(id=val).update(price=prc)
            pr = RecipePrice.objects.filter(profil=prf,pause=False)
            context = {'pr': pr, 'sts': 'list', 'val': prf.id}
            return render(request, 'kitchen/prcdsp.html', context)
        if action == 'fetdel':
            syst = request.POST.get('syst')
            val = request.POST.get('val')
            prf = PricingSystem.objects.get(id=syst)
            FeatuersPrice.objects.filter(id=val).update(pause=True)
            pr = RecipePrice.objects.filter(profil=prf,pause=False)
            context = {'pr': pr, 'sts': 'list', 'val': prf.id}
            return render(request, 'kitchen/prcdsp.html', context)
        if action == 'new':
            context = { 'sts': 'new'}
            return render(request, 'kitchen/prcdsp.html', context)
        if action =='addnew':
            adprc = request.POST.get('adprc')
            pr = PricingSystem.objects.create(point=adprc)
            data = KitchenRecipe.objects.all()
            context = {'sts': 'addnew','data':data,'pr':pr.id}
            return render(request, 'kitchen/prcdsp.html', context)
        if action =='newlst':
            pr = request.POST.get('pr')
            val = request.POST.get('val')
            pr = PricingSystem.objects.get(id=pr)
            kp = KitchenRecipe.objects.get(id=val)
            rp = RecipePrice.objects.create(profil=pr, name=kp)
            if kp.feature:
                rp.feature=True
                rp.save(update_fields=['feature'])
                rf = RecipeFeatuers.objects.filter(name=kp)
                for i in rf:
                    FeatuersPrice.objects.create(name=rp,extra=i)

            context = {'sts': 'newlst','rp':rp}
            return render(request, 'kitchen/prcdsp.html', context)
        if action == 'adnepc':
            g_rp = request.POST.get('rp')
            prc = request.POST.get('prc')
            rp = RecipePrice.objects.get(id=g_rp)
            rp.price = prc
            rp.save(update_fields=['price'])
            context = {'rp': rp, 'sts': 'adnepc'}
            return render(request, 'kitchen/prcdsp.html', context)


        if action == 'nefetur':
            val = request.POST.get('val')
            g_rp = request.POST.get('rp')
            prc = request.POST.get('sbprc')
            rp = RecipePrice.objects.get(id=g_rp)
            up_rf = FeatuersPrice.objects.get(id=val)
            up_rf.price = prc
            up_rf.save()
            rf = FeatuersPrice.objects.filter(name=rp,pause=False)
            context = {'rf': rf, 'sts': 'nefetur','rp':rp.id}

            return render(request, 'kitchen/prcdsp.html', context)


    prc = PricingSystem.objects.all()
    context = {'prc': prc,  }
    return render(request, 'kitchen/price_btn.html', context)


def kitbackUp(request):

    if request.POST:
        action = request.POST.get('action')
        response = HttpResponse(content_type='text/csv')
        if action == '1':
            response['Content-Disposition'] = 'attachment; filename="Ingredients.csv"'
            acc = Ingredients.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '2':
            response['Content-Disposition'] = 'attachment; filename="SubIngredients.csv"'
            acc = SubIngredients.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '3':
            response['Content-Disposition'] = 'attachment; filename="KitchenRecipe.csv"'
            acc = KitchenRecipe.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response

        if action == '4':
            response['Content-Disposition'] = 'attachment; filename="SubKitchenRecipe.csv"'
            acc = SubKitchenRecipe.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '5':
            response['Content-Disposition'] = 'attachment; filename="RecipeFeatuers.csv"'
            acc = RecipeFeatuers.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '6':
            response['Content-Disposition'] = 'attachment; filename="PricingSystem.csv"'
            acc = PricingSystem.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '7':
            response['Content-Disposition'] = 'attachment; filename="RecipePrice.csv"'
            acc = RecipePrice.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '8':
            response['Content-Disposition'] = 'attachment; filename="FeatuersPrice.csv"'
            acc = FeatuersPrice.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '9':
            response['Content-Disposition'] = 'attachment; filename="kitchenTask.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = kitchenTask.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = kitchenTask.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '10':
            response['Content-Disposition'] = 'attachment; filename="KitchenJobsAssign.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = KitchenJobsAssign.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = KitchenJobsAssign.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '11':
            response['Content-Disposition'] = 'attachment; filename="KitchenInventory.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = KitchenInventory.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = KitchenInventory.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response
        if action == '12':
            response['Content-Disposition'] = 'attachment; filename="KitchenSubTask.csv"'
            dat1 = request.POST.get('dat1')
            dat2 = request.POST.get('dat2')
            if dat1:
                start = dat1[5:]
                end = dat2[5:]
                acc = KitchenSubTask.objects.filter(date__month__gte=start, date__month__lte=end)
            else:
                acc = KitchenSubTask.objects.all()
            opts = acc.model._meta
            writer = csv.writer(response)
            field_names = [field.name for field in opts.fields]
            writer.writerow(field_names)
            for obj in acc:
                writer.writerow([getattr(obj, field) for field in field_names])
            return response



    context = {'cog': 'cog'}
    return render(request, 'account/backup.html', context)