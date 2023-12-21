from datetime import datetime
from decimal import Decimal
from random import randint

from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save

from account.models import AccountRequest
from crm.models import CustomerProfile
from employee.models import EmployeeDetail
from inventory.models import Inventory, InventoryTask
from kitchen.models import PricingSystem, RecipePrice, KitchenRecipe, RecipeFeatuers, kitchenTask, KitchenJobsAssign, \
    KitchenInventory



class CartName(models.Model):
    name = models.CharField(max_length=150,null=True,blank=True)
    pwd  = models.CharField(max_length=150,null=True,blank=True)
    b_pwd  = models.CharField(max_length=150,null=True,blank=True)
    flat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    prcnt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    pricing = models.ForeignKey(PricingSystem,on_delete=models.CASCADE,null=True,blank=True)
    task = models.BooleanField(default=False,null=True,blank=True)
    inv = models.BooleanField(default=False,null=True,blank=True)
    online = models.BooleanField(default=False,null=True,blank=True)
    status = models.CharField(max_length=10, null=True, blank=True,default='PENDING')

class CartInv(models.Model):
    cart = models.ForeignKey(CartName,on_delete=models.CASCADE,null=True,blank=True)
    recipe = models.ForeignKey(KitchenRecipe,on_delete=models.CASCADE,null=True,blank=True)
    feat = models.ForeignKey(RecipeFeatuers,on_delete=models.CASCADE,null=True,blank=True)
    pricing = models.ForeignKey(RecipePrice,on_delete=models.CASCADE,null=True,blank=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    p_return = models.BooleanField(null=True, blank=True, default=False)
    status = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def get_orderlst(self):
        lst = self.cartproducts_set.all()
        return lst


class CartCash(models.Model):
    cart = models.ForeignKey(CartName, on_delete=models.CASCADE, null=True, blank=True)
    start = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    amt_in = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    amt_out = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    close = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    t_strt = models.DateTimeField(null=True,blank=True)
    t_end = models.DateTimeField(null=True,blank=True)
    p_open = models.BooleanField(null=True,blank=True,default=True)
    p_close = models.BooleanField(null=True,blank=True,default=False)
    rev = models.BooleanField(null=True,blank=True,default=False)
    status = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

class InvoiceRef(models.Model):
    code = models.CharField(max_length=5, null=True, blank=True)
    serial = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f'{self.serial} '

def createInvoice():
    get_inv = InvoiceRef.objects.all().last()
    ss = 0
    if get_inv :
        ss = get_inv.serial

    n_serial = ss + 1
    InvoiceRef.objects.create(code='SAL', serial=n_serial)
    new = str(n_serial)
    invoice = '00000{0}'.format(new)
    chk = len(invoice)
    while chk > 5:
        invoice = invoice[1:]
        chk = len(invoice)
    return invoice
class Cart(models.Model):
    name = models.CharField(max_length=110, null=True, blank=True)
    invoice = models.CharField(max_length=10, null=True, blank=True)
    branch = models.ForeignKey(CartName, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    service = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    delivery = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    items = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True, default='No Note')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    transaction_id = models.CharField(max_length=250, null=True, blank=True)
    ref = models.CharField(max_length=10, null=True, blank=True)
    big = models.BooleanField(null=True, blank=True, default=False)
    online = models.BooleanField(null=True, blank=True, default=False)
    status = models.CharField(max_length=20, blank=True, null=True, default='CREATED')
    create_date = models.DateTimeField(auto_now_add=True,blank=True, null=True,)

    def __str__(self):
        return f'{self.transaction_id} '

    class Meta:
        ordering = ['-create_date']

    @property
    def get_cart_total(self):
        total = self.get_cart_sub_total + self.get_otherFees  - self.get_cart_discount + self.get_delivery + self.get_VAT
        return round(Decimal(total), 2)

    @property
    def cart_total(self):
        total = self.get_cart_sub_total  - self.get_cart_discount + self.get_delivery + self.get_VAT
        return round(Decimal(total), 2)

    @property
    def get_otherFees(self):
        total = (self.branch.flat) + (self.get_cart_sub_total * self.branch.prcnt)
        return round(Decimal(total), 2)
    @property
    def get_cart_sub_total(self):
        orderitems = self.cartproducts_set.all()
        sub_total = sum([item.get_total for item in orderitems])
        return round(Decimal(sub_total), 2)

    @property
    def get_delivery(self):
        area = self.delivery
        return round(Decimal(area), 2)

    @property
    def get_cart_discount(self):
        dis = self.discount
        return round(Decimal(dis), 2)

    @property
    def get_VAT(self):
        tax = 0
        return round(Decimal(tax), 2)

    @property
    def get_orderlst(self):
        lst = self.cartproducts_set.all()
        return lst

    @property
    def cart_items(self):
        orderitems = self.cartproducts_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
def cartJournal(sender, instance, *args, **kwargs):
    if instance.status == 'PAID':
        instance.sub_total = instance.get_cart_sub_total
        instance.service = instance.get_otherFees
        instance.total = instance.get_cart_total
        mk_invoice = createInvoice()
        instance.invoice = mk_invoice

pre_save.connect(cartJournal, sender=Cart)

def ordertsks(sender, instance, *args, **kwargs):
    if instance.status == 'PAID':
        if instance.branch.task:
            code = 'POS-{0}'.format(instance.transaction_id)
            POSTask.objects.create(task=code, pos=instance.branch, order=instance, status='PENDING')
        else:
            code = 'POS-{0}'.format(instance.transaction_id)
            kt = kitchenTask.objects.create(task=code, status='PENDING')
            get_sub = CartProducts.objects.filter(order=instance)
            for i in get_sub:
                KitchenJobsAssign.objects.create(task=kt, recipe=i.product.name,
                                                 quantity=i.quantity, for_cart=True)
                if i.feat:
                    feat_sub = CartSubProducts.objects.filter(suborder=i)
                    for f in feat_sub:
                        KitchenJobsAssign.objects.create(task=kt, feat=f.product,
                                                     quantity=f.quantity, for_cart=True)
        if instance.branch.inv:

            get_sub = CartProducts.objects.filter(order=instance)
            for i in get_sub:
                ci = CartInv.objects.get(cart=instance.branch, recipe=i.product.name)
                ci.qty = ci.qty - i.quantity
                ci.save()
                if i.feat:
                    feat_sub = CartSubProducts.objects.filter(suborder=i)
                    for f in feat_sub:
                        sci = CartInv.objects.get(cart=instance.branch, feat=f.product)
                        sci.qty = sci.qty - f.quantity
                        sci.save()
        else:
            get_sub = CartProducts.objects.filter(order=instance)
            for i in get_sub:
                n = i.quantity
                while n != 0:
                    ci = KitchenInventory.objects.filter(name=i.product.name, fnsh=False).order_by('date').first()
                    if ci:
                        if ci.q_out > n:
                            ci.q_out = ci.q_out - i.quantity
                            ci.save()
                            n = 0
                        elif ci.q_out == n:
                            ci.q_out = 0
                            ci.fnsh = True
                            ci.save()
                            n = 0
                        elif ci.q_out < n:
                            n = n - ci.q_out
                            ci.q_out = 0
                            ci.fnsh = True
                            ci.save()
                    else:
                        n = 0

                if i.feat:
                    feat_sub = CartSubProducts.objects.filter(suborder=i)
                    for f in feat_sub:
                        sci = RecipeFeatuers.objects.get(id=f.product.id)
                        recipeFeatuer(f.quantity,sci)
        txt = 'Revenue Sales InvoiceNo. {0}'.format(instance.invoice)
        AccountRequest.objects.create(ref=instance.invoice,section='POS',item_id=instance.id,
                                      item=txt,amount=instance.sub_total)
        if instance.tax_amount:
            txt = 'INVOICE TAX InvoiceNo. {0}'.format(instance.invoice)
            AccountRequest.objects.create(ref=instance.invoice,section='POS',item_id=instance.id,item=txt
                                      ,amount=instance.tax_amount)
        if instance.delivery:
            txt = 'INVOICE DELIVERY InvoiceNo. {0}'.format(instance.invoice)
            AccountRequest.objects.create(ref=instance.invoice,section='POS',item_id=instance.id,
                                      item=txt,amount=instance.delivery)
        if instance.service:
            txt = 'OTHER FEES  InvoiceNo. {0}'.format(instance.invoice)
            AccountRequest.objects.create(ref=instance.invoice, section='POS', item_id=instance.id,
                                      item=txt, amount=instance.service)
        if instance.discount:
            txt = 'DISCOUNT InvoiceNo. {0}'.format(instance.invoice)
            AccountRequest.objects.create(ref=instance.invoice, section='POS', item_id=instance.id,
                                      item=txt, amount=instance.discount)
post_save.connect(ordertsks, sender=Cart)

def recipeFeatuer(qty,i):
        if i.raw:
            rq_qty =  qty
            while rq_qty != 0:
                x = Inventory.objects.filter(product=i.raw, fnsh=False).order_by('date').first()
                if x:
                    if x.q_out > rq_qty:
                        x.q_out = x.q_out - rq_qty
                        x.save(update_fields=['q_out'])
                        rq_qty = 0
                    elif x.q_out == rq_qty:
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        rq_qty = 0
                    elif x.q_out < rq_qty:
                        rq_qty = rq_qty - x.q_out
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                else:

                    InventoryTask.objects.create( product=i.raw, msg='ITEM STOCK FINISH', status='PENDING')
                    rq_qty = 0
        if i.ingre:
            rq_qty =  qty

            while rq_qty != 0:
                x = KitchenInventory.objects.filter(ingred=i.ingre, fnsh=False).order_by('date').first()
                if x:
                    if x.q_out > rq_qty:

                        x.q_out = x.q_out - rq_qty
                        x.save(update_fields=['q_out'])
                        rq_qty = 0
                    elif x.q_out == rq_qty:
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                        rq_qty = 0
                    elif x.q_out < rq_qty:
                        rq_qty = rq_qty - x.q_out
                        x.q_out = 0
                        x.fnsh = True
                        x.save()
                else:

                    kt = kitchenTask.objects.create( status='PENDING')
                    KitchenJobsAssign.objects.create(task=kt,ingrd=i.ingredient,descrp='ITEM STOCK FINISH')
                    rq_qty = 0
        return 'done'



class CartProducts(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(RecipePrice, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    feat = models.BooleanField(default=False,null=True,blank=True)
    status = models.CharField(max_length=50, blank=True, null=True, default='CREATED')
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-create_date']

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total

    @property
    def get_subfeatuers(self):
        sub = self.cartsubproducts_set.all()
        return sub

class CartSubProducts(models.Model):
    suborder = models.ForeignKey(CartProducts, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(RecipeFeatuers, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class POSTask(models.Model):
    task = models.CharField(max_length=100, null=True, blank=True)
    pos = models.ForeignKey(CartName, on_delete=models.CASCADE, null=True, blank=True)
    emply = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    j_end = models.BooleanField(null=True, blank=True, default=False)
    status = models.CharField(max_length=50,null=True,blank=True)