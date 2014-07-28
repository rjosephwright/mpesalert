from django.contrib.sites.models import Site
from alerter.models import MPesaAccount, EmailRecipient, History
from django.contrib import admin


admin.site.register(MPesaAccount)
admin.site.register(EmailRecipient)
admin.site.register(History)
admin.site.unregister(Site)
