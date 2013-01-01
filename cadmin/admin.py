
from django.contrib import admin
from cadmin.models import Family, Carer, Operation, FamilyPayment, CarerPayment, TradeRegister

admin.site.register(Family)
admin.site.register(Carer)
admin.site.register(Operation)

admin.site.register(CarerPayment)
admin.site.register(TradeRegister)