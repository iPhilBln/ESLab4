import os
import time
from src.camera import *
from os import curdir, sep
from http.server import BaseHTTPRequestHandler,HTTPServer

class myHandler(BaseHTTPRequestHandler):
    """Klasse zur Darstellung des Browserinhalts."""
    #Handler für GET Anfragen
    def do_GET(self):
        write_webpage()
        browser = get_camListValue('browser')
        telegram = get_camListValue('telegram')
        telegram_sketch = get_camListValue('telegram_sketch')

        if self.path.endswith('browser.jpg'):
            self.path = '{}'.format(browser.path + browser.name + '.jpg')
        elif self.path.endswith('telegram.jpg'):
            self.path = '{}'.format(telegram.path + telegram.name + '.jpg')
        elif self.path.endswith('telegram_sketch.jpg'):
            self.path = '{}'.format(telegram_sketch.path + telegram_sketch.name + '.jpg')
        elif self.path=="/":
            self.path="src/upload.html"

        try:
            #mimetype festlegen
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #je nach mimetype wird der Inhalt gerendert und dargestellt
                if mimetype == 'image/jpg':
                    f = open(self.path, "rb")
                else:
                    f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def write_webpage() -> None:
    """Schreibt die upload.html Datei in Abhängig des Speicherortes des Bildes."""
    browser = get_camListValue('browser')
    browser.get_picture()
    telegram = get_camListValue('telegram')
    telegram_sketch = get_camListValue('telegram_sketch')

    bildBrowser : str = "<img src=\"{}\" ".format(browser.path + browser.name + '.jpg') + "width=\"{}\" ".format(browser.width) + "height=\"{}\"".format(browser.height) + ">"
    bildTelegram : str = "<img src=\"{}\" ".format(telegram.path + telegram.name + '.jpg') + "width=\"{}\" ".format(browser.width) + "height=\"{}\"".format(browser.height) + ">"
    bildTelegram_skretch : str = "<img src=\"{}\" ".format(telegram_sketch.path + telegram_sketch.name + '.jpg') + "width=\"{}\" ".format(browser.width) + "height=\"{}\"".format(browser.height) + ">"
    timeinfo : str = "Uhrzeit: " + time.strftime("%d.%m.%Y - %H:%M:%S h")

    page = "<!DOCTYPE html>\
            <html>\
            <head>\
            <title>Embedded Systems Projektarbeit</title>\
            </head>\
            <body>\
            <center><h1>Embedded Systems Projektarbeit</h1></center>\
            <center>\
            <figure>" + bildBrowser + "\
            <figcaption>Browseraufnahme</figcaption>\
            </figure>\
            </center>\
            <center>\
            <figure>" + bildTelegram + "\
            <figcaption>Telegramaufnahme ohne Filter</figcaption>\
            </figure>\
            </center>\
            <center>\
            <figure>" + bildTelegram_skretch + "\
            <figcaption>Telegramaufnahme mit Filter: Sketch</figcaption>\
            </figure>\
            </center>\
            <center>" + timeinfo + "</center>\
            </body>\
            </html>"

    filePath = r'./src/upload.html'
    with open(filePath, 'w') as f:
        f.write(page)

def start_static_webserver():
    """Startet den Webbrowser und wartet auf einkommende Anfragen unter PORT_NUMBER"""
    PORT_NUMBER = 8080

    try:
    	server = HTTPServer(('', PORT_NUMBER), myHandler)
    	print('Started httpserver on port {}'.format(PORT_NUMBER))

    	server.serve_forever()

    except KeyboardInterrupt:
    	print(' received, shutting down the web server')
    	server.socket.close()
