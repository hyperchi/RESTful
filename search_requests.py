import requests
import datetime as dt
import urllib
import hmac
import hashlib
import base64
import pdb
import xmltodict

class SearchRequests(object):
    """
    class to handle all search requests
    """
    def __init__(self):
        self.class_name = "SearchRequests"
        self.aws_access_key_id = "AKIAJYIMWZ42Y4PHDTJQ"
        self.associate_tag = "hyperbolechi-20"
        self.version = "2013-08-01"
        self.aws_access_key_id_hash = "pGCKw2XnmuQH0Vj5i4LBiC0oSoX5b7uV3lLmT6Dj"

    def __compose_all_item_search_link(self,
                                     key_words="the hunger games",
                                     search_index="Books",
                                     item_page="1,2,3,4,5,6,7,8,9"):
        key_words = urllib.quote(key_words)
        item_page = urllib.quote(item_page)
        time_stamp = urllib.quote(dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        query = "AWSAccessKeyId="+ self.aws_access_key_id\
                +"&AssociateTag="+ self.associate_tag\
                +"&ItemPage="+ item_page\
                +"&Keywords="+ key_words\
                +"&Operation=ItemSearch&SearchIndex="+search_index\
                +"&Service=AWSECommerceService&Timestamp=" + time_stamp

        string = "\n".join(["GET", "webservices.amazon.com", "/onca/xml", query])
        new_signature = base64.b64encode(hmac.new(self.aws_access_key_id_hash, msg=string, digestmod=hashlib.sha256).digest())
        hashed_new_signature = urllib.quote(new_signature)
        query = "".join([query, "&Signature=", hashed_new_signature])
        return "".join(["http://webservices.amazon.com/onca/xml?", query])

    def __compose_search_image_link(self, item_id):
        time_stamp = urllib.quote(dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        query = "AWSAccessKeyId="+ self.aws_access_key_id\
                +"&AssociateTag="+ self.associate_tag\
                +"&IdType=ASIN&ItemId="+ item_id\
                +"&Operation=ItemLookup&ResponseGroup=Images&Service=AWSECommerceService&Timestamp="+ time_stamp
        string = "\n".join(["GET", "webservices.amazon.com", "/onca/xml", query])
        new_signature = base64.b64encode(hmac.new(self.aws_access_key_id_hash, msg=string, digestmod=hashlib.sha256).digest())
        hashed_new_signature = urllib.quote(new_signature)
        query = "".join([query, "&Signature=", hashed_new_signature])
        return "".join(["http://webservices.amazon.com/onca/xml?", query])


    def get_search_image_request(self, item_id):
        link = self.__compose_search_image_link(item_id=item_id)
        response = requests.get(url=link)
        return response.content

    def get_all_item_search_request(self, key_words="the hunger games", search_index="Books", item_page="1,2,3,4,5,6,7,8,9"):
        all_item_search_request_link = self.__compose_all_item_search_link(key_words=key_words, search_index=search_index, item_page=item_page)
        print  all_item_search_request_link
        response = requests.get(url=all_item_search_request_link)

        parse_response = xmltodict.parse(response.content)
        items = parse_response["ItemSearchResponse"]["Items"]
        for index, item in enumerate(items["Item"]):
            ASIN = item["ASIN"]
            image_response = self.get_search_image_request(item_id=ASIN)
            parsed_image_response = xmltodict.parse(image_response)
            image = parsed_image_response['ItemLookupResponse']['Items']['Item']
            items["Item"][index].setdefault("Image", image)
        return items


def main():
    search_request = SearchRequests()
    res = search_request.get_all_item_search_request()

    print res

if __name__== "__main__":
    main()
