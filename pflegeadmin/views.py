from django.shortcuts import render_to_response, get_object_or_404
from django.shortcuts import render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

from pflegeadmin.forms import FamilyForm
from pflegeadmin.models import Carer, Family

@login_required
def summary(request):
  family_count = Family.objects.all().count();
  carer_count = Carer.objects.all().count();
  return render_to_response('pflegeadmin/summary.html',
    {'carer_count' : carer_count,
    'family_count' : family_count},
    context_instance=RequestContext(request))

@login_required
def familyList(request):
  family_list = Family.objects.all();
  return render_to_response('pflegeadmin/familyList.html',
    {'family_list' : family_list},
    context_instance=RequestContext(request))

@login_required
def familyDetails(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  return render_to_response('pflegeadmin/familyDetails.html',
      {'family' : family},
      context_instance=RequestContext(request))

@login_required
def familyEdit(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  return render_to_response('pflegeadmin/familyEdit.html',
      {'family' : family},
      context_instance=RequestContext(request))

@login_required
def familySaveExisting(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  family_id = __SaveFamilyData(request, family)
  return HttpResponseRedirect('/pflegeadmin/f/'+family_id)

@login_required
def familySaveNew(request):
  family = Family()
  family_id = __SaveFamilyData(request, family)
  return HttpResponseRedirect('/pflegeadmin/f/'+family_id)

@login_required
def familyDelete(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  family.delete()
  return HttpResponseRedirect('/pflegeadmin/f/')

@login_required
def familyAdd(request):
  return render_to_response('pflegeadmin/familyAdd.html',
      {},
      context_instance=RequestContext(request))

@login_required
def familyUpdateForm(request, family_id):

  family = get_object_or_404(Family, pk=family_id)


  if request.method == 'POST':
    form = FamilyForm(request.POST) # A form bound to the POST data
    if form.is_valid():
      # All validation rules pass
      # Process the data in form.cleaned_data
      # ...
      family = form.save()
      #family.id=family_id
      #family.save()
      return HttpResponseRedirect('/pflegeadmin/f/'+str(family.id))
  else:
    form = FamilyForm(instance=family)

  return render(request, 'pflegeadmin/familyForm.html',{'form': form, 'family' : family, })

@login_required
def familyCreateForm(request):

  if request.method == 'POST':
    form = FamilyForm(request.POST) # A form bound to the POST data
    if form.is_valid():
      # All validation rules pass
      # Process the data in form.cleaned_data
      # ...
      family = form.save()
      family.save()
      return HttpResponseRedirect('/pflegeadmin/f/'+str(family.id))
  else:
    form = FamilyForm()

  return render(request, 'pflegeadmin/familyForm.html',{'form': form, })


def __SaveFamilyData(request, family):
  family.firstname_care_p = request.POST.get('firstname_care_p',family.firstname_care_p)
  family.lastname_care_p = request.POST.get('lastname_care_p',family.lastname_care_p)
  family.firstname_contact_p = request.POST.get('firstname_contact_p',family.firstname_contact_p)
  family.lastname_contact_p = request.POST.get('lastname_contact_p',family.lastname_contact_p)
  #family.phone_contact_p = request.POST.get('phone_contact_p',family.phone_contact_p)
  #family.phone_care_p = request.POST.get('phone_care_p',family.phone_care_p)
  #family.address_street = request.POST.get('address_street',family.address_street)
  #family.address_number = request.POST.get('address_number',family.address_number)
  #family.address_postal = request.POST.get('address_postal',family.address_postal)
  #family.address_town = request.POST.get('address_town',family.address_town)
  foo = request.POST.get('care_level','0')
  print foo

  try: bar = int(request.POST.get("care_level", '1'))
  except ValueError: bar = 0
  print bar
  family.care_level = int(bar)
  #family.date_of_birth = request.POST.get('date_of_birth',family.date_of_birth)
  family.save()
  return str(family.id);
