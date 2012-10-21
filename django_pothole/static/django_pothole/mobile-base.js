// API key for http://openlayers.org. Please get your own at
// http://bingmapsportal.com/ and use that instead.
var apiKey = "AqTGBsziZHIJYYxgivLBf0hVdrAk9mWO5cQcb8Yux8sW5M8c8opEC2lZqKR1ZZXf";

// initialize map when page ready
var map;
var gg = new OpenLayers.Projection("EPSG:4326");
var sm = new OpenLayers.Projection("EPSG:900913");

var init = function (onSelectFeatureFunction) {

    // create map
    map = new OpenLayers.Map({
        div: "map",
        theme: null,
        projection: sm,
        numZoomLevels: 18,
        controls: [
            new OpenLayers.Control.Attribution(),
            new OpenLayers.Control.TouchNavigation({
                dragPanOptions: {
                    enableKinetic: true
                }
            })

        ],
        layers: [
            new OpenLayers.Layer.OSM("OpenStreetMap", null, {
                transitionEffect: 'resize'
            }),
            new OpenLayers.Layer.WMS("Zipcodes", "http://localhost:8000/potholes/zipcodes/wms/", {
                layers: 'geom',
                styles: 'default',
                projection: 'EPSG:3857',
                transparent: 'true',
                fresh: 'true'
            },
                {
                    layers: 'location',
                    styles: 'default',
                    projection: 'EPSG:3857',
                    transparent: 'true',
                    fresh : 'true'
                }),
            new OpenLayers.Layer.WMS("Potholes", "http://localhost:8000/potholes/potholes/wms/", {
                layers: 'location',
                styles: 'default',
                projection: 'EPSG:3857',
                transparent: 'true',
                fresh : 'true'
            },
                {
                    layers: 'location',
                    styles: 'default',
                    projection: 'EPSG:3857',
                    transparent: 'true',
                    fresh : 'true'
                })
        ],
        center: new OpenLayers.LonLat(-78, 35),
        zoom: 1
    });



};