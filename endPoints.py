from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Making an API Endpoint 
@app.route('/restaurants', methods = ['GET','POST'])
def restaurant():
	if request.method == 'GET':
		restaurants = session.query(Restaurant).all()
		return jsonify( Restaurants=[ r.serialize for r in restaurants ] )
	elif request.method == 'POST':
		id = request.args.get('id', '')
		modifiedName = request.args.get('name', '')
		RestaurantToEdit = session.query(Restaurant).filter_by(id = id).one()
		if RestaurantToEdit:
			RestaurantToEdit.name = modifiedName
			print(RestaurantToEdit.name)
			session.add(RestaurantToEdit)
			session.commit()
			return jsonify( Restaurants = RestaurantToEdit.serialize )
		else:
			return jsonify({"error":"No Restaurants Found for id = %s " % (id)})
		

@app.route('/restaurants/<int:restaurant_id>/menu', methods = ['GET','POST'])
def restaurantMenu(restaurant_id):
	if request.method == 'GET':
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
		return jsonify( MenuItems=[ i.serialize for i in items ] )
	elif request.method == 'POST':
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		_name = request.args.get('name', '')
		if restaurant and _name:
			_description = request.args.get('description', '')
			_price = request.args.get('price', '')
			_course = request.args.get('course', '')
			newItem = MenuItem(name=_name, description=_description,
                     price=_price, course=_course, restaurant=restaurant)
			session.add(newItem)
			session.commit()
			return jsonify( Item = newItem.serialize )
		else:
			return jsonify({"error":"No Restaurants Found for id = %s " % (id)})


# Making an API Endpoint (GET Request)
@app.route('/menu/<int:menu_id>/', methods = ['GET','POST','DELETE'])
def menuJSON(menu_id):
	if request.method == 'GET':
		item = session.query(MenuItem).filter_by(id = menu_id).one()
		return jsonify( MenuItems=[ item.serialize ] )
	elif request.method == 'POST':
		itemToEdit = session.query(MenuItem).filter_by(id = menu_id).one()
		
		if itemToEdit:
			modifiedName = request.args.get('name', '')
			description = request.args.get('description', '')
			price = request.args.get('price', '')
			course = request.args.get('course', '')
			if modifiedName:
				itemToEdit.name = modifiedName
			if description:
				itemToEdit.description = description
			if price:
				itemToEdit.price = price
			if course:
				itemToEdit.course = course
			session.add(itemToEdit)
			session.commit()
			return jsonify( Item = itemToEdit.serialize )
		else:
			return jsonify({"error":"No Restaurants Found for id = %s " % (id)})
	elif request.method == 'DELETE':
		itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
		if itemToDelete:
			session.delete(itemToDelete)
			session.commit()
			return ("Menu %s is deleted " % menu_id)
		else:
			return "Menu %s id is incorrect." % menu_id



if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5678)
    # 0.0.0.0 allows for all the public ips