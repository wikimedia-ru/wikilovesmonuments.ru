# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table('wlm_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('district', self.gf('django.db.models.fields.IntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')(max_length=20, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(max_length=20, null=True, blank=True)),
            ('scale', self.gf('django.db.models.fields.IntegerField')()),
            ('iso_code', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('wlm', ['Region'])

        # Adding model 'City'
        db.create_table('wlm_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wlm.Region'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(max_length=20, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(max_length=20, null=True, blank=True)),
            ('capital', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('wlm', ['City'])

        # Adding model 'Street'
        db.create_table('wlm_street', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wlm.Region'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wlm.City'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('wlm', ['Street'])

        # Adding model 'Monument'
        db.create_table('wlm_monument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wlm.Region'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wlm.City'], null=True, blank=True)),
            ('street', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wlm.Street'], null=True, blank=True)),
            ('coord_lon', self.gf('django.db.models.fields.FloatField')(max_length=20, null=True, blank=True)),
            ('coord_lat', self.gf('django.db.models.fields.FloatField')(max_length=20, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('name_alt', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('complex_root', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wlm.Monument'], null=True, blank=True)),
            ('complex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('extra_info', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('protection', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ruwiki', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('kult_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('wlm', ['Monument'])

        # Adding model 'MonumentPhoto'
        db.create_table('wlm_monumentphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wlm.Monument'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('commons_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('contest_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('folder', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('wlm', ['MonumentPhoto'])

        # Adding model 'MonumentPhotoRating'
        db.create_table('wlm_monumentphotorating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wlm.MonumentPhoto'])),
            ('vote', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('wlm', ['MonumentPhotoRating'])


    def backwards(self, orm):
        # Deleting model 'Region'
        db.delete_table('wlm_region')

        # Deleting model 'City'
        db.delete_table('wlm_city')

        # Deleting model 'Street'
        db.delete_table('wlm_street')

        # Deleting model 'Monument'
        db.delete_table('wlm_monument')

        # Deleting model 'MonumentPhoto'
        db.delete_table('wlm_monumentphoto')

        # Deleting model 'MonumentPhotoRating'
        db.delete_table('wlm_monumentphotorating')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'wlm.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wlm.Region']"})
        },
        'wlm.monument': {
            'Meta': {'object_name': 'Monument'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wlm.City']", 'null': 'True', 'blank': 'True'}),
            'complex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'complex_root': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wlm.Monument']", 'null': 'True', 'blank': 'True'}),
            'coord_lat': ('django.db.models.fields.FloatField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'coord_lon': ('django.db.models.fields.FloatField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'extra_info': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kult_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'name_alt': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'protection': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wlm.Region']"}),
            'ruwiki': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wlm.Street']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'wlm.monumentphoto': {
            'Meta': {'object_name': 'MonumentPhoto'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'commons_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'contest_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'folder': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wlm.Monument']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'wlm.monumentphotorating': {
            'Meta': {'object_name': 'MonumentPhotoRating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wlm.MonumentPhoto']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'wlm.region': {
            'Meta': {'ordering': "['order']", 'object_name': 'Region'},
            'district': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.IntegerField', [], {}),
            'latitude': ('django.db.models.fields.FloatField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'scale': ('django.db.models.fields.IntegerField', [], {})
        },
        'wlm.street': {
            'Meta': {'object_name': 'Street'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wlm.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wlm.Region']"})
        }
    }

    complete_apps = ['wlm']