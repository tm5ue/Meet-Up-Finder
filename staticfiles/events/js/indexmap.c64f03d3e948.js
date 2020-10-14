var longitude = -78.5176329005563; // Default to Charlottesville because why not
var latitude = 38.008261664962625;
getLocation();

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alrt("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
    mapboxgl.accessToken = 'pk.eyJ1IjoibmNvb25leSIsImEiOiJja2c2dDFhNXMwMG1uMnltdXNocGJyaXB4In0.hZEsOS4rcPya0rSBefUh7A';
    var map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [longitude, latitude], // starting position
        zoom: 9, // starting zoom
    });
    var marker = new mapboxgl.Marker()
        .setLngLat([longitude, latitude])
        .addTo(map);

    var layerList = document.getElementById('menu');
    var inputs = layerList.getElementsByTagName('input');

    function switchLayer(layer) {
        var layerId = layer.target.id;
        map.setStyle('mapbox://styles/mapbox/' + layerId);
    }

    for (var i = 0; i < inputs.length; i++) {
        inputs[i].onclick = switchLayer;
    }

    var latitudes = [
        {% for event in object_list %}
            '{{ event.get_latitude }}',
        {% endfor %}
    ];
    var longitudes = [
        {% for event in object_list %}
            '{{ event.get_longitude }}',
        {% endfor %}
    ];
    var desciptions = [
        {% for event in object_list %}
            '{{ event.description }}',
        {% endfor %}
    ];
    var names = [
        {% for event in object_list %}
            '{{ event.name }}',
        {% endfor %}
    ];
    var dates = [
        {% for event in object_list %}
            '{{ event.event_date }}',
        {% endfor %}
    ];
    var identifiers = [
        {% for event in object_list %}
            '{{ event.name }}' + Math.random().toString(36).substr(2, 5),
        {% endfor %}
    ];

    // Add zoom and rotation controls to the map.
    map.addControl(new mapboxgl.NavigationControl());

    map.on('load', function () {
        for (let i = 0; i < names.length; i++) {
            map.addSource(identifiers[i], {
                'type': 'geojson',
                'data': {
                    'type': 'FeatureCollection',
                    'features': [
                    {
                        'type': 'Feature',
                        'properties': {
                            'description':
                            '<strong>' + names[i] + '<p>'+ desciptions[i] + '<br>' + dates[i] + '</p>',
                            'icon': 'information'
                        },
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [parseFloat(longitudes[i]), parseFloat(latitudes[i])]
                        }
                    },
                    ]
            }
            });
        }

        for (let i = 0; i < names.length; i++) {

            // Add a layer showing the places.
            map.addLayer({
                'id': identifiers[i],
                'type': 'symbol',
                'source': identifiers[i],
                'layout': {
                    'icon-image': '{icon}-15',
                    'icon-allow-overlap': true
                }
            });

            // When a click event occurs on a feature in the places layer, open a popup at the
            // location of the feature, with description HTML from its properties.
            map.on('click', identifiers[i], function (e) {
                var coordinates = e.features[0].geometry.coordinates.slice();
                var description = e.features[0].properties.description;

                // Ensure that if the map is zoomed out such that multiple
                // copies of the feature are visible, the popup appears
                // over the copy being pointed to.
                while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                    coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
                }

                new mapboxgl.Popup()
                .setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
            });

            // Change the cursor to a pointer when the mouse is over the places layer.
            map.on('mouseenter', identifiers[i], function () {
                map.getCanvas().style.cursor = 'pointer';
            });

            // Change it back to a pointer when it leaves.
            map.on('mouseleave', identifiers[i], function () {
                map.getCanvas().style.cursor = '';
            });
        }
    });

}