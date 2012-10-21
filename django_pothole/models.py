from django.contrib.gis.db.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
import geopy
import csv

# Create your models here.

class Pothole(Model):
    location = PointField()
    location_name = TextField(blank=True, editable=False)
    width = IntegerField()
    depth = IntegerField()
    when_logged = DateTimeField(auto_now_add=True)
    number_of_logs = IntegerField(default=1)

    # override the default manager with one that can accept geographic queries
    objects = GeoManager()

    def __unicode__(self):
        return "{location_name}: {width}, {depth} at {when_logged} ({number_of_logs} times)".format(
            location_name = self.location_name,
            width = ['small','med','lg'][self.width],
            depth = ['shallow','med','deep'][self.depth],
            when_logged = self.when_logged.strftime("%y.%m.%d"),
            number_of_logs = self.number_of_logs
        )

# Column   |         Type          |                     Modifiers
# ------------+-----------------------+----------------------------------------------------
# gid        | integer               | not null default nextval('zcta_gid_seq'::regclass)
# statefp10  | character varying(2)  |
# zcta5ce10  | character varying(5)  |
# geoid10    | character varying(7)  |
# classfp10  | character varying(2)  |
# mtfcc10    | character varying(5)  |
# funcstat10 | character varying(1)  |
# aland10    | double precision      |
# awater10   | double precision      |
# intptlat10 | character varying(11) |
# intptlon10 | character varying(12) |
# partflg10  | character varying(1)  |
# geometry   | geometry              |
# Indexes:
# "zcta_pkey" PRIMARY KEY, btree (gid)
# "zcta_geometry_gist" gist (geometry)
# Check constraints:
# "enforce_dims_geometry" CHECK (st_ndims(geometry) = 2)
# "enforce_geotype_geometry" CHECK (geometrytype(geometry) = 'MULTIPOLYGON'::text OR geometry IS NULL)
# "enforce_srid_geometry" CHECK (st_srid(geometry) = 4326)
class Zcta(Model):
    gid = IntegerField(primary_key=True)
    statefp10 = CharField(max_length=2,null=True)
    zcta5ce10 = CharField(max_length=5,null=True)
    geoid10 = CharField(max_length=7,null=True, db_index=True)
    classfp10 = CharField(max_length=2,null=True)
    mtfcc10 = CharField(max_length=5,null=True)
    funcstat10 = CharField(max_length=1,null=True)
    aland10 = FloatField(null=True)
    awater10 = FloatField(null=True)
    intptlat10 = CharField(max_length=11, null=True)
    intptlon10 = CharField(max_length=12, null=True)
    partflg10 = CharField(max_length=1, null=True)

    geom = MultiPolygonField()
    objects=GeoManager()

    class Meta:
        db_table = "zipcodes"
        managed = False

class Population(Model):
    zcta5ce10 = OneToOneField(Zcta)
    pop = IntegerField()

    @classmethod
    def load(klass):
        with open('/Users/jeff/PyCarolinas/pycarolinas/django_pothole/data/aff_download/DEC_10_SF1_P1_with_ann.csv') as stream:
            records = csv.DictReader(stream)
            klass.objects.bulk_create(
                klass(
                    zcta5ce10 = Zcta.objects.get(zcta5ce10=rec['GEO.id2']),
                    pop       = int(rec['D001'])
                )
                for rec in records)

# signals to connect

geocoder = geopy.geocoders.Google()
@receiver(pre_save, sender=Pothole)
def pothole_pre_save(sender, instance, *args, **kwargs):
    global geocoder

    if instance.location_name == '' or not instance.location_name:
        try:
            instance.location_name = geocoder.reverse((instance.location.x, instance.location.y))[0]
        except:
            instance.location_name = "No nearby address."

