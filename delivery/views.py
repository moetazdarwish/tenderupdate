from django.shortcuts import render

from delivery.models import *


# Create your views here.


def delivery(request):
    if request.user.is_authenticated:
        if request.htmx:
            action = request.POST.get('action')
            if action == 'area':
                context = {'sts': 'area'}
                return render(request, 'delivery/sub.html', context)
            if action == 'man':
                context = {'sts': 'man'}
                return render(request, 'delivery/sub.html', context)
            if action == 'btnarea':
                dlv = DeliveryCost.objects.all()
                context = {'sts': 'btnarea','dlv':dlv}
                return render(request, 'delivery/sub.html', context)
            if action == 'btnman':
                man = DeliveryProfile.objects.all()
                context = {'sts': 'btnman','man':man}
                return render(request, 'delivery/sub.html', context)
            if action == 'mandelt':
                val = request.POST.get('val')
                DeliveryProfile.objects.get(id=val).delete()
                man = DeliveryProfile.objects.all()
                context = {'sts': 'btnman', 'man': man}
                return render(request, 'delivery/sub.html', context)
            if action == 'delt':
                val = request.POST.get('val')
                DeliveryCost.objects.get(id=val).delete()
            if action == 'aread':
                area = request.POST.get('area')
                cost = request.POST.get('cost')
                price = request.POST.get('price')
                DeliveryCost.objects.create(area=area,cost=cost,price=price)
            if action == 'manad':
                name = request.POST.get('name')
                phone = request.POST.get('phone')
                DeliveryProfile.objects.create(name=name,phone=phone)
                man = DeliveryProfile.objects.all()
                context = {'sts': 'btnman', 'man': man}
                return render(request, 'delivery/sub.html', context)
            if action == 'select':
                val = request.POST.get('Val')
                mn =DeliveryProfile.objects.get(id=val)
                dlv = DeliveryCost.objects.all()

                context = {'sts': 'select', 'dlv': dlv,'man':mn}
                return render(request, 'delivery/sub.html', context)
            if action == 'areaselct':
                val = request.POST.get('val')
                man = request.POST.get('man')
                mn =DeliveryProfile.objects.get(id=man)
                ara = DeliveryCost.objects.get(id=val)
                DeliveryArea.objects.create(name=mn,area=ara)
                context = {'sts': 'areaselct', 'ara': ara}
                return render(request, 'delivery/sub.html', context)
            if action == 'work':
                man = request.POST.get('man')
                mn =DeliveryProfile.objects.get(id=man)
                dlv = DeliveryArea.objects.filter(name=mn)
                context = {'sts': 'work', 'dlv': dlv,'man':mn}
                return render(request, 'delivery/sub.html', context)

            if action == 'areadlt':
                val = request.POST.get('val')
                ara = DeliveryArea.objects.get(id=val)
                nam = ara.area
                ara.delete()
                context = {'sts': 'areaselct', 'ara': nam}
                return render(request, 'delivery/sub.html', context)

            if action == 'ardata':
                val = request.POST.get('val')
                mn = DeliveryCost.objects.get(id=val)
                dlv = DeliveryArea.objects.filter(area=mn)
                context = {'sts': 'ardata', 'dlv': dlv, 'man': mn}
                return render(request, 'delivery/sub.html', context)
            if action == 'datadlt':
                val = request.POST.get('val')
                ara = DeliveryArea.objects.get(id=val)
                nam = ara.name
                ara.delete()
                context = {'sts': 'datselct', 'ara': nam}
                return render(request, 'delivery/sub.html', context)

        dlv = DeliveryCost.objects.all()
        context = {'dlv': dlv}
        return render(request, 'delivery/list.html', context)