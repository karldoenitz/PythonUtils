# -*-encoding:utf-8-*-

import tornado
from tornado.options import options, define
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer

define('port', default=8888, help='run on the given port', type=int)


def reload_source_config():
    print("testing ...")


def schedule(main_loop):
    reload_source_config()
    source_config_reloader = PeriodicCallback(
        reload_source_config,
        10 * 1000,
        io_loop=main_loop
    )
    source_config_reloader.start()


class HelloWorldHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        self.write("{\"data\": \"Hello World!\"}")
        self.flush()
        self.finish()


urls = [
    ("/hello-world", HelloWorldHandler)
]


def main():
    tornado.options.parse_command_line()
    application = Application(urls)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)

    main_loop = tornado.ioloop.IOLoop.instance()
    schedule(main_loop)
    main_loop.start()


if __name__ == '__main__':
    main()
