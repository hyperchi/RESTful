import pdb
import xmltodict

# user defined packages

from search_requests import SearchRequests


class SearchResponds(object):
    """
    This class deal with item search response

    """
    def __init__(self):
        self.class_name = "SearchRespond"
        self.search_requests = SearchRequests()

    def get_item_search_response(self, key_words="the hunger games", search_index="Books"):
        """
        :param key_words:    type string search keywords
        :param search_index: type string search category
        :return:
        dict
        """
        response = self.search_requests.get_item_search_request(key_words=key_words, search_index=search_index)
        parsed_response = xmltodict.parse(response)
        items = parsed_response["ItemSearchResponse"]["Items"]
        return items
    def get_all_item_search_response(self, key_words="the hunger games", search_index="Books", item_page="1,2,3,4,5,6,7,8,9"):
        """
        :param key_words:    type string search keywords
        :param search_index: type string search category
        :param item_page:    type string search page
        :return:
        dict
        """
        response = self.search_requests.get_all_item_search_request(key_words=key_words, search_index=search_index)
        parse_response = xmltodict.parse(response)
        items = parse_response["ItemSearchResponse"]["Items"]
        return items
