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
        :return:
        processed response
        """
        response = self.search_requests.get_item_search_request(key_words=key_words, search_index=search_index)
        parsed_response = xmltodict.parse(response)
        items = parsed_response["ItemSearchResponse"]["Items"]
        return items

