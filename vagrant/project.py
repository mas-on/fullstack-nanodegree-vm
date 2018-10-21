from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem



engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#session.add(MenuItem(restaurant_id = 4, name = "vegetable salad" ))
#session.add(MenuItem(restaurant_id = 2, name = "chicken pizza" ))

#for item in session.query(MenuItem):
#	item.price = "$1.99"
#	item.description = "delicious food"
#session.commit()

#Making an API endpoint
@app.route('/restaurants/<int:restaurant_id>/menu/json')
def RestaurantMenuJson(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json')
def MenuItemJson(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()	
	return jsonify(MenuItem = item.serialize)

@app.route('/')
def DefaultRestaurantMenu():	
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template('menu.html', restaurant = restaurant, items = items)	
	
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant = restaurant, items = items)

#Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):	
	if request.method == 'POST':							
		item = MenuItem(restaurant_id = restaurant_id, name = request.form['name'], price = request.form['price'], description = request.form['description'])					
		session.add(item)
		session.commit()
		flash('New menu item created!')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
		
	else: #GET
		item = MenuItem(restaurant_id = restaurant_id)
		return render_template('editMenuItem.html', caption='Enter new menu item', i = item)
	#return "page to create a new menu item. Task 1 complete!"

#Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()	
	if request.method == 'POST':								
		item.name = request.form['name']
		item.price = request.form['price']
		item.description = request.form['description']				
		session.add(item)
		session.commit()
		flash('Menu Item has been edited!')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
		
	else: #GET		
		return render_template('editMenuItem.html', caption='Edit this menu item', i = item)
	#return "page to edit a new menu item. Task 2 complete!"

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':									
		session.delete(item)
		session.commit()
		flash('Menu Item has been deleted!')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:#GET		
		return render_template('deleteMenuItem.html', i = item)
	#return "page to delete a new menu item. Task 3 complete!"
	
	
if __name__ == "__main__":
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)