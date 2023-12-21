from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save


# Create your models here.


class AccountFixed(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name} '
class AccountParent(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=8,null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name} '
class AccountKeys(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    nature = models.ForeignKey(AccountParent, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=5, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f'{self.id} '



class AccountRef(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=5, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name} '

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
    InvoiceRef.objects.create(code='Inv', serial=n_serial)
    new = str(n_serial)
    invoice = '00000{0}'.format(new)
    chk = len(invoice)
    while chk > 5:
        invoice = invoice[1:]
        chk = len(invoice)
    return invoice
class JournalRef(models.Model):
    ref = models.CharField(max_length=20, null=True, blank=True)
    ref_nm = models.CharField(max_length=20, null=True, blank=True)
    ref_cd = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    audt = models.BooleanField(default=False, null=True, blank=True)
    e_date = models.DateField( null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.ref} '

    @property
    def get_debit(self):
        debit = self.accountjournaldebt_set.all()
        return debit

    @property
    def get_debit_total(self):
        orderitems = self.accountjournaldebt_set.all()
        sub_total = sum([item.amount for item in orderitems])
        return round(Decimal(sub_total), 2)
    @property
    def get_credit(self):
        credit = self.accountjournalcredit_set.all()
        return credit

    @property
    def get_credit_total(self):
        orderitems = self.accountjournalcredit_set.all()
        sub_total = sum([item.amount for item in orderitems])
        return round(Decimal(sub_total), 2)
def JournalRefJornal(sender, instance, *args, **kwargs):
    nm = instance.ref[:3]
    cd = instance.ref[4:]
    instance.ref_nm = nm
    instance.ref_cd = cd
pre_save.connect(JournalRefJornal, sender=JournalRef)


class AccountJournalDebt(models.Model):
    ref = models.ForeignKey(JournalRef, on_delete=models.CASCADE, null=True, blank=True)
    key = models.ForeignKey(AccountKeys, models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    ex_ref = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f'{self.ref.ref} '

class AccountJournalCredit(models.Model):
    ref = models.ForeignKey(JournalRef, on_delete=models.CASCADE, null=True, blank=True)
    key = models.ForeignKey(AccountKeys, models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    ex_ref = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f'{self.ref.ref} '



class AccountRequest(models.Model):
    ref = models.CharField(max_length=50, null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)
    item_id = models.IntegerField(null=True, blank=True,default=0)
    item = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True,default='PENDING')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class AccountLedger(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    key = models.ForeignKey(AccountKeys, models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class AccountCOGS(models.Model):
    patch = models.CharField(max_length=50, null=True, blank=True)
    invoice = models.CharField(max_length=50, null=True, blank=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    direct = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    indirect = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
