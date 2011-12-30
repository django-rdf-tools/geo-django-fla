#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal

from django.test import TestCase

from geodjangofla import models

class DepartementTest(TestCase):
    def setUp(self):
        pass

    def test_data_creation_from_list(self):
        items = [[1,'01','AIN','053','BOURG-EN-BRESSE', 8717, 65696, 8814,
                  65582,'82','RHONE-ALPES'],
                 [2,'02','AISNE','408','LAON', 7451, 69406, 7404, 69401,
                  '22','PICARDIE'],
                 [3,'03','ALLIER','190','MOULINS', 7254, 66072, 7144, 65882,
                  '83','AUVERGNE']]
        for item in items:
            dct = dict(zip(models.Departement.GEOFLA_DBF_FIELDS, item))
            models.Departement.create_or_update_from_GEOFLA_dict(dct)
        self.assertEqual(models.Departement.objects.count(), 3)
        self.assertEqual(models.Region.objects.count(), 3)
        self.assertEqual(models.Departement.objects.get(id_geofla=1).nom_dept,
                         'AIN')
        # update
        item = [1,'01','AINE','053','BOURG-EN-BRESSE', 8717, 65696, 8814,
                65582,'83','AUVERGNE']
        dct = dict(zip(models.Departement.GEOFLA_DBF_FIELDS, item))
        models.Departement.create_or_update_from_GEOFLA_dict(dct)
        self.assertEqual(models.Departement.objects.count(), 3)
        self.assertEqual(models.Region.objects.count(), 3)
        self.assertEqual(models.Departement.objects.get(id_geofla=1).nom_dept,
                         'AINE')

class ArrondissementTest(TestCase):
    def setUp(self):
        items = [[1,'01','AIN','053','BOURG-EN-BRESSE', 8717, 65696, 8814,
                  65582,'82','RHONE-ALPES'],
                 [2,'02','AISNE','408','LAON', 7451, 69406, 7404, 69401,
                  '22','PICARDIE'],
                 [3,'03','ALLIER','190','MOULINS', 7254, 66072, 7144, 65882,
                  '83','AUVERGNE']]
        for item in items:
            dct = dict(zip(models.Departement.GEOFLA_DBF_FIELDS, item))
            models.Departement.create_or_update_from_GEOFLA_dict(dct)

    def test_data_creation_from_list(self):
        items = [
         [1,'1','034','BELLEY', 9089, 65212, 8984, 65331,'01','AIN','82',
          'RHONE-ALPES'],
         [2,'1','168','CHATEAU-THIERRY', 7294, 68830, 7304, 68863,'02','AISNE',
          '22','PICARDIE'],
         [3,'1','185','MONTLUCON', 6694, 65823, 6773, 65887,'03','ALLIER','83',
          'AUVERGNE']
        ]

        for item in items:
            dct = dict(zip(models.Arrondissement.GEOFLA_DBF_FIELDS, item))
            models.Arrondissement.create_or_update_from_GEOFLA_dict(dct)

class CantonTest(TestCase):
    def setUp(self):
        item = [1,'01','AIN','053','BOURG-EN-BRESSE', 8717, 65696, 8814,
                  65582,'82','RHONE-ALPES']
        dct = dict(zip(models.Departement.GEOFLA_DBF_FIELDS, item))
        models.Departement.create_or_update_from_GEOFLA_dict(dct)
        item = [1,'1','034','BELLEY', 9089, 65212, 8984, 65331,'01','AIN','82',
          'RHONE-ALPES']
        dct = dict(zip(models.Arrondissement.GEOFLA_DBF_FIELDS, item))
        models.Arrondissement.create_or_update_from_GEOFLA_dict(dct)

    def test_data_creation_from_list(self):
        items = [
         [1,'01','004','AMBERIEU-EN-BUGEY', 8825, 65425, 8820, 65449,'1','01',
          'AIN','82','RHONE-ALPES'],
         [2,'02','003','AIGUILLES', 10059, 64166, 10066, 64138,'1','01',
          'AIN','82', "RHONE-ALPES"],
        ]

        for item in items:
            dct = dict(zip(models.Canton.GEOFLA_DBF_FIELDS, item))
            models.Canton.create_or_update_from_GEOFLA_dict(dct)

class CommuneTest(TestCase):
    def setUp(self):
        item = [1,'01','AIN','053','BOURG-EN-BRESSE', 8717, 65696, 8814,
                  65582,'82','RHONE-ALPES']
        dct = dict(zip(models.Departement.GEOFLA_DBF_FIELDS, item))
        models.Departement.create_or_update_from_GEOFLA_dict(dct)
        item = [1,'1','034','BELLEY', 9089, 65212, 8984, 65331,'01','AIN','82',
          'RHONE-ALPES']
        dct = dict(zip(models.Arrondissement.GEOFLA_DBF_FIELDS, item))
        models.Arrondissement.create_or_update_from_GEOFLA_dict(dct)
        item = [1,'01','004','AMBERIEU-EN-BUGEY', 8825, 65425, 8820, 65449,'1',
                '01','AIN','82','RHONE-ALPES']
        dct = dict(zip(models.Canton.GEOFLA_DBF_FIELDS, item))
        models.Canton.create_or_update_from_GEOFLA_dict(dct)

    def test_data_creation_from_list(self):
        items = [
         [1,'398','71398','SAINT-CHRISTOPHE-EN-BRESSE','Commune simple', 8517,
          66299, 8519, 66291, 193, 2049, Decimal('0.9'),'01','1', '01',
          'AIN','82','RHONE-ALPES'],
         [2,'708','21708','VILLY-LE-MOUTIER','Commune simple', 8512, 66616,
          8508, 66617, 199, 2017, Decimal('0.3'),'01','1','01', "AIN",
          '82','RHONE-ALPES'],
        ]
        for item in items:
            dct = dict(zip(models.Commune.GEOFLA_DBF_FIELDS, item))
            models.Commune.create_or_update_from_GEOFLA_dict(dct)
