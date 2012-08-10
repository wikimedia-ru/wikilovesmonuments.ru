//Base module
var WLM = (function(){
    var version = "1.0";
    
    //Cache for region cities
    var cities = []
    
    var getRegionCities = function(region, callback){
        if (typeof cities[region] !== 'undefined'){
            if (callback) {
                callback(cities[region]);
            } else{
                return cities[region];    
            }
        } else {
            $.ajax({url: '/ajax/citiesregion/' + region,
                success: function(data){
                    cities[region] = data;
                    if (callback) {callback(cities[region]);}
                }
            });
        }
    }

    return {
        version: version,
        getRegionCities: getRegionCities
    }
})(jQuery);

WLM.map = (function($){
    
    var minZoom = 3;
    var maxZoom = 18;
    var center = new L.LatLng(66, 94)
    //Cloudmade layer
    var cloudmade = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
									maxZoom: 18,
									minZoom: 3,
									attribution: 'карта &copy; OpenStreetMap, рендер &copy; CloudMade'
								});
    //Map object
    var map;

    //Initialise map code.
    init_map = function(item_name){
        map = new L.Map(item_name, {
            center: new L.LatLng(66, 94),
            zoom: 3,
            zoomControl: false,
            layers: [cloudmade]
        });
        map.zoomControl = new L.Control.Zoom({ position: 'bottomleft' });
    }

    //Pan and zoom map
    setPosition = function(region){
        var data = regions[region];
        map.panTo(new L.LatLng(data['latitude'], data['longitude']))
        map.setZoom(data['scale']);
    }

    //Clear map layers
    var clearMap = function(){
        for (key in markers){
            map.removeLayer(markers[key]);
        }
    }

    //Markers cache
    var markers = [];

    //Get markers for selected region
    regionMarkers = function(region) {
        if (typeof markers[region] !== 'undefined') {
            clearMap();
            setPosition(region);
            map.addLayer(markers[region]);
            return;
        } else {
            getMarkers(region);
        }

    }


    //Get markers from site and put it in cache
    var getMarkers = function(region){
        markers[region] = new L.MarkerClusterGroup();
        $.ajax({url: '/ajax/markersregion/' + region,
                success: function(data){
                    for (var key in data) {
                        var val = data[key];
                        var marker = new L.Marker(new L.LatLng(val.coord_lat, val.coord_lon), { title: val.name });
                        marker.bindPopup(val.name)
                            .addTo(markers[region]);
                    }
					clearMap();
                    map.addLayer(markers[region]);
                    setPosition(region);
                }
        });
    }
    return {
        init_map: init_map,
        regionMarkers: regionMarkers,
        setPosition: setPosition
    };
})(jQuery);


