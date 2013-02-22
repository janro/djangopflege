from logger.models import LogEntry
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.shortcuts import render_to_response

@permission_required('logger.logs', raise_exception=True)
def logView(request):
  log_list = LogEntry.objects.all().order_by('-timestamp')
  return render_to_response('logger/log.html',
    {'log_list' : log_list},
    context_instance=RequestContext(request))
