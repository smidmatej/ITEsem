from __future__ import print_function
from tornado.web import StaticFileHandler, Application as TornadoApplication
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
import tornado.gen

from os.path import dirname, join as join_path
from datetime import datetime
import logging

logging.basicConfig(
    format='%(asctime)s: [%(levelname)s] - %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.DEBUG)

class MainHandler(tornado.web.RequestHandler):

    def initialize(self, log):
        self.log = log

    def get(self):
        self.render('./templates/my_page_ws.html', log=reversed(self.log))

class EchoWebSocket(WebSocketHandler):

    def initialize(self, log):
        self.log = log

    @tornado.gen.coroutine
    def open(self):
        logging.info('Websocket opened')

        def run(*args):
            logging.info('Sending a message to the client...')
            self.write_message(u'Server ready.')

        # 1s delayed
        IOLoop.current().call_later(1, run)

    def on_message(self, message):
        logging.info('<- '+str(message))
        self.log.append('{:{dfmt} {tfmt}} - {}'.format(
            datetime.now(), message, dfmt='%d.%m.%Y', tfmt='%H:%M:%S'))
        logging.info('-> You said: '+str(message))
        self.write_message(u'You said: {}'.format(message))

    def on_close(self):
        logging.info('Websocket closed')


if __name__ == '__main__':
    
    log = ['pes']

    # Handlers (access points)
    app = TornadoApplication([
        (r'/', MainHandler, {'log': log}),
        (r'/websocket', EchoWebSocket, {'log': log}),
        (r'/(.*)', StaticFileHandler, {
            'path': join_path(dirname(__file__), 'assets')}),
    ])
    
    # Port
    TORNADO_PORT = 8881
    app.listen(TORNADO_PORT)
    
    # Start the server
    IOLoop.current().start()
