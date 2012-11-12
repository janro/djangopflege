from django.conf.urls import patterns, include, url

urlpatterns = patterns('pflegeadmin.views',
    url(r'^$', 'summary'),
    url(r'^f/$', 'familyList'),
    url(r'^f/add/$', 'familyAdd'),
    url(r'^f/new/$', 'familySaveNew'),
    url(r'^f/edit2/$', 'familyCreateForm'),
    url(r'^f/(?P<family_id>\d+)/edit2/$', 'familyUpdateForm'),
    url(r'^f/(?P<family_id>\d+)/$', 'familyDetails'),
    url(r'^f/(?P<family_id>\d+)/edit/$', 'familyEdit'),
    url(r'^f/(?P<family_id>\d+)/delete/$', 'familyDelete'),
    url(r'^f/(?P<family_id>\d+)/save/$', 'familySaveExisting'),
)
