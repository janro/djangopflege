from django.db import models

class Carer(models.Model):
  firstname = models.CharField(max_length=100)
  lastname = models.CharField(max_length=100)
  date_of_birth = models.DateField()
  hometown = models.CharField(max_length=100)
  family = models.CharField(max_length=100)
  language_skills = models.IntegerField()
  care_skills = models.IntegerField()
  weight = models.IntegerField()
  smoker = models.BooleanField()
  trade_registered = models.BooleanField()
  remark = models.CharField(max_length=500)
  phone = models.CharField(max_length=20)


firstname_contact_person
lastname_contact_person
phone_contact_person

class Family(models.Model):
  firstname_contact_person = models.CharField(max_length=100, null=True, blank=True)
  lastname_contact_person = models.CharField(max_length=100, null=True, blank=True)
  phone_contact_person = models.CharField(max_length=20, null=True, blank=True)
  firstname_care_person = models.CharField(max_length=100, null=True, blank=True)
  lastname_care_person = models.CharField(max_length=100, null=True, blank=True)
  phone_care_person = models.CharField(max_length=20, null=True, blank=True)
  street = models.CharField(max_length=100, null=True, blank=True)
  number = models.IntegerField(null=True, blank=True)
  postal_code = models.IntegerField(null=True, blank=True)
  city = models.CharField(max_length=100, null=True, blank=True)
  care_level = models.IntegerField(null=True, blank=True)
  date_of_birth = models.DateField(null=True, blank=True)

class Care(models.Model):
  carer = models.ForeignKey(Carer)
  family = models.ForeignKey(Family)
  start_date = models.DateField()
  end_date = models.DateField()


class FamilyPayment(models.Model):
  family = models.ForeignKey(Family)
  family_pays = models.IntegerField()

  class Meta:
      permissions = (("familyPayment_level1", "View Family Payment"), )

class CarerPayment(models.Model):
  carer = models.ForeignKey(Carer)
  amount = models.IntegerField()
  date = models.DateField()

  class Meta:
    permissions = (("carerPayment_level1", "View Carer Payment"), )
