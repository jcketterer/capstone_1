// Initialize and add the map
function initMap() {
  const lat = document.getElementById('lat').innerText;
  const long = document.getElementById('long').innerText;
  console.log(lat);
  console.log(long);

  // The location of Uluru
  const uluru = { lat: parseInt(lat), lng: parseInt(long) };
  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: uluru,
  });
  // The marker, positioned at Uluru
  const marker = new google.maps.Marker({
    position: uluru,
    map: map,
  });
}
