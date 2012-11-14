from django.db import models
from django.forms import ModelForm

from pflegeadmin.models import Family, Carer

class FamilyForm(ModelForm):
  class Meta:
    model = Family

class CarerForm(ModelForm):
  class Meta:
    model = Carer