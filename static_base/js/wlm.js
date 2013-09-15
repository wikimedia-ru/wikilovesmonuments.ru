//Base module
var WLM = (function() {
	var version = "1.2";

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
		}
		else {
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
	var minZoom = 4,
		maxZoom = 17,
		center = new L.LatLng(66, 94);

	//Default layer
	var mapsurfer = L.tileLayer('http://129.206.74.245:8001/tms_r.ashx?x={x}&y={y}&z={z}', {
		maxZoom: maxZoom,
		minZoom: minZoom,
		attribution: 'данные карты &copy; участники <a href="http://osm.org">OpenStreetMap</a>, рендер &copy; <a href=\"http://giscience.uni-hd.de/\" target=\"_blank\">GIScience Research Group @ University of Heidelberg</a>'
	});
	var mapbox = L.tileLayer('http://{s}.tiles.mapbox.com/v3/putnik.map-86mogcj7/{z}/{x}/{y}.png', {
		maxZoom: maxZoom,
		minZoom: minZoom,
		attribution: 'данные карты &copy; участники <a href="http://osm.org">OpenStreetMap</a>, рендер &copy; <a href="http://mapbox.com/">MapBox</a>'
	});

	//Map object
	var map;

	//Initialise map code
	var initMap = function (item_name, config) {
		var config = config || [];
		if (config['coord_lat'] && config['coord_lon']) {
			center = new L.LatLng(config['coord_lat'], config['coord_lon']);
		}
		map = new L.Map(item_name, {
			center:        center,
			zoom:          config['zoom'] || minZoom,
			zoomControl:   config['zoomControl'] || false,
			searchControl: config['searchControl'] || false,
			layers:        [mapsurfer]
		});
		map.zoomControl = new L.Control.Zoom({ position: 'topright' });
		map.addControl(map.zoomControl);
	}

	//Pan and zoom map to region
	var setRegionPosition = function(region) {
		var data = regions[region]; //Global bootstraped regions data
		map.setView(
			new L.LatLng(data['latitude'], data['longitude']),
			data['scale']
		);
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
	var regionMarkers = function(region) {
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
		markersLayer = new L.MarkerClusterGroup({
			showCoverageOnHover: false,
			spiderfyOnMaxZoom: true,
			maxClusterRadius: 70
		});
		for (var key in data) {
			var val = data[key];
			var marker = new L.Marker(
				new L.LatLng(val.coord_lat, val.coord_lon),
				{ title: val.name }
			);
			marker
				.bindPopup(buildPopup(val))
				.addTo(markersLayer);
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
		initMap: initMap,
		addMarker: addMarker,
		regionMarkers: regionMarkers,
		cityMarkers: cityMarkers,
		setPosition: setPosition,
		setZoom: setZoom
	};
})(jQuery);

