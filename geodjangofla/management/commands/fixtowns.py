#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is free software; you can redistribute it and/or modify it
# under the terms of the BSD License (see the file COPYING included with
# the distribution).

import os
from optparse import make_option

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import DataSource
from django.core.management.base import BaseCommand, CommandError

from geodjangofla import settings
from geodjangofla import models
from geodjangofla.utils import dbf

class Command(BaseCommand):
    help = 'Regroupe les arrondissements en une seule commune'

    def handle(self, *args, **options):
        for commune in models.Commune.objects.filter(
                        nom_comm__endswith='-ARRONDISSEMENT').all():
            items = commune.nom_comm.split('--')
            if len(items) < 3:
                items = commune.nom_comm.split('-')
            nb_ardt = items[-2]
            if nb_ardt[0:2] != '1E':
                commune.delete()
                continue
            commune.nom_comm = "-".join(items[0:-2])
            commune.save()
        self.stdout.write('Regroup done\n')
