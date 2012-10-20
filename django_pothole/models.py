from django.contrib.gis.db.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
import geopy

# Create your models here.

class Pothole(Model):
    location = PointField()
    location_name = TextField(blank=True, editable=False)
    width = IntegerField()
    depth = IntegerField()
    when_logged = DateTimeField(auto_now_add=True)

    # override the default manager with one that can accept geographic queries
    objects = GeoManager()

@receiver(pre_save, sender=Pothole)
def pothole_pre_save(sender, instance, *args, **kwargs):
    try:
        g = geopy.geocoders.Google()
        instance.location_name = g.reverse((instance.location.x, instance.location.y))[0]
    except:
        instance.location_name = "No nearby address."

