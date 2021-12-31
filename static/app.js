function initMap() {
  const options = {
    zoom: 8,
    center: { lat: -25.344, lng: 131.036 },
  };

  const map = new google.maps.Map(document.getElementById('map'), options);

  const markers = locations.map((position, i) => {
    const label = labels[i % labels.length];
    const marker = new google.maps.Marker({
      position,
      label,
    });
  });
}

let url = 'https://api.openbrewerydb.org/breweries';

function getData() {
  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw Error('Something went wrong');
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      const latLong = data.map((brewery) => {
        return brewery.latitude && brewery.latitude;
      });
      console.log(latLong);
    });
}
getData();
