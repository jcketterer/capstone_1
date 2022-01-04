# Brewery App

I am using the Open Brewery App for my capstone project.

[Open Brewery DB](https://www.openbrewerydb.org)

[Google Maps API](https://developers.google.com/maps)

![Brewery App Schema](/images/schema_photo.png)

https://capstone-one.herokuapp.com/

My App is a simple brewery searching application where you can create a user account and search for different breweries in the US as well as abroad in Ireland and UK.

I wanted to make sure that the user could search for breweries in a few different ways. So I implemented a search by name of brewery, state, and city.

The user can choose to create an account or not. This will not inhibit them from searching the breweries.

As stated before depending on how the recolect the brewery there are three different avenues to choose from. If the user chooses to create an account they will have a profile where they will be able to edit their account and change their username and favorite brewery.

I used two api's the main api was the brewery api where I used for the name, city, and state search but I also incorporated all the brewery from a csv file and loaded the data into my database. This was very helpful to creat a large comprehensive list of all breweries. Within the table the brewery name is a link to take you to the brewery info card that will produce a single page with a map and the information about the brewery. The map was used with JavaScript and the google maps API.

# Tech stack

HTML5, CSS, Javascript, Python, Flask, WTForms, SQLAlchemy, PostgreSQL, Jinja, and Heroku.

# Further Additions

Eventually I would like to add the ability to like a brewery when a user is logged in. That would save and commit to my database. I have the model already spun up I need to add the routes. Another great addition would be to add an age gate. Essentially have the user enter in their date of birth when signing up (which they already do) and if they are not 21 years or older it will flash an error and send them back to the home page. This
