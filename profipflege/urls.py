from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('profipflege.views',
    #(r'^$', 'index'),
    (r'^logout/', 'logoutView'),
    (r'^test/', 'testView'),
)

urlpatterns += patterns('',

    # root page is cadmin summary (was index above)
    (r'^$', 'cadmin.views.summary'),

    # cadmin app
    (r'^ca/', include('cadmin.urls')),

    # logger app
    (r'^log/', include('logger.urls')),

    # admin app
    (r'^admin/', include(admin.site.urls)),

    # etc
    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #(r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}),
)
