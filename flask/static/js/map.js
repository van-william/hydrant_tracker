let map;
let selectedMarker;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 41.8781, lng: -87.6298 },
        zoom: 8
    });

    // Loop through hydrantPoints to add them as markers
    hydrantPoints.forEach(function(point) {
        let marker = new google.maps.Marker({
            position: { lat: point.latitude, lng: point.longitude },
            map: map,
            title: `Hydrant ID: ${point.id}`  // Example title
        });

        // Add click event listener to each marker
        marker.addListener('click', function() {
            // Handle marker click event
            // You can show a form or update data here
            // Example: prompt for new data and submit a form to '/update_point/point_id'
        });
    });
}

window.onload = initMap;
