# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailRecipient'
        db.create_table('alerter_emailrecipient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email_recipient', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('alerter', ['EmailRecipient'])

        # Adding model 'History'
        db.create_table('alerter_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=50, decimal_places=2)),
        ))
        db.send_create_signal('alerter', ['History'])

        # Adding model 'MPesaAccount'
        db.create_table('alerter_mpesaaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('org', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('account_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('alerter', ['MPesaAccount'])


    def backwards(self, orm):
        # Deleting model 'EmailRecipient'
        db.delete_table('alerter_emailrecipient')

        # Deleting model 'History'
        db.delete_table('alerter_history')

        # Deleting model 'MPesaAccount'
        db.delete_table('alerter_mpesaaccount')


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