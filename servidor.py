#!/usr/bin/env python3

import argparse

import sys
import itertools
import socket
from socket import socket as Socket

import os
#from pathlib import Path

# A simple web server

# Issues:
# Ignores CRLF requirement
# Header must be < 1024 bytes
# ...
# probabaly loads more


def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
    args = parser.parse_args()
	
    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    #with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    ss = Socket(socket.AF_INET, socket.SOCK_STREAM)
    # COMPLETE (1)

    # The socket stays connected even after this script ends. So in order
    # to allow the immediate reuse of the socket (so that we can kill and
    # re-run the server while debugging) we set the following option. This
    # is potentially dangerous in real code: in rare cases you may get junk
    # data arriving at the socket.
	
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # COMPLETE (2)
    endpoint = ('', args.port)
    # COMPLETE (3)
    ss.bind(endpoint)
    ss.listen(1)
	
    print("server ready")
    
    while True:

     cs = ss.accept()[0]
     request = cs.recv(1024).decode('ascii')
     print(request)
     reply = http_handle(request)
     cs.send(reply.encode('ascii'))


     print("\n\nReceived request")
     print("======================")
     print(request.rstrip())
     print("======================")


     print("\n\nReplied with")
     print("======================")
     print(reply.rstrip())
     print("======================")
    
    return 0


def http_handle(request_string):
    """Given a http requst return a response

    Both request and response are unicode strings with platform standard
    line endings.
    """

    assert not isinstance(request_string, bytes)


    # Fill in the code to handle the http request here. You will probably want
    # to write additional functions to parse the http request into a nicer data
    # structure (eg a dict), and to easily create http responses.

    # COMPLETE (4)
    # esta funcion DEBE RETORNAR UNA CADENA que contenga el recurso (archivo)
    # que se consulta desde un navegador e.g. http://localhost:2080/index.html
    # En el ejemplo anterior se esta solicitando por el archivo 'index.html'
    # Referencias que pueden ser de utilidad
    # - https://www.acmesystems.it/python_http, muestra como enviar otros
    #                                           archivos ademas del HTML
    # - https://goo.gl/i7hJYP, muestra como construir un mensaje de respuesta
    #                          correcto en HTTP
    #print request.request_version
    #print request.path
    
    #if (request_string.path[0] == "/"):
       #esta el archivo que pide?
       #
     #  with open(request_string.path[1:]) as myfile:
     #          data = myfile.read()
     #  headers = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "Connection: close\n" + "\n"
     #  answer = "%s%s\n"(headers,data)

    #return answer

    metodo = request_string.split()[0]
    path = request_string.split()[1].split('/')[1]
    print metodo
    print path
    
    #with open(path) as myfile:
	#	data = myfile.read()
    
    #headers = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "Connection: close\n" + "\n"
    #answer = "%s%s\n"(headers,data)
    #return answer
    
    #self.path = path
    try:
		sendReply = False
		if path.endswith(".html"):
			mimetype = 'text/html'
			sendReply = True
			
		if path.endswith(".jpg"):
			mimetype = 'image/jpg'
			sendReply = True
			
		if path.endswith(".gif"):
			mimetype = 'image/gif'
			sendReply = True
			
		if path.endswith(".js"):
			mimetype = 'application/javascript'
			sendReply = True
			
		if path.endswith(".css"):
			mimetype = 'text/css'
			sendReply = True
			
		if sendReply == True:
			#f = open(curdir + sep + path)
			f = open(path)
			data = f.read()
			headers = "HTTP/1.1 200 OK\n" + "Content-Type: " + mimetype + "\n" + "Connection: close\n" + "\n"
			print headers
			print data
			#answer = "%s%s\n"(headers, data)
			answer = (headers, data)
			f.close()
		
		return answer
		
    except IOError:
		print ("ERROR 404. Ruta No Valida")

if __name__ == "__main__":
    sys.exit(main())
