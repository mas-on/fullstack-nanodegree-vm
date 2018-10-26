from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem



engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    items = session.query(Restaurant).all()
    if items.first() is None:
        flash('You currently have no items.')
    return render_template('restaurants.html', items = items)	


@app.route('/restaurant/new')
def newRestaurant():	
    return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):	
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    return render_template('editRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):	
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    return render_template('deleteRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):	
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    if items.first() is None:
        flash('You currently have no items.')
    return render_template('menu.html', restaurant = restaurant, items = items)    
        

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):	    
    return render_template('newMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):		
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return render_template('editMenuItem.html', i = item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):		
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return render_template('deleteMenuItem.html', i = item)


if __name__ == "__main__":
    	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)