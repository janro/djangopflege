from django.db import models

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
  # care_skills
  # remark

  SKILL_LEVELS = (
    (1, 'Skill Level 1'),
    (2, 'Skill Level 2'),
    (3, 'Skill Level 3'),
    (4, 'Skill Level 4'),
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
  care_skills = models.IntegerField(default=1, choices=SKILL_LEVELS, blank=True)
  remark = models.CharField(max_length=500, null=True, blank=True)

  
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

  CARE_LEVELS = (
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3, 'Level 3'),
    (4, 'Level 4'),
  )
  
  firstname_contact_person = models.CharField(max_length=100, null=True, blank=True)
  lastname_contact_person = models.CharField(max_length=100, null=True, blank=False)
  phone_contact_person = models.CharField(max_length=20, null=True, blank=False)
  firstname_care_person = models.CharField(max_length=100, null=True, blank=True)
  lastname_care_person = models.CharField(max_length=100, null=True, blank=True)
  phone_care_person = models.CharField(max_length=20, null=True, blank=True)
  street = models.CharField(max_length=100, null=True, blank=True)
  number = models.IntegerField(null=True, blank=True)
  postal_code = models.IntegerField(null=True, blank=True)
  city = models.CharField(max_length=100, null=True, blank=True)
  care_level = models.IntegerField(default=1, choices=CARE_LEVELS, blank=True)
  date_of_birth = models.DateField(null=True, blank=True)

  class Meta:
      permissions = (('familyCreateDelete', 'Create or Delete'),)

class Care(models.Model):
  carer = models.ForeignKey(Carer)
  family = models.ForeignKey(Family)
  start_date = models.DateField()
  end_date = models.DateField()


class FamilyPayment(models.Model):
  family = models.ForeignKey(Family)
  family_pays = models.IntegerField()

  class Meta:
      permissions = (('familyPayment_level1', 'View Family Payment'),)

class CarerPayment(models.Model):
  carer = models.ForeignKey(Carer)
  amount = models.IntegerField()
  date = models.DateField()

  class Meta:
    permissions = (('carerPayment_level1', 'View Carer Payment'),)
