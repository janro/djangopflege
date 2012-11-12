from django.conf.urls import patterns, include, url

urlpatterns = patterns('pflegeadmin.views',
    url(r'^$', 'summary'),
    url(r'^f/$', 'familyList'),
    url(r'^f/edit/$', 'familyCreateForm'),
    url(r'^f/(?P<family_id>\d+)/edit/$', 'familyUpdateForm'),
    url(r'^f/(?P<family_id>\d+)/$', 'familyDetails'),
    url(r'^f/(?P<family_id>\d+)/delete/$', 'familyDelete'),
)
