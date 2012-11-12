from django.db import models
from django.forms import ModelForm

from pflegeadmin.models import Family

class FamilyForm(ModelForm):
  class Meta:
    model = Family