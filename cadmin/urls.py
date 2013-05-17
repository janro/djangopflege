from django.conf.urls import patterns, include, url

from cadmin import views

urlpatterns = patterns('cadmin.views',
    
    (r'^$', 'summary'),

    # family section
    (r'^f/$', 'familyList'),
    (r'^f/archive/$', 'familyArchiveList'),
    (r'^f/edit/$', 'familyCreateForm'),
    (r'^f/(?P<family_id>\d+)/$', 'familyDetails'),
    (r'^f/(?P<family_id>\d+)/delete/$', 'familyDelete'),
    (r'^f/(?P<family_id>\d+)/archive/$', 'familyArchive'),
    (r'^f/(?P<family_id>\d+)/activate/$', 'familyActivate'),
    (r'^f/(?P<family_id>\d+)/edit/$', 'familyUpdateForm'),
    (r'^f/(?P<family_id>\d+)/pm/add/$', 'familyPaymentAddForm'),
    (r'^f/(?P<family_id>\d+)/pm/(?P<payment_id>\d+)/delete/$', 'familyPaymentDelete'),
    (r'^f/(?P<family_id>\d+)/pm/(?P<payment_id>\d+)/edit/$', 'familyPaymentEditForm'),

    # family ajax load
    (r'^f/(?P<family_id>\d+)/ajax/pm/$','ajaxFamilyPaymentList'),
    (r'^f/(?P<family_id>\d+)/ajax/op/$','ajaxFamilyOperationList'),

    # carer section
    (r'^c/$', 'carerList'),
    (r'^c/new/$', 'newCarerList'),
    (r'^c/archive/$', 'carerArchiveList'),
    (r'^c/edit/$', 'carerCreateForm'),
    (r'^c/(?P<carer_id>\d+)/$', 'carerDetails'),
    (r'^c/(?P<carer_id>\d+)/delete/$', 'carerDelete'),
    (r'^c/(?P<carer_id>\d+)/archive/$', 'carerArchive'),
    (r'^c/(?P<carer_id>\d+)/activate/$', 'carerActivate'),    
    (r'^c/(?P<carer_id>\d+)/edit/$', 'carerUpdateForm'),
    (r'^c/(?P<carer_id>\d+)/pm/add/$', 'carerPaymentAddForm'),
    (r'^c/(?P<carer_id>\d+)/pm/(?P<payment_id>\d+)/delete/$', 'carerPaymentDelete'),
    (r'^c/(?P<carer_id>\d+)/pm/(?P<payment_id>\d+)/edit/$', 'carerPaymentEditForm'),

    # carer ajax load
    (r'^c/(?P<carer_id>\d+)/ajax/pm/$','ajaxCarerPaymentList'),
    (r'^c/(?P<carer_id>\d+)/ajax/op/$','ajaxCarerOperationList'),
    (r'^c/(?P<carer_id>\d+)/ajax/re/$','ajaxCarerRegistrationList'),

    # operations
    (r'^op/$', 'operations'),
    (r'^op/edit/$', 'operationCreateForm'),
    (r'^op/(?P<operation_id>\d+)/delete/$', 'operationDelete'),
    (r'^op/(?P<operation_id>\d+)/edit/$', 'operationUpdateForm'),
)