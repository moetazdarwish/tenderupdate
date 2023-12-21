from django.contrib import admin

from account.models import *

# Register your models here.
admin.site.register(AccountFixed)
admin.site.register(AccountParent)
admin.site.register(AccountKeys)
admin.site.register(AccountRef)
admin.site.register(InvoiceRef)
admin.site.register(AccountJournalDebt)
admin.site.register(AccountJournalCredit)
admin.site.register(JournalRef)
admin.site.register(AccountRequest)
admin.site.register(AccountLedger)
admin.site.register(AccountCOGS)