from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('profipflege.views',
    #(r'^$', 'index'),
    (r'^logout/', 'logoutView'),
    (r'^login2/', 'loginView'),
)

urlpatterns += patterns('',

    # root page is cadmin summary (was index above)
    (r'^$', 'cadmin.views.summary'),

    # cadmin app
    (r'^ca/', include('cadmin.urls')),

    # admin app
    (r'^admin/', include(admin.site.urls)),

    # etc
    #(r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #(r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}),
)
