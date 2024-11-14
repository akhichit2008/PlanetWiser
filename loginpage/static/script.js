// Initialize Leaflet map
var map = L.map('map').setView([51.505, -0.09], 13);

// Load tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Add marker on click
var marker;
map.on('click', function(e) {
    if (marker) {
        map.removeLayer(marker);
    }
    marker = L.marker(e.latlng).addTo(map);
    document.getElementById('address').value = e.latlng.lat + ", " + e.latlng.lng; // Save coordinates in address field
});

// Update map based on address input
document.getElementById('address').addEventListener('change', function() {
    var address = this.value;

    // Using OpenStreetMap Nominatim API to get latitude and longitude
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${address}`)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                var lat = data[0].lat;
                var lon = data[0].lon;
                map.setView([lat, lon], 13); // Center the map on the address
                if (marker) {
                    map.removeLayer(marker);
                }
                marker = L.marker([lat, lon]).addTo(map); // Place a marker
            } else {
                alert("Address not found. Please enter a valid address.");
            }
        })
        .catch(err => console.error(err));
});