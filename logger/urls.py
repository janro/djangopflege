from django.conf.urls import patterns, include, url

urlpatterns = patterns('logger.views',
    
    (r'^$', 'logView'),

)