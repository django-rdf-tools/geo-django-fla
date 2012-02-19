About
*****

This software is a Django application to simplify management of GEOFLA(R) datas
of the IGN (french geographic institute).
No GEOFLA(R) datas are provided.

You have to get them on the IGN website. Theses datas are distributed under an
open license (Licence Ouverte 1.0).

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file COPYING included with
the distribution).

Requirements
************
  - Django (>=1.2);

  - Django-south (>=0.7.3);

  - Postgresql (>=8) with its geographic extension PostGIS (>=1.4);

  - PROJ.4.


Usage
*****

 - Install the requirements of this application (a requirement file is provided
   for python dependencies) by your prefered mean (pip, sources or packages).

 - Create a new Django project or go to an existing project you want to include
   this application into. Add 'south' and 'geodjangofla' to INSTALLED_APPS in
   your settings.py

 - Get the software, extract it on a dir to make it available on the python path
   or set the python path to include the dir in your django project.

 - Download the GEOFLA(R) Communes archive (available `here
   <http://professionnels.ign.fr/ficheProduitCMS.do?idDoc=6185461>`_ on december
   2011)

 - Extract the archive on a temporary path.

 - Inside your Django application path, run the command
   "./manage.py importgeofla PATH_TO_GEOFLA_DATAS". It should normaly import all
   datas.

 - That's it!

FAQ
***

Why not using a "simple" shp2pg?
--------------------------------

 - upgrade is managed

 - tables are automatically linked between them with foreign key

 - "chef lieu" and "centroid" are converted to points

 - and you get all the benefit of having a ready to serve django application.

Funding
*******

geodjangofla development was funded by `CREDIS <http://credis.org/>`_, FSE
(European Social Fund) and Conseil Regional d'Auvergne.

