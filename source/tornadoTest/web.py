import tornado.ioloop
import tornado.web
import tornado.template as template



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Tohle je domov")

class FormHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_cookie('name', 'NONAME')
        param = self.get_argument('message', None)
        if param:
            self.set_header("Content-Type", "text/plain")
            self.write(name+" napsal: "+param)
        else:
            self.set_header("Content-Type", "text/html")
            self.render('index.html', name=name)


class NameHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name', None)
        if name is not None:
            self.set_cookie('name', name)
        else:
            name = self.get_cookie('name', 'NONAME')

        self.set_header("Content-Type", "text/html")
        self.write('<html><body> Ahoj ' + name + ', napis svoje novy jmeno pls '+ 
                   '<form action="/name" method="GET">'
                   '<input type="text" name="name" >'
                   '<input type="submit" value="OK" >'
                   '</form></body></html>')



if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/form", FormHandler),
        (r"/name", NameHandler),
    ])
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()

