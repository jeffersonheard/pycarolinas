from django.conf.urls.defaults import patterns, url
from ga_ows.views.wfs import WFS
from ga_ows.views.wms import WMS, GeoDjangoWMSAdapter
from ga_ows.models import test_models as m

