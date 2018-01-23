#!/usr/bin/env python3
import socket
import random
import http.server
import socketserver
import urllib.parse


class HttpHandler(http.server.SimpleHTTPRequestHandler):
    """Implementation d'un handler http simple:
        - fournit des fichiers (via SimpleHTTPRequestHandler)
        - parse et execute des commandes passées via des paramètres GET"""


    def __init__(self, *args, **kwargs):
        self._session_id = None
        super().__init__(*args, **kwargs)




    def do_GET(self):
        """Méthode à surcharger pour répondre à une requête HTTP get"""

        #Parsing the l'URL
        parsed_url = urllib.parse.urlparse(self.path)
        #Extraction des paramètres GET sous la forme d'un dictionnaire python
        #?p1=v1&p2=v2&...&pn=vn devient { 'p1' : ['v1'], …, 'pn':['vn'] }
        #Les paramètres de même noms sont fusionnés:
        #?p=v1&p=v2  devient { 'p': [ 'v1', 'v2' ]
        parameters = urllib.parse.parse_qs(parsed_url.query)
        print ("Resource :")
        print (parsed_url.path)
        print ("Paramètres :")
        print (parameters)

        #L'appel à la méthode parente SimpleHTTPRequestHandler qui va renvoyer le fichier
        #On n'est pas obligé de l'appeler.
        super().do_GET()




class ExtensibleHttpServer(socketserver.TCPServer):
    """Serveur HTTP qui étend celui donné par défaut. 2 Améilorations
       - on configure la socket pour pouvoir redémarrer immédiatement le serveur
         si jamais on quitte le programme et on le relance (sinon il
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
    HTTPD = ExtensibleHttpServer(("localhost", 9010), HttpHandler)
    HTTPD.serve_until_interrupted()
