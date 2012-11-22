from django.shortcuts import render_to_response, get_object_or_404
from django.shortcuts import render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from cadmin.forms import FamilyForm, CarerForm
from cadmin.models import Carer, Family, Care

import datetime

@login_required
def summary(request):
  family_count = Family.objects.all().count()
  carer_count = Carer.objects.all().count()
  care_count = Care.objects.filter(
    start_date__lte = datetime.date.today()).filter(
    end_date__gte = datetime.date.today()).count()

  arrival_list = Care.objects.filter(start_date__gte = datetime.date.today()).order_by('-start_date')[0:5]
  departure_list = Care.objects.filter(end_date__gte = datetime.date.today()).order_by('-end_date')[0:5]
  return render_to_response('cadmin/summary.html',
    {'carer_count' : carer_count,
     'family_count' : family_count,
     'care_count' : care_count,
     'arrival_list' : arrival_list,
     'departure_list' : departure_list},
    context_instance=RequestContext(request))

@login_required
def familyList(request):
  family_list = Family.objects.all();
  return render_to_response('cadmin/familyList.html',
    {'family_list' : family_list},
    context_instance=RequestContext(request))

@login_required
def carerList(request):
  carer_list = Carer.objects.all();
  return render_to_response('cadmin/carerList.html',
    {'carer_list' : carer_list},
    context_instance=RequestContext(request))

@login_required
def familyDetails(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  try:
    care_list = Care.objects.filter(family=family_id).order_by('-start_date')
  except ObjectDoesNotExist:
    care_list = {}
  return render_to_response('cadmin/familyDetails.html',
      {'family' : family, 'care_list' : care_list},
      context_instance=RequestContext(request))

@login_required
def carerDetails(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  try:
    care_list = Care.objects.filter(carer=carer_id).order_by('-start_date')
  except ObjectDoesNotExist:
    care_list = {}
  return render_to_response('cadmin/carerDetails.html',
      {'carer' : carer, 'care_list' : care_list},
      context_instance=RequestContext(request))

@permission_required('cadmin.familyCreateDelete', raise_exception=True)
def familyDelete(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  family.delete()
  return HttpResponseRedirect('/cadmin/f/')

@permission_required('cadmin.carerCreateDelete', raise_exception=True)
def carerDelete(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  carer.delete()
  return HttpResponseRedirect('/cadmin/c/')

@permission_required('cadmin.familyCreateDelete', raise_exception=True)
def familyUpdateForm(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  if request.method == 'POST':
    form = FamilyForm(request.POST, instance=family)
    if form.is_valid():
      family = form.save()
      return HttpResponseRedirect('/cadmin/f/'+str(family.id))
  else:
    form = FamilyForm(instance=family)
  return render_to_response('cadmin/familyForm.html',
    {'form': form, 'family' : family, },
    context_instance=RequestContext(request))

@login_required
def carerUpdateForm(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  if request.method == 'POST':
    form = CarerForm(request.POST, instance=carer)
    if form.is_valid():
      carer = form.save()
      return HttpResponseRedirect('/cadmin/c/'+str(carer.id))
  else:
    form = CarerForm(instance=carer)
  return render_to_response('cadmin/carerForm.html',
    {'form': form, 'carer' : carer, },
    context_instance=RequestContext(request))

@permission_required('cadmin.carerCreateDelete', raise_exception=True)
def familyCreateForm(request):
  if request.method == 'POST':
    form = FamilyForm(request.POST)
    if form.is_valid():
      family = form.save()
      return HttpResponseRedirect('/cadmin/f/'+str(family.id))
  else:
    form = FamilyForm()
  return render_to_response('cadmin/familyForm.html',
    {'form': form, },
    context_instance=RequestContext(request))

@login_required
def carerCreateForm(request):
  if request.method == 'POST':
    form = CarerForm(request.POST)
    if form.is_valid():
      carer = form.save()
      return HttpResponseRedirect('/cadmin/c/'+str(carer.id))
  else:
    form = CarerForm()
  return render_to_response('cadmin/carerForm.html',
    {'form': form, },
    context_instance=RequestContext(request))