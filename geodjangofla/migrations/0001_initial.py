# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Region'
        db.create_table('geodjangofla_region', (
            ('id_geofla', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('code_reg', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('nom_region', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('geodjangofla', ['Region'])

        # Adding model 'Departement'
        db.create_table('geodjangofla_departement', (
            ('id_geofla', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('code_dept', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('nom_dept', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('code_chf', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('nom_chf', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('chf_lieu', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('centroid', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('limite', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geodjangofla.Region'], null=True, blank=True)),
        ))
        db.send_create_signal('geodjangofla', ['Departement'])

        # Adding model 'Arrondissement'
        db.create_table('geodjangofla_arrondissement', (
            ('id_geofla', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('departement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geodjangofla.Departement'], null=True, blank=True)),
            ('code_arr', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('code_chf', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('nom_chf', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('chf_lieu', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('centroid', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('limite', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
        ))
        db.send_create_signal('geodjangofla', ['Arrondissement'])

        # Adding model 'Canton'
        db.create_table('geodjangofla_canton', (
            ('id_geofla', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('departement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geodjangofla.Departement'], null=True, blank=True)),
            ('code_cant', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('code_chf', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('nom_chf', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('chf_lieu', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('centroid', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('limite', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('arrondissement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geodjangofla.Arrondissement'], null=True, blank=True)),
        ))
        db.send_create_signal('geodjangofla', ['Canton'])

        # Adding model 'Commune'
        db.create_table('geodjangofla_commune', (
            ('id_geofla', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('code_comm', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('insee_com', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('nom_comm', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('statut', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('chf_lieu', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('centroid', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('z_moyen', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('superficie', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('population', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('limite', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('canton', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geodjangofla.Canton'], null=True, blank=True)),
        ))
        db.send_create_signal('geodjangofla', ['Commune'])


    def backwards(self, orm):
        
        # Deleting model 'Region'
        db.delete_table('geodjangofla_region')

        # Deleting model 'Departement'
        db.delete_table('geodjangofla_departement')

        # Deleting model 'Arrondissement'
        db.delete_table('geodjangofla_arrondissement')

        # Deleting model 'Canton'
        db.delete_table('geodjangofla_canton')

        # Deleting model 'Commune'
        db.delete_table('geodjangofla_commune')


    models = {
        'geodjangofla.arrondissement': {
            'Meta': {'object_name': 'Arrondissement'},
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'chf_lieu': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'code_arr': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'code_chf': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'departement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geodjangofla.Departement']", 'null': 'True', 'blank': 'True'}),
            'id_geofla': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'limite': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'nom_chf': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'geodjangofla.canton': {
            'Meta': {'object_name': 'Canton'},
            'arrondissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geodjangofla.Arrondissement']", 'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'chf_lieu': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'code_cant': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'code_chf': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'departement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geodjangofla.Departement']", 'null': 'True', 'blank': 'True'}),
            'id_geofla': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'limite': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'nom_chf': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'geodjangofla.commune': {
            'Meta': {'object_name': 'Commune'},
            'canton': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geodjangofla.Canton']", 'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'chf_lieu': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'code_comm': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id_geofla': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'insee_com': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'limite': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'nom_comm': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'statut': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'superficie': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'z_moyen': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'geodjangofla.departement': {
            'Meta': {'object_name': 'Departement'},
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'chf_lieu': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'code_chf': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'code_dept': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id_geofla': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'limite': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'nom_chf': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'nom_dept': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geodjangofla.Region']", 'null': 'True', 'blank': 'True'})
        },
        'geodjangofla.region': {
            'Meta': {'object_name': 'Region'},
            'code_reg': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id_geofla': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom_region': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['geodjangofla']
