#!/usr/bin/env python3
# -*- coding:  utf-8
import socket
import random
import json
import http.server
import socketserver
import urllib.parse
from twitter_db import TwitterDB


class HttpHandler(http.server.SimpleHTTPRequestHandler):
    """Implementation d'un handler http simple:
        - fournit des fichiers (via SimpleHTTPRequestHandler)
        - parse et execute des commandes passées via des paramètres GET"""


    def __init__(self, *args, **kwargs):
        self._session_id = None
        self.db = TwitterDB()
        super().__init__(*args, **kwargs)


    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def send_JSON(self, json):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.encode(encoding='utf_8'))
        return

    def do_GET(self):
        """Méthode à surcharger pour répondre à une requête HTTP get"""

        #Parsing the l'URL
        parsed_url = urllib.parse.urlparse(self.path)
        #Extraction des paramètres GET sous la forme d'un dictionnaire python
        #?p1=v1&p2=v2&...&pn=vn devient { 'p1' : ['v1'], …, 'pn':['vn'] }
        #Les paramètres de même noms sont fusionnés:
        #?p=v1&p=v2  devient { 'p': [ 'v1', 'v2' ]
        parameters = urllib.parse.parse_qs(parsed_url.query)
        print ("Resource : '" + parsed_url.path+"'")
        print ("Paramètres : "+str(parameters))

        content = ""

        #Index
        if parsed_url.path == "/":
            super().do_GET()
        #Search query
        elif parsed_url.path == "/search":
            print("Search Query")
            if 'q' not in parameters:
                print("No query parameter")
                self.send_error(404, "No Query parameter (q) found")
            else:
                val = self.db.search(str(parameters['q'][0]))
                if 'hashtags' in val:
                    val['hashtags'] = dict(val['hashtags'])
                if 'places' in val:
                    val['places'] = dict(val['places'])
                val = json.dumps(dict(val))
                print("search done : "+str(val))
                self.send_JSON(val)


class ExtensibleHttpServer(socketserver.TCPServer):
    """Serveur HTTP qui étend celui donné par défaut. 2 Améilorations
       - on configure la socket pour pouvoir redémarrer immédiatement le serveur
         si jamais on quitte le programme et on le relance (sinon   il
         faut attendre le timeout de la socket)
       - on ajoute une méthode serve_until_interrupted qui rattrape le CTRL-C dans le terminal.
"""

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def serve_until_interrupted(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.shutdown()
        finally:
            self.server_close()


#Exemple d'utilisation :
#Naviguer sur http://localhost:9010 après avoir lancé le serveur et observer la console

if __name__ == "__main__":
    HTTPD = ExtensibleHttpServer(("127.0.0.1", 9010), HttpHandler)
    HTTPD.serve_until_interrupted()
