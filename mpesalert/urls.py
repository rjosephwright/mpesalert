from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import django_cron
django_cron.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpesalert.views.home', name='home'),
    # url(r'^mpesalert/', include('mpesalert.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
