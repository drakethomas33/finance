# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'finance_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('initial_currency', self.gf('djmoney.models.fields.CurrencyField')(default='GBP')),
            ('initial', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='GBP')),
        ))
        db.send_create_signal(u'finance', ['Account'])

        # Adding model 'Category'
        db.create_table(u'finance_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Category'], null=True, blank=True)),
        ))
        db.send_create_signal(u'finance', ['Category'])

        # Adding model 'Transaction'
        db.create_table(u'finance_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='GBP')),
            ('amount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='GBP')),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Category'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Account'])),
        ))
        db.send_create_signal(u'finance', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'finance_account')

        # Deleting model 'Category'
        db.delete_table(u'finance_category')

        # Deleting model 'Transaction'
        db.delete_table(u'finance_transaction')


    models = {
        u'finance.account': {
            'Meta': {'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'GBP'"}),
            'initial_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'GBP'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'finance.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Category']", 'null': 'True', 'blank': 'True'})
        },
        u'finance.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Account']"}),
            'amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'GBP'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'GBP'"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Category']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['finance']