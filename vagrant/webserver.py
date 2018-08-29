from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import cgi


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>Hello!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say?</h2><input name='message' type='text'>"
				output += "<input type='submit' value='Submit'></form></body></html>"
				
				self.wfile.write(output)
				print output
				return
				
			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>&#161Hola! <a href='/hello'>Back to Hello</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say?</h2><input name='message' type='text'>"
				output += "<input type='submit' value='Submit'></form></body></html>"
				
				self.wfile.write(output)
				print output
				return
				
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body><a href='/restaurants/new'>Make new restaurant</a>"
				
				for rest in session.query(Restaurant).order_by(Restaurant.name):
					output += "<h4> %s <a href='#'>Edit</a><span> </span><a href='#'>Delete</a><br/></h4>" % rest.name
				

				output += "</body></html>"
				self.wfile.write(output)
				print output
				
				return
				
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<h2>Enter new restaurant name</h2><input name='restaurant' type='text'>"
				output += "<input type='submit' value='Create'></form>"
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				
				return
			
				
		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)
	
	def do_POST(self):
		try:
				
			if self.path.endswith("/restaurants/new"):
			
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					restaurant_name = fields.get('restaurant')
					
					restaurant = Restaurant(name = restaurant_name[0])					
					session.add(restaurant)
					session.commit()
					
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
			
					return	
					
				
			"""self.send_response(301)
			self.end_headers()
			
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
				
			output = ""
			output += "<html><body>"
			output += " <h2>Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]
			output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
			output += "<h2>What would you like me to say?</h2><input name='message' type='text'>"
			output += "<input type='submit' value='Submit'></form></body></html>"
			
			self.wfile.write(output)
			print output"""
			
		except:
			pass
			
def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
		
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()
	
if __name__ == '__main__':
	main()