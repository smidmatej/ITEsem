import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/test", MainHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
