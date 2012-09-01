/*
 * Search field
 */
L.Control.Search = L.Control.extend({
	options: {
		position: 'topright'
	},

	onAdd: function (map) {
		var className = 'leaflet-control-search',
			container = L.DomUtil.create('div', className),
			form = L.DomUtil.create('form', 'input-append', container);
		L.DomEvent.disableClickPropagation(container);

		var input = L.DomUtil.create('input', className + '-input', form);
		try {
			input.type = 'search';
		}
		catch(e) {
			input.type = 'text'; // IE
		}
		input.placeholder = 'Воспользуйтесь поиском';

		var submit = L.DomUtil.create('button', className + '-submit btn', form);
		submit.type = 'submit';
		submit.innerHTML = 'Найти памятник';

		return container;
	}
});

L.Map.mergeOptions({
	searchControl: true
});

L.Map.addInitHook(function () {
	if (this.options.searchControl) {
		this.searchControl = new L.Control.Search();
		this.addControl(this.searchControl);
	}
});

L.control.search = function (options) {
	return new L.Control.Search(options);
};


/*
 * Comboboxes
 */
L.Control.Location = L.Control.extend({
	options: {
		position: 'topleft',
		id: 'location'
	},

	onAdd: function (map) {
		var className = 'leaflet-control-location',
			container = L.DomUtil.create('div', className);
		L.DomEvent.disableClickPropagation(container);

		$('#' + this.options.id).appendTo($(container));

		return container;
	}
});

L.Map.mergeOptions({
	locationControl: true
});

L.Map.addInitHook(function () {
	if (this.options.locationControl) {
		this.locationControl = new L.Control.Location();
		this.addControl(this.locationControl);
	}
});

L.control.location = function (options) {
	return new L.Control.Location(options);
};

