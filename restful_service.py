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
        with open("config.json") as file:
            data = json.load(file)
        aws_key = data['aws_key']
        aws_key_hash = data['aws_key_hash']
        self.search_response = SearchResponds(aws_key=aws_key, aws_key_hash=aws_key_hash)

    def get(self):
        """
        Returns
        -------
        """

        # get bucket name and data config file name from users
        get_detail = self.get_argument("detail", False)

        result = {}
        if not get_detail:
            key_words = self.get_argument("key_words")
            search_index = self.get_argument("search_index", "Book")
            item_page = self.get_argument("item_page", 1)
            print key_words
            result = self.search_response.get_all_item_search_response(key_words=key_words, search_index=search_index, item_page=item_page)
        elif get_detail:
            item_id = self.get_argument("item_id")
            result = self.search_response.get_item_details_response(item_id=item_id)
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
    parser.add_argument("-c", "--config", dest="config", help="aws key file", default="config.json", type=str)
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