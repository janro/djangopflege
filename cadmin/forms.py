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

  def __init__(self, *args, **kwargs):
    super(OperationForm, self).__init__(*args, **kwargs)
    self.fields['carer'].queryset = Carer.objects.order_by('lastname')
    self.fields['family'].queryset = Family.objects.order_by('lastname_care_person')

class CarerPaymentForm(ModelForm):
  class Meta:
    model = CarerPayment

class FamilyPaymentForm(ModelForm):
  class Meta:
    model = FamilyPayment

class CarerTradeRegisterForm(ModelForm):
  class Meta:
    model = TradeRegister