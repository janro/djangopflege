from urlparse import urlparse, urlunparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.template import RequestContext
#from django.utils.http import is_safe_url
#from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site


@login_required
def index(request):
  return render_to_response('index.html',
  {},
  context_instance=RequestContext(request))

@login_required
def logoutView(request):
  auth_logout(request)
  logged_out = 1
  return render_to_response('login.html',
    {'logged_out' : logged_out, },
    context_instance=RequestContext(request))

def testView(request):
  import datetime
  t = datetime.datetime.now()
  return render_to_response('testpage.html',
    {'t':t},
    context_instance=RequestContext(request))