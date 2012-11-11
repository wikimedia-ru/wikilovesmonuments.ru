//Base module
var WLM = (function() {
	var version = "1.1";

	//Cache for region cities
	var cities = [];
	var cur_region;

	//Regions cache
	var regionMarkers = [];

	var getRegionMarkers = function(region, callback) {
		if (typeof regionMarkers[region] !== 'undefined') {
			callback(regionMarkers[region]);
		}
		else {
			fetchRegionMarkers(region, callback);
		}
	}

	//Get markers from site and put it in cache
	var fetchRegionMarkers = function(region, callback) {
		$.ajax({
			url: '/ajax/markersregion/' + region,
			success: function(data) {
				regionMarkers[region] = data;
				callback(regionMarkers[region]);
			}
		});
	}

	//Fetch cities info from site and cache it.
	var getRegionCities = function(region, callback) {
		cur_region = region;
		if (typeof cities[region] !== 'undefined') {
			if (callback) {
				callback(cities[region]);
			}
			else {
				return cities[region];
			}
		} else {
			$.ajax({
				url: '/ajax/citiesregion/' + region,
				success: function(data) {
					cities[region] = data;
					if (callback) {
						callback(cities[region]);
					}
				}
			});
		}
	}

	var getCity = function(city_id) {
		var city;
		$.each(cities[cur_region], function(key, val) {
			if (val.id == city_id) {
				city = val;
				return false;
			}
		});
		return city;
	}

	return {
		version: version,
		getRegionMarkers: getRegionMarkers,
		getRegionCities: getRegionCities,
		getCity: getCity
	}
})(jQuery);


WLM.map = (function($) {
	var minZoom = 3;
	var maxZoom = 18;
	var center = new L.LatLng(66, 94);

	//Cloudmade layer
	var cloudmade = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 18,
		minZoom: 3,
		attribution: 'карта &copy; OpenStreetMap, рендер &copy; CloudMade'
	});

	//Map object
	var map;

	//Initialise map code.
	init_map = function(item_name, config) {
		var config = config || [];
		if (config['coord_lat'] && config['coord_lon']) {
			center = new L.LatLng(config['coord_lat'], config['coord_lon']);
		}
		map = new L.Map(item_name, {
			center:      center,
			zoom:        config['zoom'] || 3,
			zoomControl: config['zoomControl'] || false,
			layers:      [cloudmade]
		});
		map.zoomControl = new L.Control.Zoom({ position: 'topright' });
		map.addControl(map.zoomControl);
	}

	//Pan and zoom map to region
	var setRegionPosition = function(region) {
		var data = regions[region]; //Global bootstraped regions data
		map.panTo(new L.LatLng(data['latitude'], data['longitude']))
		map.setZoom(data['scale']);
	}

	//Pan map to coordinates
	var setPosition = function(lat, lon) {
		map.panTo(new L.LatLng(lat, lon));
	}

	//Zoom map to lvl
	var setZoom = function(lvl) {
		map.setZoom(lvl);
	}

	//Clear map layers
	var clearMap = function() {
		for (key in markers) {
			map.removeLayer(markers[key]);
		}
	}

	//Markers cache
	//var markers = [];

	//Markers Layer
	var markersLayer;

	//Get markers for selected region
	regionMarkers = function(region) {
		setRegionPosition(region);
		WLM.getRegionMarkers(region, buildMarkersLayer);
	}

	//Build pop-up.
	//XXX Rewrite to mustache engine
	var buildPopup = function(item) {
		var name = item.name ? item.name : "[Без названия]";
		return "<a class='name' href='/monument/" + item.id + "'>" + name + "</a>";
	}

	//Put alone marker to map.
	var addMarker = function(item) {
		var marker = new L.Marker(
			new L.LatLng(item.coord_lat, item.coord_lon),
			{title: item.name, draggable: (item.draggable ? item.draggable: false )}
		);
		marker.addTo(map);
		return marker;
	}

	//Internal callback for building markers layer.
	var buildMarkersLayer = function(data) {
		if (markersLayer) {
			map.removeLayer(markersLayer);
		}
		markersLayer = new L.MarkerClusterGroup();
		for (var key in data) {
			var val = data[key];
			var marker = new L.Marker(
				new L.LatLng(val.coord_lat, val.coord_lon),
				{ title: val.name }
			);
			marker.bindPopup(buildPopup(val)).addTo(markersLayer);
		}
		map.addLayer(markersLayer);
	}


	var cityMarkers = function(city_id) {
		city = WLM.getCity(city_id);
		if (city) {
			map.panTo(new L.LatLng(city.latitude, city.longitude));
			map.setZoom(12);
		}

		$.ajax({
			url: '/ajax/markerscity/' + city_id,
			success: buildMarkersLayer
		});
	}

	return {
		init_map: init_map,
		addMarker: addMarker,
		regionMarkers: regionMarkers,
		cityMarkers: cityMarkers,
		setPosition: setPosition,
		setZoom:setZoom
	};
})(jQuery);

