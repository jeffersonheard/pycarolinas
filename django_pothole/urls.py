from django.conf.urls import patterns, url
from django_pothole import views

urlpatterns = patterns('',
    url(r'^report/', views.PotholeReportingView.as_view()),
    url(r'^zipcodes/wms/', views.ZipcodeLayer.as_view()),
    url(r'^potholes/wms/', views.PotholeLayer.as_view()),
    url(r'^triage/', views.PotholeTriageView.as_view())
)