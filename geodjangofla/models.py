#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.gis.db import models

class Region(models.Model):
    code_reg = models.CharField(verbose_name=u"Code région", null=True,
                                 blank=True, max_length=2)
    nom_region = models.CharField(verbose_name=u"Nom", null=True, blank=True,
                                max_length=30)

class Departement(models.Model):
    code_dept = models.CharField(verbose_name=u"Code département", max_length=2)
    nom_dept = models.CharField(verbose_name=u"Nom", null=True, blank=True,
                                max_length=30)
    code_chf = models.CharField(verbose_name=u"Code du chef lieu", null=True,
                                blank=True, max_length=3)
    nom_chf = models.CharField(verbose_name=u"Nom de la préfecture", null=True,
                               blank=True, max_length=30)
    chf_lieu = models.PointField(verbose_name=u"Chef lieu", null=True,
                                 blank=True, srid=settings.EPSG_PROJECTION)
    centroid = models.PointField(verbose_name=u"Centroïde", null=True,
                                 blank=True, srid=settings.EPSG_PROJECTION)
    limite = models.MultiPolygonField(verbose_name=_(u"Limite"),
                                      srid=settings.EPSG_PROJECTION)
    objects = models.GeoManager()

class Arrondissement(models.Model):
    departement = models.ForeignKey("Departement", null=True, blank=True)
    code_arr = models.CharField(verbose_name=u"Code arrondissement",
                                max_length=1)
    code_chf = models.CharField(verbose_name=u"Code du chef lieu", null=True,
                                blank=True, max_length=3)
    nom_chf = models.CharField(verbose_name=u"Nom de la préfecture", null=True,
                               blank=True, max_length=30)
    chf_lieu = models.PointField(verbose_name=u"Chef lieu", null=True,
                                 blank=True, srid=settings.EPSG_PROJECTION)
    centroid = models.PointField(verbose_name=u"Centroïde", null=True,
                                 blank=True, srid=settings.EPSG_PROJECTION)
    limite = models.MultiPolygonField(verbose_name=_(u"Limite"),
                                      srid=settings.EPSG_PROJECTION)
    objects = models.GeoManager()

class Canton(models.Model):
    departement = models.ForeignKey("Departement", null=True, blank=True)
    code_cant = models.CharField(verbose_name=u"Code arrondissement",
                                max_length=2)
    code_chf = models.CharField(verbose_name=u"Code du chef lieu", null=True,
                                blank=True, max_length=3)
    nom_chf = models.CharField(verbose_name=u"Nom de la préfecture", null=True,
                               blank=True, max_length=30)
    chf_lieu = models.PointField(verbose_name=u"Chef lieu", null=True,
                                 blank=True, srid=settings.EPSG_PROJECTION)
    centroid = models.PointField(verbose_name=u"Centroïde", null=True,
                                 blank=True, srid=settings.EPSG_PROJECTION)
    limite = models.MultiPolygonField(verbose_name=_(u"Limite"),
                                      srid=settings.EPSG_PROJECTION)
    arrondissement = models.ForeignKey("Arrondissement", null=True, blank=True)
    objects = models.GeoManager()

STATUT_COMMUNE = (
  ('CE', u"Capitale d'État"),
  ('PR', u"Préfecture de région"),
  ('PD', u"Préfecture de département"),
  ('SP', u"Sous préfecture"),
  ('CC', u"Chef-lieu de canton"),
  ('CS', u"Commune simple"),
)

class Commune(models.Model):
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
                                 blank=True, srid=settings.EPSG_PROJECTION)
    centroid = models.PointField(verbose_name=u"Centroïde", null=True,
                                 blank=True, srid=settings.EPSG_PROJECTION)
    z_moyen = models.IntegerField(verbose_name=u"Altitude moyenne (m)",
                                  null=True, blank=True)
    superficie = models.IntegerField(verbose_name=u"Superficie (ha)", null=True,
                                     blank=True)
    population = models.IntegerField(verbose_name=u"Population", null=True,
                                     blank=True)
    code_cant = models.CharField(verbose_name=u"Code canton", null=True,
                                 blank=True, max_length=2)
    code_arr = models.CharField(verbose_name=u"Code arrondissement", null=True,
                                blank=True, max_length=1)
    canton = models.ForeignKey("Canton", null=True, blank=True)
    arrondissement = models.ForeignKey("Arrondissement", null=True, blank=True)
    departement = models.ForeignKey("Departement", null=True, blank=True)
    objects = models.GeoManager()


