from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem



engine = create_engine('sqlite:///restaurantmenu.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    items = session.query(Restaurant).order_by(Restaurant.id)
    msgIfEmpty(items)
    return render_template('restaurants.html', items = items)	


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        rest = Restaurant(name = request.form['name'])
        session.add(rest)
        session.commit()
        flash('New restaurant created!')
        return redirect(url_for('showRestaurants'))	
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):	    
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash('Restaurant has been edited!')
        return redirect(url_for('showRestaurants'))	
    else:
        return render_template('editRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):	
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':									
		session.delete(restaurant)
		session.commit()
		flash('Restaurant has been deleted!')
		return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):	
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).order_by(MenuItem.id)
    msgIfEmpty(items)
    return render_template('menu.html', restaurant = restaurant, items = items, courses = getCourses())    
        

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):	    
    if request.method == 'POST':        							
        item = MenuItem(
                restaurant_id = restaurant_id, 
                name = request.form['name'], 
                price = request.form['price'], 
                description = request.form['description'],
                course = request.form['course'])					
        session.add(item)
        session.commit()
        flash('New menu item created!')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id, courses = getCourses())


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):		
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':        
        item.name = request.form['name']
        item.price = request.form['price']
        item.description = request.form['description']
        item.course = request.form['course']				
        session.add(item)
        session.commit()
        flash('Menu Item has been edited!')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:        
        return render_template('editMenuItem.html', i = item, courses = getCourses())


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):		
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':									
		session.delete(item)
		session.commit()
		flash('Menu Item has been deleted!')
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', i = item)


### help methods
def msgIfEmpty(items):
    if items.first() is None:
        flash('You currently have no items.')

def getCourses():
        return ('Appetizer','Entree','Dessert','Beverage')

if __name__ == "__main__":
    	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)