# RestaurantMenu
Small Project for Full Stack Application using Python Flask Framework and Relational Database

Here are the steps to demo the small application
1. execute database_setup.py to create the database with 'Restaurant' and 'MenuItem' Table
2. execute lotsofmenus.py to insert something into the tables
3. execute project.py to load up the server on your localhost
4. open up your browser and type in the address localhost:678 to start using the application

RESTFUL API is also available in JSON format

1. List of restaurants : http://localhost:5678/restaurants/JSON
2. Menus in a restaurant : http://localhost:5678/restaurants/<restaurant_id>/menu/JSON
2. Specific Menu: http://localhost:5678/restaurants/<restaurant_id>/menu/<menu_id>/JSON
