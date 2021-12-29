const searchBar = document.querySelector('#brew-search');
const info = document.querySelector('#info');
API_URL = 'https://api.openbrewerydb.org/breweries';

const findBrew = (e) => {
  e.preventDefault();

  info.innerHTML = '';

  const links = document.querySelector('#card a');
  const name = document.querySelector('[id=search-name]').value;
  const state = document.querySelector('[id=search-state]').value;
  const city = document.querySelector('[id=search-city]').value;

  if (city != '') {
    info.innerHTML += `<h2 class="center-text result-header"> Showing Results for ${city}</h2>`;
    const url = `${API_URL}?by_city=${city}`;
    const data = fetch(url);
    console.log(data);

    data
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          data.forEach((brewery) => {
            info.innerHTML += `
            <div class="brewery-section center-text">
            <div class="card center-text">
            <h2>${brewery.name}</h2>
            <p class="web-url font-weight-bold"><a href="${brewery.website_url}">${brewery.website_url}</a></p>
            <p class="font-weight-bold">Type: ${brewery.brewery_type}</p>
            <p class="font-weight-bold">Address: ${brewery.street}, ${brewery.city}, ${brewery.state}, ${brewery.country}</p>
            </div>
            </div>
            `;
          });
        } else {
          info.innerHTML += "<h2 class='center-text'>No Results</h2>";
        }
      });
  } else {
    if (name && !state) {
      info.innerHTML += `<h2 class='center-text result-header'>Showing breweries under ${name}</h2>`;
    } else if (state && !name) {
      info.innerHTML += `<h2 class='center-text result-header'>Showing breweries inside ${state}</h2>`;
    } else {
      info.innerHTML += `<h2 class='center-text result-header'>Showing breweries for ${name}, ${state}</h2>`;
    }
    const url = `${API_URL}?by_name=${name}&by_state=${state}`;
    const data = fetch(url);
    console.log(data);

    data
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          data.forEach((brewery) => {
            info.innerHTML += `
            <div class="brewery-section center-text">
            <div class="card center-text">
            <h2>${brewery.name}</h2>
            <p class="web-url font-weight-bold"><a href="${brewery.website_url}">${brewery.website_url}</a></p>
            <p class="font-weight-bold">Type: ${brewery.brewery_type}</p>
            <p class="font-weight-bold">Address: ${brewery.street}, ${brewery.city}, ${brewery.state}, ${brewery.country}</p>
            </div>
            </div>
            `;
          });
        } else {
          info.innerHTML += "<h2 class='center-text'>No Results</h2>";
        }
        searchBar.reset();
      });
  }
};

searchBar.addEventListener('submit', findBrew);
