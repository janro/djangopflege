from django.db import models
from django.forms import ModelForm

from cadmin.models import Family, Carer, Operation, CarerPayment, TradeRegister

class FamilyForm(ModelForm):
  class Meta:
    model = Family

class OperationrForm(ModelForm):
  class Meta:
    model = Carer

class OperationForm(ModelForm):
  class Meta:
    model = Operation

class CarerPaymentForm(ModelForm):
  class Meta:
    model = CarerPayment

class CarerTradeRegisterForm(ModelForm):
  class Meta:
    model = TradeRegister