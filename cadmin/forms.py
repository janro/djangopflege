from django.db import models
from django.forms import ModelForm

from cadmin.models import Family, Carer, Operation, CarerPayment, TradeRegister, FamilyPayment

class FamilyForm(ModelForm):
  class Meta:
    model = Family

class CarerForm(ModelForm):
  class Meta:
    model = Carer

class OperationForm(ModelForm):
  class Meta:
    model = Operation

class CarerPaymentForm(ModelForm):
  class Meta:
    model = CarerPayment

class FamilyPaymentForm(ModelForm):
  class Meta:
    model = FamilyPayment

class CarerTradeRegisterForm(ModelForm):
  class Meta:
    model = TradeRegister