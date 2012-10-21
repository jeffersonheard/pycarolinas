# Create your views here.
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponseRedirect

from django_pothole.models import Zcta, Population, Pothole
from django.views.generic import TemplateView
from ga_ows.views.wms import WMS, GeoDjangoWMSAdapter
from ga_ows.rendering import styler

lo = (237/255.0, 248/255.0, 177/255.0, 1.0)
med = (127/255.0, 205/255.0, 187/255.0, 1.0)
hi = (44/255.0, 127/255.0, 184/255.0, 1.0)
black = (0,0,0,1.0)

lo1 =(247/255.0, 247/255.0, 247/255.0, 0.7)
lo2 =(204/255.0, 204/255.0, 204/255.0, 0.7)
med1 =(150/255.0, 150/255.0, 150/255.0, 0.7)
hi1 =(99/255.0, 99/255.0, 99/255.0, 0.7)
hi2 = (37/255.0, 37/255.0, 37/255.0, 0.7)


pmax = max(p.pop for p in Population.objects.all())
def bin(data,n=5):
    bins = [k*pmax/n for k in range(1, n+1)]
    for i, binval in enumerate(bins):
        if data <= binval:
            return i

pothole_styles = {
    'default' : styler.Stylesheet(name='default',
        point_shape = 'circle',
        point_size = lambda data, pxsz: (5, 10, 18)[ data['width'] ],
        stroke_width = lambda data, pxsz: (0.5, 1.5, 3.5)[ data['depth'] ],
        stroke_color = black,
        fill_color = lambda data, pxsz: (lo, med, hi)[ data['width'] ]
    )
}

zipcode_styles = {
    'default' : styler.Stylesheet(name='default',
        stroke_width = 0.5,
        stroke_color = black,
        fill_color = lambda data, pxsz: (lo1, lo2, med1, hi1, hi2)[ bin(Population.objects.get(zcta5ce10_id=data['gid']).pop) ]
    )
}

class PotholeLayer(WMS):
    adapter = GeoDjangoWMSAdapter(cls=Pothole, styles=pothole_styles)
    title = "Potholes"

class ZipcodeLayer(WMS):
    adapter = GeoDjangoWMSAdapter(cls=Zcta, styles=zipcode_styles)
    title = "Zipcodes"

class PotholeReportingView(TemplateView):
    template_name = "django_pothole/pothole_reporting.html"

    def post(self, request, *args, **kwargs):
        width = int(request.POST['width'])
        depth = int(request.POST['depth'])
        longitude = float(request.POST['longitude'])
        latitude = float(request.POST['latitude'])

        p = Point(latitude, longitude, srid=4326)
        p3857 = p.transform(3857, clone=True)

        similar = Pothole.objects.transform(srid=3857).filter(location__distance_lt=(p3857, D(m=5)))
        if len(similar):
            similar[0].number_of_logs += 1
            similar[0].save()
        else:
            p = Pothole(width=width, depth=depth, location=Point(latitude, longitude, srid=4326))
            p.save()

        return HttpResponseRedirect('/potholes/report/')

class PotholeTriageView(TemplateView):
    template_name = "django_pothole/pothole_triage.html"

