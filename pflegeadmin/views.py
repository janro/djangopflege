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
def familyDelete(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  family.delete()
  return HttpResponseRedirect('/pflegeadmin/f/')

@login_required
def familyUpdateForm(request, family_id):
  
  family = get_object_or_404(Family, pk=family_id)

  if request.method == 'POST':
    form = FamilyForm(request.POST, instance=family)
    if form.is_valid():
      family = form.save()
      return HttpResponseRedirect('/pflegeadmin/f/'+str(family.id))
  else:
    form = FamilyForm(instance=family)

  return render_to_response('pflegeadmin/familyForm.html',
    {'form': form, 'family' : family, },
    context_instance=RequestContext(request))

@login_required
def familyCreateForm(request):

  if request.method == 'POST':
    form = FamilyForm(request.POST)
    if form.is_valid():
      family = form.save()
      return HttpResponseRedirect('/pflegeadmin/f/'+str(family.id))
  else:
    form = FamilyForm()

  return render_to_response('pflegeadmin/familyForm.html',
    {'form': form, },
    context_instance=RequestContext(request))