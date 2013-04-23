#!/usr/bin/env python
# -*- coding: utf-8 -*-

EPSG = 4326
GEOFLA_EPSGS = {'metropole': 2154, # RGF93 / Lambert-93 : metropole
                'reunion': 2975, # RGR92 / UTM 40S : Reunion
                'guyanne': 2972, # RGFG95 / UTM 22N : Guyane
                'mayotte': 4471, # RGM04 / UTM 38S : Mayotte
                'guadeloupe-martinique': 32620, # WGS84 / UTM 20N : Guadeloupe / Martinique
                'st-pierre_et-miquelon': 4467 # RGSPM06 / UTM 21N : St-Pierre-et-Miquelon
                }

GEOFLA_EPSG = GEOFLA_EPSGS['metropole']

GEOFLA_FILES = (('DEPARTEMENTS/DEPARTEMENT', 'Departement'),
                ('ARRONDISSEMENTS/ARRONDISSEMENT', 'Arrondissement'),
                ('CANTONS/CANTON', 'Canton'),
                ('COMMUNES/COMMUNE', 'Commune'))
DBF_ENCODING = 'iso-8859-15'

