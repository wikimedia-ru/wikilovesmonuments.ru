//Base module
var WLM = (function(){
    var version = "1.0";
    
    //Cache for region cities
    var cities = [];
    var cur_region;
    
    var getRegionCities = function(region, callback){
        cur_region = region;
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

    var getCity = function(city_id){
        var city;
        $.each(cities[cur_region], function(key, val){
            if (val.id == city_id){
                city = val;
                return false;
            }
        });
        return city;
    }

    return {
        version: version,
        getRegionCities: getRegionCities,
        getCity: getCity
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
    var cluster;

    //Get markers for selected region
    regionMarkers = function(region) {
        if (typeof markers[region] !== 'undefined') {
            if (cluster){
                map.removeLayer(cluster);
            }
            setPosition(region);
            cluster = markers[region];
            map.addLayer(cluster);
            return;
        } else {
            getMarkers(region);
        }

    }

    cityMarkers = function(city_id){
        if (cluster) {
            map.removeLayer(cluster);    
        }
        cluster = new L.MarkerClusterGroup();
        $.ajax({
            url: '/ajax/markerscity/' + city_id,
            success: function(data){
                for (var key in data){
                    var val = data[key];
                    var marker = new L.Marker(new L.LatLng(val.coord_lat, val.coord_lon), { title: val.name });
                        marker.bindPopup(val.name)
                            .addTo(cluster);
                }
                clearMap();
                city = WLM.getCity(city_id);
                if (city){
                    map.panTo(new L.LatLng(city.latitude, city.longitude))
                }
                map.addLayer(cluster);
            }

        });
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
					if (cluster){
                        map.removeLayer(cluster);
                    }
                    cluster = markers[region];
                    map.addLayer(cluster);
                    setPosition(region);
                }
        });
    }
    return {
        init_map: init_map,
        regionMarkers: regionMarkers,
        cityMarkers: cityMarkers,
        setPosition: setPosition
    };
})(jQuery);


