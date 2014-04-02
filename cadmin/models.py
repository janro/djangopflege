
from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class Carer(models.Model):

  # firstname
  # lastname
  # phone_at
  # phone_ro
  # date_of_birth
  # hometown
  # family
  # weight
  # height
  # children
  # driving_license
  # smoker
  # nationality
  # insurance_number
  # id_card_number
  # iban
  # bic
  # language_skills
  # operation_skills
  # remark
  # archive
  # duty

  SKILL_LEVELS = (
    (0, 'Unbekannt'),
    (1, 'Stufe 1'),
    (2, 'Stufe 2'),
    (3, 'Stufe 3'),
    (4, 'Stufe 4'),
  )

  GENDER = (
    (1, 'MALE'),
    (2, 'FEMALE'),
  )

  firstname = models.CharField(max_length=100, blank=False)
  lastname = models.CharField(max_length=100, blank=True)
  phone_at = models.CharField(max_length=20, blank=True)
  phone_ro = models.CharField(max_length=20, blank=True)
  date_of_birth = models.DateField(null=True, blank=True)
  hometown = models.CharField(max_length=100, blank=True)
  weight = models.IntegerField(null=True, blank=True)
  height = models.IntegerField(null=True, blank=True)
  family = models.BooleanField()
  children = models.BooleanField()
  smoker = models.BooleanField() 
  driving_license = models.BooleanField()
  nationality = models.CharField(max_length=100, blank=True)
  insurance_number = models.CharField(max_length=100, blank=True)
  id_card_number = models.CharField(max_length=100, blank=True)
  iban = models.CharField(max_length=100, blank=True)
  bic = models.CharField(max_length=100, blank=True)
  language_skills = models.IntegerField(default=0, choices=SKILL_LEVELS, blank=False)
  operation_skills = models.IntegerField(default=0, choices=SKILL_LEVELS, blank=False)
  remark = models.CharField(max_length=500, null=True, blank=True)
  archive = models.BooleanField()
  duty = models.IntegerField(null=True, blank=True)

  def __str__(self):
    full_name = self.lastname
    full_name += ' '
    full_name += self.firstname
    return full_name

#  @models.permalink
#  def get_absolute_url(self):
#      return ('cadmin.views.carerDetails', [str(self.id)])

  class Meta:
    permissions = (('carerCreateDelete', 'Create or Delete'),)

class Family(models.Model):
  
  # firstname_contact_person
  # lastname_contact_person
  # phone_contact_person
  # firstname_care_person
  # lastname_care_person
  # phone_care_person
  # street
  # number
  # postal_code
  # city
  # care_level
  # date_of_birth
  # archive
  # duty

  CARE_LEVELS = (
    (0,'Unbekannt'),
    (1, 'Stufe 1'),
    (2, 'Stufe 2'),
    (3, 'Stufe 3'),
    (4, 'Stufe 4'),
    (5, 'Stufe 5'),
    (6, 'Stufe 6'),
  )
  
  firstname_contact_person = models.CharField(max_length=100, blank=True)
  lastname_contact_person = models.CharField(max_length=100, blank=False)
  phone_contact_person = models.CharField(max_length=20, blank=False)
  firstname_care_person = models.CharField(max_length=100, blank=True)
  lastname_care_person = models.CharField(max_length=100, blank=True)
  phone_care_person = models.CharField(max_length=20, blank=True)
  street = models.CharField(max_length=100, blank=True)
  number = models.IntegerField(null=True, blank=True)
  postal_code = models.IntegerField(null=True, blank=True)
  city = models.CharField(max_length=100, blank=True)
  care_level = models.IntegerField(default=1, choices=CARE_LEVELS, blank=True)
  date_of_birth = models.DateField(null=True, blank=True)
  archive = models.BooleanField()
  duty = models.IntegerField(null=True, blank=True)
  remark = models.CharField(max_length=500, null=True, blank=True)

  def __str__(self):
    if self.firstname_care_person and self.lastname_care_person:
      full_name = self.lastname_care_person
      full_name += ' '
      full_name += self.firstname_care_person
      return full_name
    else:
      full_name = self.lastname_contact_person
      full_name += ' '
      full_name += self.firstname_contact_person
      return full_name

  class Meta:
      permissions = (('familyCreateDelete', 'Create or Delete'),)

class Operation(models.Model):

  # carer
  # family
  # start_date
  # end_date

  carer = models.ForeignKey(Carer)
  family = models.ForeignKey(Family)
  start_date = models.DateField(null=False, blank=False)
  end_date = models.DateField(null=True, blank=True)

  def clean(self):

    pass

    # very primitive and first solution for missing end_dates
    # --> only do the check if end_date is avaible!

    # disabled due problems
    # there might be the case a famaly pays for two carers at the same time

    # if self.end_date is not None:
    #   # Check all Operations for Intersections
    #   # 1 - The Carer is envolved
    #   try:
    #     operations = Operation.objects.filter(carer=self.carer).exclude(id=self.id)
    #     for operation in operations:
    #       if operation.end_date is not None:
    #         if Operation.opIntersect(operation,self):
    #           #if the carer is already at another family
    #           raise ValidationError(str(self.carer)+' is already at '+str(operation.family)+
    #             ' ('+operation.start_date.strftime("%d.%m.%Y")+' - '+operation.end_date.strftime("%d.%m.%Y")+')')
    #   except ObjectDoesNotExist:
    #     pass
    #   # 2 - The Family is envolved
    #   try:
    #     operations = Operation.objects.filter(family=self.family).exclude(id=self.id)
    #     for operation in operations:
    #       if operation.end_date is not None:
    #         if Operation.opIntersect(operation,self):
    #           #if an other carer is already at this family
    #           raise ValidationError(str(operation.carer)+' is already at '+str(self.family)+
    #             ' ('+operation.start_date.strftime("%d.%m.%Y")+' - '+operation.end_date.strftime("%d.%m.%Y")+')')
    #   except ObjectDoesNotExist:
    #     pass
    

  def opIntersect(op1, op2):
    return (op1.start_date < op2.start_date < op1.end_date) or (op1.start_date < op2.end_date < op1.end_date)

  class Meta:
    permissions = (('operationCreateDelete', 'Create or Delete'),)

class FamilyPayment(models.Model):

  # family
  # amount
  # date
  # account_print_number
  # method
  # remark

  PAYMENT_METHODS = (
    (1, 'Bar'),
    (2, 'Elektronisch'),
  )

  family = models.ForeignKey(Family)
  amount = models.IntegerField(null=False, blank=False)
  date = models.DateField(blank=False)
  account_print_number = models.IntegerField(null=True, blank=True)
  method = models.IntegerField(default=1, choices=PAYMENT_METHODS, blank=False)
  remark = models.CharField(max_length=200, blank=True)

  class Meta:
      permissions = (('familyPaymentView', 'View Family Payment'),)

class CarerPayment(models.Model):

  # carer
  # amount
  # date
  # account_print_number
  # method
  # remark

  PAYMENT_METHODS = (
    (1, 'Bar'),
    (2, 'Elektronisch'),
  )

  carer = models.ForeignKey(Carer)
  date = models.DateField(blank=False)
  amount = models.IntegerField(null=False, blank=False)
  method = models.IntegerField(default=1, choices=PAYMENT_METHODS, blank=False)
  account_print_number = models.IntegerField(null=True, blank=True)
  remark = models.CharField(max_length=200, blank=True)

  class Meta:
    permissions = (('carerPaymentView', 'View Carer Payment'),)

class TradeRegister(models.Model):

  ACTIONS = (
    (1, 'IN'),
    (2, 'OUT'),
  )

  carer = models.ForeignKey(Carer)
  date = models.DateField(blank=False)
  action = models.IntegerField(default=1, choices=ACTIONS, blank=False)
