# RestaurantMenu
Small Project for Full Stack Application using Python Flask Framework and Relational Database

Here are the steps to demo the small application
1. execute database_setup.py to create the database with 'Restaurant' and 'MenuItem' Table
2. execute lotsofmenus.py to insert something into the tables

a. Web browsing

a1. execute project.py to load up the server on your localhost
a2. open up your browser and type in the address localhost:5678/ to start using the application

b. RESTful API

b1. execute endPoints.py to load up the server on your localhost
b2. use cURL/POSTMAN to send corresponding request

GET
1. List of restaurants : localhost:5678/restaurants/
2. Menu in a specific restaurant : localhost:5678/restaurants/<r_id>/menu
3. Specific menu : localhost:5678/menu/<m_id>

POST
1. To modify the name of a specific restaurant : localhost:5678/restaurants?id=<r_id>&name=<new_name>
2. To add a new item into a specific restaurant : 
          localhost:5678/restaurants/<r_id>/menu?name=<new_name>&description=<>&price=<>&course=<>
   # name if mandatory for adding / other features are optional
3. To edit a specific menu : localhost:5678/menu/<m_id>/?name=<new_name>&description=<>&price=<>&course=<>

DELETE
1. Specific Menu: localhost:5678/menu/<m_id>
