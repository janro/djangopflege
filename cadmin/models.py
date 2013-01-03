
from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class Carer(models.Model):

  # firstname
  # lastname
  # phone
  # date_of_birth
  # hometown
  # family
  # weight
  # smoker
  # trade_registered
  # language_skills
  # operation_skills
  # remark

  SKILL_LEVELS = (
    (1, 'Skill Level 1'),
    (2, 'Skill Level 2'),
    (3, 'Skill Level 3'),
    (4, 'Skill Level 4'),
  )

  GENDER = (
    (1, 'MALE'),
    (2, 'FEMALE'),
  )

  firstname = models.CharField(max_length=100, null=True, blank=False)
  lastname = models.CharField(max_length=100, null=True, blank=True)
  phone = models.CharField(max_length=20, null=True, blank=True)
  date_of_birth = models.DateField(null=True, blank=True)
  hometown = models.CharField(max_length=100, null=True, blank=True)
  weight = models.IntegerField(null=True, blank=True)
  family = models.BooleanField()
  smoker = models.BooleanField()
  trade_registered = models.BooleanField()
  language_skills = models.IntegerField(default=1, choices=SKILL_LEVELS, blank=True)
  operation_skills = models.IntegerField(default=1, choices=SKILL_LEVELS, blank=True)
  remark = models.CharField(max_length=500, null=True, blank=True)

  def __unicode__(self):
    full_name = self.firstname
    full_name += ' '
    full_name += self.lastname
    return full_name

  class Meta:
    permissions = (('carerCreateDelete', 'Create or Delete'),)

class Family(models.Model):
  
  # firstname_contact_person
  # lastname_contact_person
  # phone_contact_person
  # firstname_operation_person
  # lastname_operation_person
  # phone_operation_person
  # street
  # number
  # postal_code
  # city
  # care_level
  # date_of_birth

  CARE_LEVELS = (
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3, 'Level 3'),
    (4, 'Level 4'),
  )
  
  firstname_contact_person = models.CharField(max_length=100, null=True, blank=True)
  lastname_contact_person = models.CharField(max_length=100, null=True, blank=False)
  phone_contact_person = models.CharField(max_length=20, null=True, blank=False)
  firstname_operation_person = models.CharField(max_length=100, null=True, blank=True)
  lastname_operation_person = models.CharField(max_length=100, null=True, blank=True)
  phone_operation_person = models.CharField(max_length=20, null=True, blank=True)
  street = models.CharField(max_length=100, null=True, blank=True)
  number = models.IntegerField(null=True, blank=True)
  postal_code = models.IntegerField(null=True, blank=True)
  city = models.CharField(max_length=100, null=True, blank=True)
  care_level = models.IntegerField(default=1, choices=CARE_LEVELS, blank=True)
  date_of_birth = models.DateField(null=True, blank=True)

  def __unicode__(self):
    full_name = self.firstname_operation_person
    full_name += ' '
    full_name += self.lastname_operation_person
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
    # Check all Operations for Intersections
    # 1 - The Carer is envolved
    try:
      operations = Operation.objects.filter(carer=self.carer)
      for operation in operations:
        if Operation.opIntersect(operation,self):
          #if the carer is already at another family
          raise ValidationError(str(self.carer)+' is already at '+str(operation.family)+
            ' ('+operation.start_date.strftime("%d.%m.%Y")+' - '+operation.end_date.strftime("%d.%m.%Y")+')')
    except ObjectDoesNotExist:
      pass
    # 2 - The Family is envolved
    try:
      operations = Operation.objects.filter(family=self.family)
      for operation in operations:
        if Operation.opIntersect(operation,self):
          #if an other carer is already at this family
          raise ValidationError(str(operation.carer)+' is already at '+str(self.family)+
            ' ('+operation.start_date.strftime("%d.%m.%Y")+' - '+operation.end_date.strftime("%d.%m.%Y")+')')
    except ObjectDoesNotExist:
      pass

  def opIntersect(op1, op2):
    return (op1.start_date < op2.start_date < op1.end_date) or (op1.start_date < op2.end_date < op1.end_date)

  class Meta:
    permissions = (('operationCreateDelete', 'Create or Delete'),)

class FamilyPayment(models.Model):
  family = models.ForeignKey(Family)
  family_pays = models.IntegerField()

  class Meta:
      permissions = (('familyPaymentView', 'View Family Payment'),)

class CarerPayment(models.Model):

  PAYMENT_METHODS = (
    (1, 'Cash'),
    (2, 'Bank Transaction'),
  )

  carer = models.ForeignKey(Carer)
  date = models.DateField(null=False, blank=False)
  amount = models.IntegerField(null=False, blank=False)
  method = models.IntegerField(default=1, choices=PAYMENT_METHODS, blank=False)

  class Meta:
    permissions = (('carerPaymentView', 'View Carer Payment'),)

class TradeRegister(models.Model):

  ACTIONS = (
    (1, 'IN'),
    (2, 'OUT'),
  )

  carer = models.ForeignKey(Carer)
  date = models.DateField(null=False, blank=False)
  action = models.IntegerField(default=1, choices=ACTIONS, blank=False)
