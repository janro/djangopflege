from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^pflegeadmin/', include('pflegeadmin.urls')),
    url(r'^admin/', include(admin.site.urls)),

    (r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
)
