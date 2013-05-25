from django.shortcuts import render_to_response, get_object_or_404
from django.shortcuts import render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from cadmin.forms import FamilyForm, CarerForm, OperationForm, CarerPaymentForm, FamilyPaymentForm
from cadmin.models import Carer, Family, Operation, CarerPayment, TradeRegister, FamilyPayment

from logger.models import LogEntry

import datetime

@login_required
def summary(request):
  family_count = Family.objects.all().filter(archive=False).count()
  family_archive_count = Family.objects.all().filter(archive=True).count()
  carer_count = Carer.objects.all().filter(archive=False).count()
  carer_archive_count = Carer.objects.all().filter(archive=True).count()

  # start < today <= end
  operation_count = Operation.objects.filter(
    start_date__lte = datetime.date.today()).filter(
    end_date__gte = datetime.date.today()).count()

  # start < today <= n.A.
  operation_count += Operation.objects.filter(
    start_date__lte = datetime.date.today()).filter(
    end_date=None).count()

  arrival_list = Operation.objects.filter(start_date__gte = datetime.date.today()).order_by('start_date')[0:10]
  departure_list = Operation.objects.filter(end_date__gte = datetime.date.today()).order_by('end_date')[0:10]
  return render_to_response('cadmin/summary.html',
    {'carer_count' : carer_count,
     'carer_archive_count' : carer_archive_count,
     'family_count' : family_count,
     'family_archive_count' : family_archive_count,
     'operation_count' : operation_count,
     'arrival_list' : arrival_list,
     'departure_list' : departure_list},
    context_instance=RequestContext(request))

@login_required
def familyList(request):
  family_list = Family.objects.all().order_by('lastname_care_person').filter(archive=False)
  return render_to_response('cadmin/familyList.html',
    {'family_list' : family_list},
    context_instance=RequestContext(request))

@login_required
def carerList(request):
  carer_list = Carer.objects.all().order_by('lastname').filter(archive=False)
  return render_to_response('cadmin/carerList.html',
    {'carer_list' : carer_list},
    context_instance=RequestContext(request))

@login_required
def newCarerList(request):
  
  from itertools import chain
  # start < today <= end
  set1 = Operation.objects.filter(
    start_date__lte = datetime.date.today(), end_date__gte = datetime.date.today()).values_list('carer_id', flat=True)
  # start < today <= n.A.
  set2 = Operation.objects.filter(start_date__lte = datetime.date.today(), end_date=None).values_list('carer_id', flat=True)

  set3 = list(chain(set1,set2))
  

  active_carers = Carer.objects.filter(archive=False).filter(pk__in=set3).order_by('lastname')
  inactive_carers = Carer.objects.filter(archive=False).exclude(pk__in=set3).order_by('lastname')
  
  return render_to_response('cadmin/newCarerList.html',
    {'active_carers' : active_carers,
     'inactive_carers' : inactive_carers,
    },
    context_instance=RequestContext(request))

@login_required
def familyDetails(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  try:
    operation_list = Operation.objects.filter(family=family_id).order_by('-start_date')
  except ObjectDoesNotExist:
    operation_list = {}
  return render_to_response('cadmin/familyDetails.html',
      {'family' : family, 'operation_list' : operation_list},
      context_instance=RequestContext(request))

@login_required
def carerDetails(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  return render_to_response('cadmin/carerDetails.html',
      {'carer' : carer},
      context_instance=RequestContext(request))

@permission_required('cadmin.familyCreateDelete', raise_exception=True)
def familyDelete(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  # delete operations and payments!!

  # delete all operation entries belonging to this family
  try:
    operation_list = Operation.objects.filter(family=family_id)
  except ObjectDoesNotExist:
    operation_list = {}

  for operation in operation_list:
    operation.delete()

  # delete all payment entries belonging to this family
  try:
    payment_list = FamilyPayment.objects.filter(family=family_id)
  except ObjectDoesNotExist:
    payment_list = {}

  for payment in payment_list:
    payment.delete()


  # finally delete the family
  family.delete()
  LogEntry(user=request.user, action=3, comment=str(family)).save()
  messages.add_message(request, messages.INFO, 'Eintrag geloescht!')
  return HttpResponseRedirect(
    reverse('cadmin.views.familyList', ))

@permission_required('cadmin.carerCreateDelete', raise_exception=True)
def carerDelete(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  #delete operations and payments!!

  # delete all operation entries belonging to this carer
  try:
    operation_list = Operation.objects.filter(carer=carer_id)
  except ObjectDoesNotExist:
    operation_list = {}

  for operation in operation_list:
    operation.delete()

  # delete all payments entries belonging to this carer
  try:
    payment_list = CarerPayment.objects.filter(carer=carer_id)
  except ObjectDoesNotExist:
    payment_list = {}

  for payment in payment_list:
    payment.delete()

  # finally delete the carer
  carer.delete()
  LogEntry(user=request.user, action=3, comment=str(carer)).save()
  messages.add_message(request, messages.INFO, 'Eintrag geloescht!')
  return HttpResponseRedirect(
    reverse('cadmin.views.carerList', ))

#--------------------- Carer Archive Methods ----------------------------------
@permission_required('cadmin.carerCreateDelete', raise_exception=True)
def carerArchive(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  carer.archive = True
  carer.save()
  messages.add_message(request, messages.INFO, 'Eintrag archivierd!')
  return HttpResponseRedirect(
        reverse('cadmin.views.carerList'))

@permission_required('cadmin.carerCreateDelete', raise_exception=True)
def carerActivate(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  carer.archive = False
  carer.save()
  messages.add_message(request, messages.INFO, 'Eintrag reaktiviert!')
  return HttpResponseRedirect(
        reverse('cadmin.views.carerArchiveList'))

@login_required
def carerArchiveList(request):
  carer_list = Carer.objects.all().order_by('lastname').filter(archive=True)
  return render_to_response('cadmin/carerList.html',
    {'carer_list' : carer_list, 'archive' : True},
    context_instance=RequestContext(request))

#--------------------- Family Archive Methods ---------------------------------
@permission_required('cadmin.carerCreateDelete', raise_exception=True)
def familyArchive(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  family.archive = True
  family.save()
  messages.add_message(request, messages.INFO, 'Eintrag archivierd!')
  return HttpResponseRedirect(
        reverse('cadmin.views.familyList'))

@permission_required('cadmin.carerCreateDelete', raise_exception=True)
def familyActivate(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  family.archive = False
  family.save()
  messages.add_message(request, messages.INFO, 'Eintrag reaktiviert!')
  return HttpResponseRedirect(
        reverse('cadmin.views.familyArchiveList'))

@login_required
def familyArchiveList(request):
  family_list = Family.objects.all().order_by('lastname_care_person').filter(archive=True)
  return render_to_response('cadmin/familyList.html',
    {'family_list' : family_list, 'archive' : True},
    context_instance=RequestContext(request))

#------------------------------------------------------------------------------
@permission_required('cadmin.familyCreateDelete', raise_exception=True)
def familyUpdateForm(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  if request.method == 'POST':
    form = FamilyForm(request.POST, instance=family)
    if form.is_valid():
      family = form.save()
      LogEntry(user=request.user, action=2, comment=str(family)).save()
      return HttpResponseRedirect(
        reverse('cadmin.views.familyDetails', args=(family.id,)))
  else:
    form = FamilyForm(instance=family)
  return render_to_response('cadmin/forms/familyForm.html',
    {'form': form, 'family' : family, },
    context_instance=RequestContext(request))

@login_required
def carerUpdateForm(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  if request.method == 'POST':
    form = CarerForm(request.POST, instance=carer)
    if form.is_valid():
      carer = form.save()
      LogEntry(user=request.user, action=2, comment=str(carer)).save()
      return HttpResponseRedirect(
        reverse('cadmin.views.carerDetails', args=(carer.id,)))
  else:
    form = CarerForm(instance=carer)
  return render_to_response('cadmin/forms/carerForm.html',
    {'form': form, 'carer' : carer, },
    context_instance=RequestContext(request))

@permission_required('cadmin.carerCreateDelete', raise_exception=True)
def familyCreateForm(request):
  if request.method == 'POST':
    form = FamilyForm(request.POST)
    if form.is_valid():
      family = form.save()
      LogEntry(user=request.user, action=1, comment=str(family)).save()
      return HttpResponseRedirect(
        reverse('cadmin.views.familyDetails', args=(family.id,)))
  else:
    form = FamilyForm()
  return render_to_response('cadmin/forms/familyForm.html',
    {'form': form, },
    context_instance=RequestContext(request))

@login_required
def carerCreateForm(request):
  if request.method == 'POST':
    form = CarerForm(request.POST)
    if form.is_valid():
      carer = form.save()
      LogEntry(user=request.user, action=1, comment=str(carer)).save()
      return HttpResponseRedirect(
        reverse('cadmin.views.carerDetails', args=(carer.id,)))
  else:
    form = CarerForm()
  return render_to_response('cadmin/forms/carerForm.html',
    {'form': form, },
    context_instance=RequestContext(request))

@login_required
def operationUpdateForm(request, operation_id):
  operation = get_object_or_404(Operation, pk=operation_id)
  if request.method == 'POST':
    form = OperationForm(request.POST, instance=operation)
    if form.is_valid():
      operation = form.save()
      return HttpResponseRedirect(
        reverse('cadmin.views.familyDetails', args=(operation.family.id,)))
  else:
    form = OperationForm(instance=operation)
  return render_to_response('cadmin/forms/operationForm.html',
    {'form': form, 'operation' : operation, },
    context_instance=RequestContext(request))

@permission_required('cadmin.operationCreateDelete', raise_exception=True)
def operationCreateForm(request):
  if request.method == 'POST':
    form = OperationForm(request.POST)
    if form.is_valid():
      operation = form.save()
      return HttpResponseRedirect(
        reverse('cadmin.views.familyDetails', args=(operation.family.id,)))
  else:
    form = OperationForm()
  return render_to_response('cadmin/forms/operationForm.html',
    {'form': form, },
    context_instance=RequestContext(request))

@permission_required('cadmin.operationCreateDelete', raise_exception=True)
def operationDelete(request, operation_id):
  operation = get_object_or_404(Operation, pk=operation_id)
  family_id = operation.family.id
  operation.delete()
  messages.add_message(request, messages.INFO, 'Eintrag geloescht!')
  return HttpResponseRedirect(
    reverse('cadmin.views.familyDetails', args=(family_id,)))

@login_required
def operations(request):
  operationList = Operation.objects.all()
  messages.add_message(request, messages.INFO, 'Noch nicht Verfuegbar!')
  return render_to_response('cadmin/operationPlan.html',
    {'operationList' : operationList, },
    context_instance=RequestContext(request))

@login_required
def ajaxCarerOperationList(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  try:
    operation_list = Operation.objects.filter(carer=carer_id).order_by('-start_date')
  except ObjectDoesNotExist:
    operation_list = {}
  return render_to_response('cadmin/ajax/operationList.html',
      {'operation_list' : operation_list,
       'carer' : carer},
      context_instance=RequestContext(request))

@login_required
def ajaxFamilyOperationList(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  try:
    operation_list = Operation.objects.filter(family=family_id).order_by('-start_date')
  except ObjectDoesNotExist:
    operation_list = {}
  return render_to_response('cadmin/ajax/operationList.html',
      {'operation_list' : operation_list,
       'family' : family},
      context_instance=RequestContext(request))

@permission_required('cadmin.carerPaymentView', raise_exception=True)
def ajaxCarerPaymentList(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  try:
    payment_list = CarerPayment.objects.filter(carer=carer_id).order_by('-date')
  except ObjectDoesNotExist:
    payment_list = {}
  return render_to_response('cadmin/ajax/carerPaymentList.html',
      {'payment_list' : payment_list},
      context_instance=RequestContext(request))

@permission_required('cadmin.familyPaymentView', raise_exception=True)
def ajaxFamilyPaymentList(request, family_id):
  family = get_object_or_404(Family, pk=family_id)
  try:
    payment_list = FamilyPayment.objects.filter(family=family_id).order_by('-date')
  except ObjectDoesNotExist:
    payment_list = {}
  return render_to_response('cadmin/ajax/familyPaymentList.html',
      {'payment_list' : payment_list},
      context_instance=RequestContext(request))

@login_required
def ajaxCarerRegistrationList(request, carer_id):
  carer = get_object_or_404(Carer, pk=carer_id)
  try:
    registration_list = TradeRegister.objects.filter(carer=carer_id).order_by('-date')
  except ObjectDoesNotExist:
    registration_list = {}
  return render_to_response('cadmin/ajax/registrationList.html',
      {'registration_list' : registration_list},
      context_instance=RequestContext(request))

@permission_required('cadmin.carerPaymentView', raise_exception=True)
def carerPaymentAddForm(request, carer_id):
  if request.method == 'POST':
    form = CarerPaymentForm(request.POST)
    if form.is_valid():
      carer_payment = form.save()
      return HttpResponseRedirect(
        reverse('cadmin.views.carerDetails', args=(carer_payment.carer.id,)))
  else:
    form = CarerPaymentForm()

  carer = get_object_or_404(Carer, pk=carer_id)
  return render_to_response('cadmin/forms/carerPaymentForm.html',
    {'form': form, 'carer' : carer,},
    context_instance=RequestContext(request))

@permission_required('cadmin.carerPaymentView', raise_exception=True)
def carerPaymentEditForm(request, carer_id, payment_id):
  carer_payment = get_object_or_404(CarerPayment, pk=payment_id)

  if request.method == 'POST':
    form = CarerPaymentForm(request.POST, instance=carer_payment)
    if form.is_valid():
      carer_payment = form.save()
      return HttpResponseRedirect(
        reverse('cadmin.views.carerDetails', args=(carer_payment.carer.id,)))
  else:
    form = CarerPaymentForm(instance=carer_payment)

  carer = get_object_or_404(Carer, pk=carer_id)
  return render_to_response('cadmin/forms/carerPaymentForm.html',
    {'form': form, 'carer' : carer, 'carer_payment' : carer_payment},
    context_instance=RequestContext(request))

@permission_required('cadmin.carerPaymentView', raise_exception=True)
def carerPaymentDelete(request, carer_id, payment_id):
  carer_payment = get_object_or_404(CarerPayment, pk=payment_id)
  carer_id = carer_payment.carer.id
  carer_payment.delete()
  messages.add_message(request, messages.INFO, 'Eintrag geloescht!')
  return HttpResponseRedirect(
    reverse('cadmin.views.carerDetails', args=(carer_payment.carer.id,)))

#-----------------------------------------------------------------------

@permission_required('cadmin.familyPaymentView', raise_exception=True)
def familyPaymentAddForm(request, family_id):
  if request.method == 'POST':
    form = FamilyPaymentForm(request.POST)
    if form.is_valid():
      family_payment = form.save()
      return HttpResponseRedirect(
        reverse('cadmin.views.familyDetails', args=(family_payment.family.id,)))
  else:
    form = FamilyPaymentForm()

  family = get_object_or_404(Family, pk=family_id)
  return render_to_response('cadmin/forms/familyPaymentForm.html',
    {'form': form, 'family' : family,},
    context_instance=RequestContext(request))

@permission_required('cadmin.familyPaymentView', raise_exception=True)
def familyPaymentEditForm(request, family_id, payment_id):
  family_payment = get_object_or_404(FamilyPayment, pk=payment_id)

  if request.method == 'POST':
    form = FamilyPaymentForm(request.POST, instance=family_payment)
    if form.is_valid():
      family_payment = form.save()
      return HttpResponseRedirect(
        reverse('cadmin.views.familyDetails', args=(family_payment.family.id,)))
  else:
    form = FamilyPaymentForm(instance=family_payment)

  family = get_object_or_404(Family, pk=family_id)
  return render_to_response('cadmin/forms/familyPaymentForm.html',
    {'form': form, 'family' : family, 'family_payment' : family_payment},
    context_instance=RequestContext(request))

@permission_required('cadmin.familyPaymentView', raise_exception=True)
def familyPaymentDelete(request, family_id, payment_id):
  family_payment = get_object_or_404(FamilyPayment, pk=payment_id)
  family_id = family_payment.family.id
  family_payment.delete()
  messages.add_message(request, messages.INFO, 'Eintrag geloescht!')
  return HttpResponseRedirect(
    reverse('cadmin.views.familyDetails', args=(family_payment.family.id,)))