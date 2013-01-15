from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
  return render_to_response('index.html',
  {},
  context_instance=RequestContext(request))

@login_required
def logoutView(request):
  logout(request)
  logged_out = 1
  return render_to_response('login.html',
    {'logged_out' : logged_out, },
    context_instance=RequestContext(request))

def loginView(request):
  if request.method == 'POST':
    form = AuthenticationForm(request.POST)
    if form.is_valid():
      print('valid')
      return HttpResponseRedirect(reverse('cadmin.views.summary'))
    else:
      print('invalid')
  else:
    form = AuthenticationForm()
  return render_to_response('login2.html',
    {'form' : form, },
    context_instance=RequestContext(request))
