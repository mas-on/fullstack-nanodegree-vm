from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
app = Flask(__name__)


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Restaurant, MenuItem



# engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind = engine)
# session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():	
	#restaurant = session.query(Restaurant).first()
	#items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	#return render_template('menu.html', restaurant = restaurant, items = items)	
	return "This page will show all my restaurants"


@app.route('/restaurant/new')
def newRestaurant():	
    return "This page will be for making a new restaurant"

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):	
    return "This page will be for editing restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):	
    return "This page will be for deleting restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):	
    return "This page is the menu for restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):		
	return "This page is for making a new menu item for restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):		
	return "This page is for editing menu item %s for restaurant %s" % (menu_id, restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):		
	return "This page is for deleteng menu item %s for restaurant %s" % (menu_id, restaurant_id)


if __name__ == "__main__":
    	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)