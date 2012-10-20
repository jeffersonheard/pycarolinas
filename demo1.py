from django_pothole import models
from django.contrib.gis.geos import Point

# should be 3926 swarthmore rd durham nc 27707
p = models.Pothole(location=Point(35.934849, -78.959757), width=4, depth=2)
p.save()

print p.location_name
