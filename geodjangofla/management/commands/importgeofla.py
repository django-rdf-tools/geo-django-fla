#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from geodjangofla import models
from geodjangofla.utils import dbf
from geodjangofla import settings


class Command(BaseCommand):
    args = '<geofla_path>'
    help = 'Import des donnees geofla en base de donnees'

    def handle(self, *args, **options):
        if not args:
            raise CommandError("No GEOFLA directory provided")
        path = os.path.realpath(args[0])
        try:
            assert(os.path.isdir(path))
            for file_name, cls_name in settings.GEOFLA_FILES:
                for ext in ['.SHP', '.DBF']:
                    assert(os.path.isfile(os.sep.join([path, file_name + ext])))
        except AssertionError:
            raise CommandError("The given GEOFLA directory structure is not "\
                               "correct")
        # import dbf datas
        for file_name, cls_name in settings.GEOFLA_FILES[1:]:
            f = open(os.sep.join([path, file_name+'.DBF']))
            for idx, values in enumerate(dbf.reader(f)):
                print values
                if idx > 3:
                    raise
        """
            self.stdout.write('Successfully closed poll "%s"\n' % poll_id)
        """
