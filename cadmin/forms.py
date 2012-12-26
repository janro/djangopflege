from django.db import models
from django.forms import ModelForm

from cadmin.models import Family, Carer, Operation

class FamilyForm(ModelForm):
  class Meta:
    model = Family

class OperationrForm(ModelForm):
  class Meta:
    model = Carer

class OperationForm(ModelForm):
  class Meta:
    model = Operation    