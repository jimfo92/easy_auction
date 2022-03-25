# ebay_clone
e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Features
  - Register and login.
  - Create Listing: Users should be able to visit a page to create a new listing.
  - Active Listings Page: The default route of web application should let users view all of the currently active auction listings.
  - Listing Page: Clicking on a listing should take users to a page specific to that listing.
  - Watchlist: Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist.
  - Categories: Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.
  
## Install
In your terminal, `cd` into the project directory.
  ```
  python manage.py makemigrations
  python manage.py migrate
  
  python manage.py runserver
  ```
