from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def defaultRestaurant():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurant.html', restaurants = restaurants)

@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET','POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash("Restaurant Name " + editedRestaurant.name + " Edited!")
		return redirect(url_for('defaultRestaurant'))
	else:
		return render_template('editRestaurant.html', restaurant = editedRestaurant)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], 
						   description = request.form['description'],
						   price = request.form['price'],
						   course = request.form['course'],
			               restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New Menu Item " + newItem.name + " Created!")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description'].strip():
			editedItem.description = request.form['description']
		if request.form['price'].strip():
			editedItem.price = request.form['price']
		if request.form['course'].strip():
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		flash("Menu Item " + editedItem.name + " Edited!")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = editedItem)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		name = deletedItem.name
		session.delete(deletedItem)
		session.commit()
		flash("Menu Item " + name + " Deleted!")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id,i = deletedItem)

# Making an API Endpoint (GET Request)
@app.route('/restaurants/JSON')
def restaurantJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify( Restaurants=[ r.serialize for r in restaurants ] )


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	return jsonify( MenuItems=[ i.serialize for i in items ] )

# Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify( MenuItems=[ item.serialize ] )


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
    # 0.0.0.0 allows for all the public ips
