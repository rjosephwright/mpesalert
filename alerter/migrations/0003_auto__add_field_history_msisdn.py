# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'History.msisdn'
        db.add_column('alerter_history', 'msisdn',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'History.msisdn'
        db.delete_column('alerter_history', 'msisdn')


    models = {
        'alerter.emailrecipient': {
            'Meta': {'object_name': 'EmailRecipient'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email_recipient': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'alerter.history': {
            'Meta': {'object_name': 'History'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '50', 'decimal_places': '2'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msisdn': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'receipt': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'alerter.mpesaaccount': {
            'Meta': {'object_name': 'MPesaAccount'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['alerter']