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

class Family(models.Model):
  firstname_contact_p = models.CharField(max_length=100, null=True)
  lastname_contact_p = models.CharField(max_length=100, null=True)
  phone_contact_p = models.CharField(max_length=20, null=True)
  firstname_care_p = models.CharField(max_length=100, null=True)
  lastname_care_p = models.CharField(max_length=100, null=True)
  phone_care_p = models.CharField(max_length=20, null=True)
  address_street = models.CharField(max_length=100, null=True)
  address_number = models.IntegerField(null=True)
  address_postal = models.IntegerField(null=True)
  address_town = models.CharField(max_length=100, null=True)
  care_level = models.IntegerField(null=True)
  date_of_birth = models.DateField(null=True)

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
