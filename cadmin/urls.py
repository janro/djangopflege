from django.conf.urls import patterns, include, url

urlpatterns = patterns('cadmin.views',
    
    (r'^$', 'summary'),

    # family section
    (r'^f/$', 'familyList'),
    (r'^f/edit/$', 'familyCreateForm'),
    (r'^f/(?P<family_id>\d+)/edit/$', 'familyUpdateForm'),
    (r'^f/(?P<family_id>\d+)/$', 'familyDetails'),
    (r'^f/(?P<family_id>\d+)/delete/$', 'familyDelete'),

    # carer section
    (r'^c/$', 'carerList'),
    (r'^c/edit/$', 'carerCreateForm'),
    (r'^c/(?P<carer_id>\d+)/edit/$', 'carerUpdateForm'),
    (r'^c/(?P<carer_id>\d+)/$', 'carerDetails'),
    (r'^c/(?P<carer_id>\d+)/delete/$', 'carerDelete'),    
    (r'^c/(?P<carer_id>\d+)/pm/add/$', 'carerPaymentAddForm'),
    (r'^c/(?P<carer_id>\d+)/pm/(?P<payment_id>\d+)/edit/$', 'carerPaymentEditForm'),
    (r'^c/(?P<carer_id>\d+)/pm/(?P<payment_id>\d+)/delete/$', 'carerPaymentDelete'),

    # carer ajax load
    (r'^c/(?P<carer_id>\d+)/ajax/op/$','ajaxCarerOperationList'),
    (r'^c/(?P<carer_id>\d+)/ajax/pm/$','ajaxCarerPaymentList'),
    (r'^c/(?P<carer_id>\d+)/ajax/re/$','ajaxCarerRegistrationList'),

    # operations
    (r'^op/$', 'operations'),
    (r'^op/edit/$', 'operationCreateForm'),
    (r'^op/(?P<operation_id>\d+)/edit/$', 'operationUpdateForm'),
    (r'^op/(?P<operation_id>\d+)/delete/$', 'operationDelete'),
)