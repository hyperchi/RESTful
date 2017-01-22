import tornado.ioloop
import tornado.web
import logging.config
from tornado.httpserver import HTTPServer
import argparse
import json
import pdb
# user defined packages
from search_responds import SearchResponds

class Handler(tornado.web.RequestHandler):
    """
    rest service for web api service
    """
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', ' PUT, DELETE, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def initialize(self):
        self.logger = logging.getLogger("api_logger")
        self.search_response = SearchResponds()

    def get(self):
        """
        Returns
        -------
        """

        # get bucket name and data config file name from users
        optional1 = self.get_argument("optional1")
        print optional1
        result = self.search_response.get_all_item_search_response(key_words=optional1)
        self.finish(json.dumps(result))


def main():
    """
    Main function for rest service
    Returns
    -------
    """
    print("Loading arguments...")
    parser = argparse.ArgumentParser("sAPI parser")
    parser.add_argument("-p", "--port", dest="port", help="which port to listen to", default=12345, type=int)

    args = parser.parse_args()

    app = tornado.web.Application([(r"/amazon_api", Handler, {})])
    server = HTTPServer(app)
    server.bind(args.port)
    server.start()
    print("Now taking requests...")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    print("Starting service")
    main()