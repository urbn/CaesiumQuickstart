
import tornado.ioloop
import tornado.web
from tornado.options import options
import tornado.httpserver
from caesium.handler import BaseRestfulMotorHandler
from caesium.document import BaseAsyncMotorDocument, AsyncRevisionStackManager
from settings import settings
import logging

class CommentHandler(BaseRestfulMotorHandler):
    """
    An example handler for a Comment resource

    """

    #JSON Schema definition is used for validation of post/put bodies
    SCHEMA = {
        "title":"Example Comment Schema",
        "type": "object",
        "required": ["title", "username", "text"],
        "properties" : {
            "title": {
                "type": "string",
            },
            "username": {
                "type": "string",
            },
            "text": {
                "type": "string",
            }
        }
    }

    def initialize(self):
        super(self.__class__, self).initialize()
        self.object_name = "comment"
        self.client = BaseAsyncMotorDocument(self.object_name, self.settings, schema=self.SCHEMA)

url_patterns = [
    (r"/comment", CommentHandler),
    (r"/comment/([0-9a-zA-Z]+)", CommentHandler),
]

class App(tornado.web.Application):

    def __init__(self):
        """App wrapper constructor, global objects within our Tornado platform should be managed here."""
        self.logger = logging.getLogger(self.__class__.__name__)
        tornado.web.Application.__init__(self, url_patterns, **settings)

        #Document publisher, this allows for patches to be applied
        document_publisher = tornado.ioloop.PeriodicCallback(AsyncRevisionStackManager(settings).publish,
                                                             settings['scheduler']["timeout_in_milliseconds"],
                                                             io_loop=tornado.ioloop.IOLoop.current()
        )

        document_publisher.start()

application = App()

if __name__ == "__main__":

    logger = logging.getLogger()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info("\nStopping server on port %s" % options.port)