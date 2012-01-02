#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is free software; you can redistribute it and/or modify it
# under the terms of the BSD License (see the file COPYING included with
# the distribution).


from geodjangofla import settings

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist

class GEOFLAManager:
    GEOFLAFIELDS = []
    GEOFLA_DBF_FIELDS = []

    @classmethod
    def create_or_update_from_GEOFLA_dict(cls, values):
        dct = {}
        for field_manager in cls.GEOFLAFIELDS:
            dct[field_manager.attr_name] = field_manager.convert(values)
        try:
            instance = cls.objects.get(id_geofla=dct['id_geofla'])
            dct.pop('id_geofla')
            for k in dct:
                setattr(instance, k, dct[k])
            instance.save()
        except ObjectDoesNotExist:
            instance = cls.objects.create(**dct)
        return instance

class GEOFLAFieldManager:
    def __init__(self, geofla_name, attr_name, conv, instance_class=None,
                 choices=[],lax=False):
        self.geofla_name, self.attr_name = geofla_name, attr_name
        self.lax, self.instance_class = lax, instance_class
        if callable(conv):
            self.conv = conv
        else:
            self.conv = getattr(self, conv)
        self.choices = choices

    def _get_from_dict(self, name, values):
        if name not in values:
            if self.lax:
                return None
            else:
                raise ValueError("The key \"%s\" is not available in the DBF "\
                                 "file" % name)
        return values[name]

    def convert(self, values):
        base_value = None
        if type(self.geofla_name) in (list, tuple):
            base_value = []
            for name in self.geofla_name:
                base_value.append(self._get_from_dict(name, values))
        else:
            base_value = self._get_from_dict(self.geofla_name, values)
        return self.conv(base_value)

    def to_unicode(self, value):
        if not value:
            return ""
        return unicode(value)

    def to_point(self, value):
        assert(len(value) == 2)
        pt = Point(value[0], value[1], srid=settings.GEOFLA_EPSG)
        return pt

    def to_instance(self, value):
        assert(len(self.geofla_name) == len(value))
        dct = {}
        for key, val in zip(self.geofla_name, value):
            dct[key] = val
        return self.instance_class.create_or_update_from_GEOFLA_dict(dct)

    def get_instance(self, value):
        dct = {}
        geo_fla_dct = dict([(field.geofla_name, field)
                        for field in self.instance_class.GEOFLAFIELDS])
        last_keys, last_vals = [], [] # regroup keys in a tuple when not
                                      # available
        for key, val in zip(self.geofla_name, value):
            last_keys += [key]
            last_vals += [val]
            if len(last_keys) > 1:
                key = tuple(last_keys)
            if key not in geo_fla_dct:
                continue
            if type(key) == tuple:
                val = dict(zip(key, last_vals))
            else:
                val = {key:val}
            # convert the data getting appropriate value for the filter
            val = geo_fla_dct[key].convert(val)
            dct[geo_fla_dct[key].attr_name] = val
            last_keys, last_vals = [], []
        return self.instance_class.objects.get(**dct)

    def to_choice(self, value):
        for k, lbl in self.choices:
            if lbl == value:
                return k
        print "*%s*" % value
        raise ValueError(u"%s is not referenced" % value)

GFFM = GEOFLAFieldManager

class Region(models.Model, GEOFLAManager):
    GEOFLAFIELDS = [
            GFFM('CODE_REG', 'id_geofla', int),
            GFFM('CODE_REG', 'code_reg', 'to_unicode'),
            GFFM('NOM_REGION', 'nom_region', 'to_unicode'),
            ]
    id_geofla = models.IntegerField(primary_key=True)
    code_reg = models.CharField(verbose_name=u"Code région", null=True,
                                 blank=True, max_length=2)
    nom_region = models.CharField(verbose_name=u"Nom", null=True, blank=True,
                                max_length=30)

    class Meta:
        ordering = ('nom_region',)

    def __unicode__(self):
        return u"%s (%s)" % (self.nom_region, self.code_reg)

class Departement(models.Model, GEOFLAManager):
    GEOFLA_DBF_FIELDS = ['ID_GEOFLA','CODE_DEPT','NOM_DEPT','CODE_CHF',
         'NOM_CHF','X_CHF_LIEU','Y_CHF_LIEU','X_CENTROID','Y_CENTROID',
         'CODE_REG','NOM_REGION']
    GEOFLAFIELDS = [
            GFFM('ID_GEOFLA', 'id_geofla', int),
            GFFM('CODE_DEPT', 'code_dept', 'to_unicode'),
            GFFM('NOM_DEPT', 'nom_dept', 'to_unicode'),
            GFFM('CODE_CHF', 'code_chf', 'to_unicode'),
            GFFM('NOM_CHF', 'nom_chf', 'to_unicode'),
            GFFM(('X_CHF_LIEU', 'Y_CHF_LIEU'), 'chf_lieu', 'to_point'),
            GFFM(('X_CENTROID', 'Y_CENTROID'), 'centroid', 'to_point'),
            GFFM(('CODE_REG', 'NOM_REGION'), 'region', 'to_instance',
                                            instance_class=Region)]
    id_geofla = models.IntegerField(primary_key=True)
    code_dept = models.CharField(verbose_name=u"Code département", max_length=2)
    nom_dept = models.CharField(verbose_name=u"Nom", null=True, blank=True,
                                max_length=30)
    code_chf = models.CharField(verbose_name=u"Code du chef lieu", null=True,
                                blank=True, max_length=3)
    nom_chf = models.CharField(verbose_name=u"Nom de la préfecture", null=True,
                               blank=True, max_length=50)
    chf_lieu = models.PointField(verbose_name=u"Chef lieu", null=True,
                                 blank=True, srid=settings.EPSG)
    centroid = models.PointField(verbose_name=u"Centroïde", null=True,
                                 blank=True, srid=settings.EPSG)
    limite = models.MultiPolygonField(verbose_name=u"Limite", null=True,
                                 blank=True, srid=settings.EPSG)
    region = models.ForeignKey("Region", null=True, blank=True)
    objects = models.GeoManager()

    class Meta:
        ordering = ('nom_dept',)

    def __unicode__(self):
        return u"%s (%s)" % (self.nom_dept, self.code_dept)

class Arrondissement(models.Model, GEOFLAManager):
    GEOFLA_DBF_FIELDS = ['ID_GEOFLA','CODE_ARR','CODE_CHF','NOM_CHF',
         'X_CHF_LIEU','Y_CHF_LIEU','X_CENTROID','Y_CENTROID','CODE_DEPT',
         'NOM_DEPT','CODE_REG','NOM_REGION']
    GEOFLAFIELDS = [
            GFFM('ID_GEOFLA', 'id_geofla', int),
            GFFM('CODE_ARR', 'code_arr', 'to_unicode'),
            GFFM('CODE_CHF', 'code_chf', 'to_unicode'),
            GFFM('NOM_CHF', 'nom_chf', 'to_unicode'),
            GFFM(('X_CHF_LIEU', 'Y_CHF_LIEU'), 'chf_lieu', 'to_point'),
            GFFM(('X_CENTROID', 'Y_CENTROID'), 'centroid', 'to_point'),
            GFFM(('CODE_DEPT', 'NOM_DEPT'), 'departement', 'get_instance',
                                            instance_class=Departement)]
    id_geofla = models.IntegerField(primary_key=True)
    departement = models.ForeignKey("Departement", null=True, blank=True)
    code_arr = models.CharField(verbose_name=u"Code arrondissement",
                                max_length=1)
    code_chf = models.CharField(verbose_name=u"Code du chef lieu", null=True,
                                blank=True, max_length=3)
    nom_chf = models.CharField(verbose_name=u"Nom de la préfecture", null=True,
                               blank=True, max_length=50)
    chf_lieu = models.PointField(verbose_name=u"Chef lieu", null=True,
                                 blank=True, srid=settings.EPSG)
    centroid = models.PointField(verbose_name=u"Centroïde", null=True,
                                 blank=True, srid=settings.EPSG)
    limite = models.MultiPolygonField(verbose_name=u"Limite", null=True,
                                 blank=True, srid=settings.EPSG)
    objects = models.GeoManager()

    class Meta:
        ordering = ('departement', 'code_arr')

    def __unicode__(self):
        return u"Arrondissement %s - %s" % (unicode(self.code_arr),
                                            unicode(self.departement))

class Canton(models.Model, GEOFLAManager):
    GEOFLA_DBF_FIELDS = ['ID_GEOFLA','CODE_CANT','CODE_CHF','NOM_CHF',
         'X_CHF_LIEU','Y_CHF_LIEU','X_CENTROID','Y_CENTROID','CODE_ARR',
         'CODE_DEPT','NOM_DEPT','CODE_REG','NOM_REGION']
    GEOFLAFIELDS = [
            GFFM('ID_GEOFLA', 'id_geofla', int),
            GFFM('CODE_CANT', 'code_cant', 'to_unicode'),
            GFFM('CODE_CHF', 'code_chf', 'to_unicode'),
            GFFM('NOM_CHF', 'nom_chf', 'to_unicode'),
            GFFM(('X_CHF_LIEU', 'Y_CHF_LIEU'), 'chf_lieu', 'to_point'),
            GFFM(('X_CENTROID', 'Y_CENTROID'), 'centroid', 'to_point'),
            GFFM(('CODE_ARR', 'CODE_DEPT', 'NOM_DEPT'), 'arrondissement',
                            'get_instance', instance_class=Arrondissement)]

    id_geofla = models.IntegerField(primary_key=True)
    code_cant = models.CharField(verbose_name=u"Code canton", max_length=2)
    code_chf = models.CharField(verbose_name=u"Code du chef lieu", null=True,
                                blank=True, max_length=3)
    nom_chf = models.CharField(verbose_name=u"Nom de la préfecture", null=True,
                               blank=True, max_length=50)
    chf_lieu = models.PointField(verbose_name=u"Chef lieu", null=True,
                                 blank=True, srid=settings.EPSG)
    centroid = models.PointField(verbose_name=u"Centroïde", null=True,
                                 blank=True, srid=settings.EPSG)
    limite = models.MultiPolygonField(verbose_name=u"Limite", null=True,
                                 blank=True, srid=settings.EPSG)
    arrondissement = models.ForeignKey("Arrondissement", null=True, blank=True)
    objects = models.GeoManager()

    class Meta:
        ordering = ('arrondissement', 'code_cant')

    def __unicode__(self):
        return u"Canton %s - %s" % (self.code_cant,
                                    unicode(self.arrondissement))

STATUT_COMMUNE = (
  ('CE', u"Capitale d'état"),
  ('PF', u"Préfecture"),
  ('PR', u"Préfecture de région"),
  ('PD', u"Préfecture de département"),
  ('SP', u"Sous-préfecture"),
  ('CC', u"Chef-lieu canton"),
  ('CS', u"Commune simple"),
)

class Commune(models.Model, GEOFLAManager):
    GEOFLA_DBF_FIELDS = ['ID_GEOFLA','CODE_COMM','INSEE_COM','NOM_COMM',
         'STATUT','X_CHF_LIEU','Y_CHF_LIEU','X_CENTROID','Y_CENTROID',
         'Z_MOYEN','SUPERFICIE','POPULATION','CODE_CANT','CODE_ARR',
         'CODE_DEPT','NOM_DEPT','CODE_REG','NOM_REGION']
    GEOFLAFIELDS = [
            GFFM('ID_GEOFLA', 'id_geofla', int),
            GFFM('CODE_COMM', 'code_comm', 'to_unicode'),
            GFFM('INSEE_COM', 'insee_com', 'to_unicode'),
            GFFM('NOM_COMM', 'nom_comm', 'to_unicode'),
            GFFM('STATUT', 'statut', 'to_choice', choices=STATUT_COMMUNE),
            GFFM(('X_CHF_LIEU', 'Y_CHF_LIEU'), 'chf_lieu', 'to_point'),
            GFFM(('X_CENTROID', 'Y_CENTROID'), 'centroid', 'to_point'),
            GFFM('Z_MOYEN', 'z_moyen', int),
            GFFM('SUPERFICIE', 'superficie', int),
            GFFM('POPULATION', 'population', float),
            GFFM(('CODE_CANT', 'CODE_ARR', 'CODE_DEPT', 'NOM_DEPT'), 'canton',
                                    'get_instance', instance_class=Canton),]
    id_geofla = models.IntegerField(primary_key=True)
    code_comm = models.CharField(verbose_name=u"Code commune", null=True,
                                 blank=True, max_length=3)
    insee_com = models.CharField(verbose_name=u"Code INSEE", null=True,
                                 blank=True, max_length=5)
    nom_comm = models.CharField(verbose_name=u"Nom", null=True, blank=True,
                                max_length=50)
    statut = models.CharField(verbose_name=u"Statut", null=True, blank=True,
                              max_length=2, choices=STATUT_COMMUNE)
    chf_lieu = models.PointField(verbose_name=u"Chef lieu", null=True,
                                 blank=True, srid=settings.EPSG)
    centroid = models.PointField(verbose_name=u"Centroïde", null=True,
                                 blank=True, srid=settings.EPSG)
    z_moyen = models.IntegerField(verbose_name=u"Altitude moyenne (m)",
                                  null=True, blank=True)
    superficie = models.IntegerField(verbose_name=u"Superficie (ha)", null=True,
                                     blank=True)
    population = models.FloatField(verbose_name=u"Population (en milliers)",
                                   null=True, blank=True)
    limite = models.MultiPolygonField(verbose_name=u"Limite", null=True,
                                 blank=True, srid=settings.EPSG)
    canton = models.ForeignKey("Canton", null=True, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.nom_comm
