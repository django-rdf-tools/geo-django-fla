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
from django.core.exceptions import ObjectDoesNotExist

from geodjangofla import settings
from geodjangofla import models
from geodjangofla.utils import dbf

class Command(BaseCommand):
    args = '<geofla_path>'
    help = 'Import des donnees geofla en base de donnees'
    option_list = BaseCommand.option_list + (
        make_option('-d', '--departements',
            action='store',
            type='string',
            dest='departements',
            default=None,
            help='Liste de départements à importer séparée par une virgule. Si'\
                 'cette liste n\'est pas précisée, on importe tous les '\
                 'départements.'),
        )

    def handle(self, *args, **options):
        if not args:
            raise CommandError("No GEOFLA directory provided")
        departements = []
        if options['departements']:
            departements = options['departements'].split(',')
        path = os.path.realpath(args[0])
        data_present = False
        for file_name, cls_name in settings.GEOFLA_FILES:
            for ext in ['.SHP', '.DBF']:
                if os.path.isfile(os.sep.join([path, file_name + ext])):
                    data_present = True
        if not data_present:
            raise CommandError("The given GEOFLA directory structure is not "\
                               "correct")
        # import dbf datas
        for file_name, cls_name in settings.GEOFLA_FILES:
            try:
                f = open(os.sep.join([path, file_name+'.DBF']))
            except IOError:
                continue
            model = getattr(models, cls_name)
            self.stdout.write('* %ss :\n' % (cls_name))
            imported = 0
            for idx, values in enumerate(dbf.reader(f)):
                if idx == 0:
                    if values != model.GEOFLA_DBF_FIELDS:
                        msg = 'Cannot import. The DBF format has changed for '
                        msg += '%s.\n\n' % cls_name
                        msg += '* known :\t%s\n' % str(model.GEOFLA_DBF_FIELDS)
                        msg += '* current :\t%s\n' % str(values)
                        raise CommandError(msg)
                    continue
                if idx == 1:
                    # pass the definition line
                    continue
                converted_values = []
                for val in values:
                    if type(val) == str:
                        val = unicode(val, settings.DBF_ENCODING).strip()
                    converted_values.append(val)
                m = model.create_or_update_from_GEOFLA_dict(
                           dict(zip(model.GEOFLA_DBF_FIELDS, converted_values)),
                           departements=options['departements'])
                if m:
                    imported += 1
                    self.stdout.write('\t- Data : %d\r' % imported)
            self.stdout.write('\n')
            imported = 0
            ds = DataSource(os.sep.join([path, file_name+'.SHP']))
            for idx, feat in enumerate(ds[0]):
                try:
                    o = model.objects.get(id_geofla=feat.get('ID_GEOFLA'))
                except ObjectDoesNotExist:
                    continue
                wkt = feat.geom.wkt
                if wkt.startswith('POLYGON '):
                    wkt = 'MULTIPOLYGON (' + wkt[len('POLYGON '):] + ')'
                o.limite = 'SRID=%d;' % settings.GEOFLA_EPSG + wkt
                o.save()
                imported += 1
                self.stdout.write('\t- Shape : %d\r' % imported)
            self.stdout.write('\n\n')
        self.stdout.write('Import done\n')
