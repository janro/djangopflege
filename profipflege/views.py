from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
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

# def login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             # Redirect to a success page.
#         else:
#             # Return a 'disabled account' error message
#     else:
#         # Return an 'invalid login' error message.