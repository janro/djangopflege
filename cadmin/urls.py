from django.conf.urls import patterns, include, url

urlpatterns = patterns('cadmin.views',
    url(r'^/$', 'summary', name='summary'),

    # family section
    url(r'^f/$', 'familyList'),
    url(r'^f/edit/$', 'familyCreateForm'),
    url(r'^f/(?P<family_id>\d+)/edit/$', 'familyUpdateForm'),
    url(r'^f/(?P<family_id>\d+)/$', 'familyDetails'),
    url(r'^f/(?P<family_id>\d+)/delete/$', 'familyDelete'),

    # carer section
    url(r'^c/$', 'carerList'),
    url(r'^c/edit/$', 'carerCreateForm'),
    url(r'^c/(?P<carer_id>\d+)/edit/$', 'carerUpdateForm'),
    url(r'^c/(?P<carer_id>\d+)/$', 'carerDetails'),
    url(r'^c/(?P<carer_id>\d+)/delete/$', 'carerDelete'),    
)
