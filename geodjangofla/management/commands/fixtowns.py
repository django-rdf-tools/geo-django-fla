#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is free software; you can redistribute it and/or modify it
# under the terms of the BSD License (see the file COPYING included with
# the distribution).

import os
from optparse import make_option
from django.contrib.gis.geos import MultiPolygon

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import DataSource
from django.core.management.base import BaseCommand, CommandError

from geodjangofla import settings
from geodjangofla import models
from geodjangofla.utils import dbf

class Command(BaseCommand):
    help = 'Regroupe les arrondissements en une seule commune'

    def handle(self, *args, **options):
        limits = {}
        for commune in models.Commune.objects.filter(
                        nom_comm__endswith='-ARRONDISSEMENT').all():
            items = commune.nom_comm.split('--')
            if len(items) < 3:
                items = commune.nom_comm.split('-')
            nb_ardt = items[-2]
            nom_comm = "-".join(items[0:-2])
            if nom_comm.endswith('-'):
                nom_comm = nom_comm[:-1]
            key = (nom_comm, commune.insee_com[0:2])
            if key not in limits:
                limits[key] = commune.limite
            else:
                limits[key] = limits[key].union(commune.limite)
            if nb_ardt[0:2] != '1E':
                commune.delete()
                continue
            commune.nom_comm = nom_comm
            commune.save()
        for nom_comm, dpt in limits:
            com = models.Commune.objects.get(nom_comm__startswith=nom_comm,
                                                 insee_com__startswith=dpt)
            new_limit = limits[(nom_comm, dpt)]
            if new_limit.geom_type == 'Polygon':
                new_limit = MultiPolygon([new_limit])
            com.limite = new_limit
            com.save()
        self.stdout.write('Regroup done\n')
