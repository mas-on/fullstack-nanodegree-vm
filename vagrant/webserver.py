from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
	except KeyboardInterrupt:
	
if __name__ == '__main__':
	main()