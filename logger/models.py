import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class LogEntry(models.Model):

  ACTIONS = (
    (0,'LOGIN'),
    (1,'ADD'),
    (2,'EDIT'),
    (3,'REMOVE')
  )

  user = models.ForeignKey(User, related_name='auth_user')
  timestamp = models.DateTimeField(null=False, auto_now_add=True, blank=False)
  action = models.IntegerField(null=False, default=0, choices=ACTIONS, blank=False)
  comment = models.CharField(max_length=50, blank=True)

  def save(self, *args, **kwargs):
    MAX_AGE = 7
    delta = datetime.timedelta(days=MAX_AGE)
    LogEntry.objects.all().filter(timestamp__lt=datetime.datetime.now()-delta).delete()
    super(LogEntry, self).save(*args, **kwargs) # Call the "real" save() method.

  def logLogin(sender, user, request, **kwargs):
    log_entry = LogEntry(user=user, action=0, timestamp=datetime.datetime.now())
    log_entry.save()

  user_logged_in.connect(logLogin)

  class Meta:
    ordering = ["-timestamp"]
    permissions = (('logs', 'View Log'),)