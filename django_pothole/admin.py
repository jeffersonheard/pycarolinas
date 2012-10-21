from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin

from django_pothole import models

admin.site.register(models.Pothole, admin_class=OSMGeoAdmin)