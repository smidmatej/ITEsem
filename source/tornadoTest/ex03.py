import tornado.ioloop
import tornado.web

NONAME = 'NONAME'

class FormHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_cookie('name', NONAME)

        param = self.get_argument('message', None)
        if param:
            self.set_header("Content-Type", "text/plain")
            self.write("Jmenujete se "+name+" a zadali jste: "+param)
        else:
            self.set_header("Content-Type", "text/html")
            self.write('<html><body>Jmenujete se '+name+', zadejte text'
                       '<form action="/form" method="GET">'
                       '<input type="text" name="message" >'
                       '<input type="submit" value="OK" >'
                       '</form></body></html>')


class NameHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name', None)
        if name is not None:
            self.set_cookie('name', name)
        else:
            name = self.get_cookie('name', NONAME)

        self.set_header("Content-Type", "text/html")
        self.write('<html><body>Jmenujete se '+name+', zadejte nove jmeno'
                   '<form action="/name" method="GET">'
                   '<input type="text" name="name" >'
                   '<input type="submit" value="OK" >'
                   '</form></body></html>')


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/form", FormHandler),
        (r"/name", NameHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
