from django.db import models


class EmailRecipient(models.Model):
    account_number = models.CharField(max_length=200)
    email_recipient = models.EmailField()

    def __unicode__(self):
        return 'Account %s: %s' % (self.account_number, self.email_recipient)


class History(models.Model):
    receipt = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    details = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    msisdn = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'history'

    def __unicode__(self):
        return self.details


class MPesaAccount(models.Model):
    org = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'M-Pesa accounts'

    def __unicode__(self):
        return self.org

