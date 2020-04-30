import tornado.ioloop
import tornado.web

class FormHandler(tornado.web.RequestHandler):
    def get(self):
        param = self.get_argument('message', None)
        if param:
            self.set_header("Content-Type", "text/plain")
            self.write("Zadali jste: "+param)
        else:
            self.set_header("Content-Type", "text/html")
            self.write('<html><body><form action="/form" method="GET">'
                       '<input type="text" name="message">'
                       '<input type="submit" value="OK">'
                       '</form></body></html>')

    post = get

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/form", FormHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
