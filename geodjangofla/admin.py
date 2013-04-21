#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is free software; you can redistribute it and/or modify it
# under the terms of the BSD License (see the file COPYING included with
# the distribution).

from django.contrib.gis import admin

import models

class RegionAdmin(admin.ModelAdmin):
    model = models.Region
    list_display = ['nom_region', 'code_reg',]
    ordering = ['nom_region']
admin.site.register(models.Region, RegionAdmin)

class DepartementAdmin(admin.OSMGeoAdmin):
    model = models.Departement
    list_display = ['nom_dept', 'code_dept',]
    ordering = ['nom_dept']
    list_filter = ['region']
admin.site.register(models.Departement, DepartementAdmin)

class ArrondissementAdmin(admin.OSMGeoAdmin):
    model = models.Arrondissement
    list_display = ['code_arr', 'departement',]
    ordering = ['departement', 'code_arr']
    list_filter = ['departement']
admin.site.register(models.Arrondissement, ArrondissementAdmin)

class CantonAdmin(admin.OSMGeoAdmin):
    model = models.Canton
    list_display = ['code_cant', 'arrondissement',]
    ordering = ['arrondissement', 'code_cant']
    list_filter = ['arrondissement__departement']
admin.site.register(models.Canton, CantonAdmin)

class CommuneAdmin(admin.OSMGeoAdmin):
    model = models.Commune
    search_fields = ['nom_comm', 'insee_com']
    list_display = ['nom_comm', 'insee_com', 'statut']
    # , 'canton']
    ordering = ['nom_comm']
    # , 'canton']
    list_filter = ['statut']
    # , 'canton__arrondissement__departement']
admin.site.register(models.Commune, CommuneAdmin)
