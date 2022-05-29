#https://stackoverflow.com/questions/22139193/cant-get-tornado-staticfilehandler-to-work
import time
import tornado.ioloop
import tornado.web
import tornado.httpserver
from src.camera import *

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/upload.html", MainHandler)
        ]
        settings = {
            "template_path": "/home/phil/Uniprojekte/",
        }
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # schreibe Webseitenkontent
        self.render("upload.html")

def write_webpage() -> None:
    browser = get_camListValue('browser')
    browser.get_picture()
    content = "<img src=\"{}\" ".format(browser.path + browser.name + '.jpg') + "width=\"{}\" ".format(browser.width) + "height=\"{}\"".format(browser.height) + ">"

    # aktuelle Systemzeit abrufen und formatieren
    timeinfo = "Uhrzeit: " + time.strftime("%d.%m.%Y - %H:%M:%S h")
    page = "<!DOCTYPE html>\
            <html>\
            <head>\
            <title>\"Embedded Systems Projektarbeit\"</title>\
            </head>\
            <body>\
            <center><h1>\"Embedded Systems Projektarbeit\"</h1></center>\
            <center>" + content + "</center>\
            <center>" + timeinfo + "</center>\
            </body>\
            </html>"
    with open('./src/upload.html', 'w') as f:
        f.write(page)

# verbinde MainHandler mit App
def start_static_webserver():
    write_webpage()
    try:
        """
        applicaton = Application()
        http_server = tornado.httpserver.HTTPServer(applicaton)
        http_server.listen(8081)

        #tornado.ioloop.IOLoop.instance().start()
        tornado.ioloop.IOLoop.current().start()


        browser = get_camListValue('browser')
        #static_path = os.path.join(os.path.dirname(__file__),"static"))
        app = tornado.web.Application([
            (   r'/', MainHandler),
            (   r'/(.*)', \
               tornado.web.StaticFileHandler, \
               {'path':r'/home/phil/Uniprojekte/Lab4'}),
        ])
        """
        applicaton = Application()
        app = tornado.web.Application(applicaton)
        app.listen(8081)
        tornado.ioloop.IOLoop.current().start()

    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
        #tornado.ioloop.IOLoop.instance().stop()
