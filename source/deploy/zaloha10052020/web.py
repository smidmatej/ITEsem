import tornado.ioloop
import tornado.web
import tornado.template as template
import sqlite3


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('html/index.html')

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM measurements')
        items = c.fetchall()
        items = [str(item) for item in items]
        print(items)
        self.render('html/data.html',items=items)


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
        (r"/name", NameHandler),
        (r"/data", DataHandler)
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

 
