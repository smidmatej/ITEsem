#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.ioloop
import tornado.web
import tornado.template as template



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')





if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
    ])
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()

