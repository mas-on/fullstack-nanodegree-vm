from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#session.add(MenuItem(restaurant_id = 4, name = "vegetable salad" ))
#session.add(MenuItem(restaurant_id = 2, name = "chicken pizza" ))

#for item in session.query(MenuItem):
#	item.price = "$1.99"
#	item.description = "delicious food"
#session.commit()

@app.route('/')
#@app.route('/hello')
#def HelloWorld():
	#return "Hello world!"

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	#restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()	
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)	
	
	output = ''
	for i in items:
		output += '%s<br/>' % i.name 
		output += '%s<br/>' % i.price
		output += '%s<br/>' % i.description 		
		output += '<br/>'
	
	return output
	
	
if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)