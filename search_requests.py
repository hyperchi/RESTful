import requests
import datetime as dt
import urllib
import hmac
import hashlib
import base64
import pdb
import xmltodict
import json
import datetime as dt

class SearchRequests(object):
    """
    class to handle all search requests
    """
    def __init__(self, aws_key, aws_key_hash, search_page_factor=3):
        self.class_name = "SearchRequests"
        self.__aws_access_key_id = aws_key
        self.__associate_tag = "hyperbolechi-20"
        self.__version = "2013-08-01"
        self.__aws_access_key_id_hash = aws_key_hash
        self.__search_page_factor = search_page_factor

    def __compose_all_item_search_link(self,
                                       key_words="the hunger games",
                                       search_index="Books",
                                       item_page="1"):

        """

        :param key_words:    type string search key words
        :param search_index: type string search index in the api
        :param item_page:    type string
        :return:
        """
        key_words = urllib.quote(key_words)
        item_page = urllib.quote(item_page)
        time_stamp = urllib.quote(dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        query = "AWSAccessKeyId="+ self.__aws_access_key_id\
                +"&AssociateTag="+ self.__associate_tag\
                +"&ItemPage="+ item_page\
                +"&Keywords="+ key_words\
                +"&Operation=ItemSearch&SearchIndex="+search_index\
                +"&Service=AWSECommerceService&Timestamp=" + time_stamp

        string = "\n".join(["GET", "webservices.amazon.com", "/onca/xml", query])
        new_signature = base64.b64encode(hmac.new(self.__aws_access_key_id_hash, msg=string, digestmod=hashlib.sha256).digest())
        hashed_new_signature = urllib.quote(new_signature)
        query = "".join([query, "&Signature=", hashed_new_signature])
        return "".join(["http://webservices.amazon.com/onca/xml?", query])

    def __compose_search_image_link(self, item_id):
        time_stamp = urllib.quote(dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        query = "AWSAccessKeyId="+ self.__aws_access_key_id\
                +"&AssociateTag="+ self.__associate_tag\
                +"&IdType=ASIN&ItemId="+ item_id\
                +"&Operation=ItemLookup&ResponseGroup=Images&Service=AWSECommerceService&Timestamp="+ time_stamp
        string = "\n".join(["GET", "webservices.amazon.com", "/onca/xml", query])
        new_signature = base64.b64encode(hmac.new(self.__aws_access_key_id_hash, msg=string, digestmod=hashlib.sha256).digest())
        hashed_new_signature = urllib.quote(new_signature)
        query = "".join([query, "&Signature=", hashed_new_signature])
        return "".join(["http://webservices.amazon.com/onca/xml?", query])

    def __compose_search_price_link(self, item_id):
        time_stamp = urllib.quote(dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        query = "AWSAccessKeyId="+self.__aws_access_key_id\
                +"&AssociateTag="+ self.__associate_tag\
                +"&IdType=ASIN&ItemId="+ item_id\
                +"&Operation=ItemLookup&ResponseGroup=Offers&Service=AWSECommerceService&Timestamp="+ time_stamp

        string = "\n".join(["GET", "webservices.amazon.com", "/onca/xml", query])
        new_signature = base64.b64encode(hmac.new(self.__aws_access_key_id_hash, msg=string, digestmod=hashlib.sha256).digest())
        hashed_new_signature = urllib.quote(new_signature)
        query = "".join([query, "&Signature=", hashed_new_signature])
        return "".join(["http://webservices.amazon.com/onca/xml?", query])

    def __compose_search_review_link(self, item_id):
        time_stamp = urllib.quote(dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        query = "AWSAccessKeyId="+self.__aws_access_key_id\
                +"&AssociateTag="+ self.__associate_tag\
                +"&IdType=ASIN&ItemId="+ item_id\
                +"&Operation=ItemLookup&ResponseGroup=Review&Service=AWSECommerceService&Timestamp="+ time_stamp
        string = "\n".join(["GET", "webservices.amazon.com", "/onca/xml", query])
        new_signature = base64.b64encode(hmac.new(self.__aws_access_key_id_hash, msg=string, digestmod=hashlib.sha256).digest())
        hashed_new_signature = urllib.quote(new_signature)
        query = "".join([query, "&Signature=", hashed_new_signature])
        return "".join(["http://webservices.amazon.com/onca/xml?", query])

    def __compose_search_similar_item_link(self, item_id):
        time_stamp = urllib.quote(dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        query = "AWSAccessKeyId="+self.__aws_access_key_id\
                +"&AssociateTag="+ self.__associate_tag\
                +"&IdType=ASIN&ItemId="+ item_id\
                +"&Operation=ItemLookup&ResponseGroup=Similarities&Service=AWSECommerceService&Timestamp="+ time_stamp
        string = "\n".join(["GET", "webservices.amazon.com", "/onca/xml", query])
        new_signature = base64.b64encode(hmac.new(self.__aws_access_key_id_hash, msg=string, digestmod=hashlib.sha256).digest())
        hashed_new_signature = urllib.quote(new_signature)
        query = "".join([query, "&Signature=", hashed_new_signature])
        return "".join(["http://webservices.amazon.com/onca/xml?", query])

    def get_search_image_request(self, item_id):
        link = self.__compose_search_image_link(item_id=item_id)
        try:
            response = requests.get(url=link)
        except response.status_code != 200:
            return
        return response.content

    def get_search_price_request(self, item_id):
        link = self.__compose_search_price_link(item_id=item_id)
        try:
            response = requests.get(url=link)
        except response.status_code != 200:
            return
        return response.content

    def get_search_review_request(self, item_id):
        link = self.__compose_search_price_link(item_id=item_id)
        try:
            response = requests.get(url=link)
        except response.status_code != 200:
            return
        return response.content

    def get_search_similar_item_request(self, item_id):
        link = self.__compose_search_similar_item_link(item_id=item_id)
        try:
            response = requests.get(url=link)
        except response.status_code != 200:
            return
        content = xmltodict.parse(response.content)
        item = content.get('ItemLookupResponse', {}).get('Items', {}).get('Item', {})
        item_ids = []
        item_images = []
        if "ASIN" in item:
            item_ids.append(item["ASIN"])
        if item_ids:
            for id in item_ids:
                item_images.append(self.get_search_image_request(item_id=id))
        return item_images


    def get_all_item_search_request(self, key_words="the hunger games", search_index="Books", item_page="1"):
        """
        Do not know how to use search index yet
        :param key_words:    type string item search name
        :param search_index: type string item category
        :param item_page:    type string the page of item we want to display
        :return:
        """
        start_page = int(item_page)
        items = None
        for page in xrange((start_page - 1) * self.__search_page_factor, start_page * self.__search_page_factor):
            all_item_search_request_link = self.__compose_all_item_search_link(key_words=key_words,
                                                                               search_index=search_index,
                                                                               item_page=str(page + 1))
            #print  all_item_search_request_link
            print(dt.datetime.now())
            response = requests.get(url=all_item_search_request_link)
            print(dt.datetime.now())
            parse_response = xmltodict.parse(response.content)
            #pdb.set_trace()
            partial_items = parse_response.get("ItemSearchResponse", {}).get("Items", {})
            if not items:
                items = partial_items
            else:
                other_page_item = partial_items.get("ItemSearchResponse", {}).get("Items", {})
                if other_page_item:
                    items['Item'].extend(other_page_item)

        if items:
            for index, item in enumerate(items["Item"]):

                ASIN = item["ASIN"]

                # add image to the search response
                image_response = self.get_search_image_request(item_id=ASIN)
                parsed_image_response = xmltodict.parse(image_response)
                image = parsed_image_response.get('ItemLookupResponse', {}).get('Items', {}).get('Item', {})
                items["Item"][index].setdefault("Image", image)

                # add price to search response
                price_response = self.get_search_price_request(item_id=ASIN)
                parsed_price_response = xmltodict.parse(price_response)
                price = parsed_price_response.get("ItemLookupResponse", {}).get("Items", {}).get("Item", {})
                items["Item"][index].setdefault("Price", price)
        return items

    def get_item_details_request(self, item_id):
        """
        if we know a specific item id we will give detailed item search results
        :param item_id: type string item id
        :return: dict
        """
        image = self.get_search_image_request(item_id=item_id)
        price = self.get_search_image_request(item_id=item_id)
        reviews = self.get_search_review_request(item_id=item_id)
        similar_items = self.get_search_similar_item_request(item_id=item_id)
        response = {"Image": image, "Price": price, "Reviews": reviews, "SimilarItem": similar_items}
        return response

def main():
    with open("config.json") as file:
        data = json.load(file)
    search_request = SearchRequests(aws_key=str(data['aws_key']), aws_key_hash=str(data['aws_key_hash']))
    #print(dt.datetime.now())
    res = search_request.get_all_item_search_request(key_words="harry porter")
    #print(dt.datetime.now())
    #print res

if __name__== "__main__":
    main()

