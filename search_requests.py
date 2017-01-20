import requests
import datetime as dt
import urllib
import hmac
import hashlib
import base64
import pdb


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

    def compose_item_search_link(self, key_words="the hunger games", search_index="Books"):
        """
        compose search link
        """
        hashed_key_word = urllib.quote(key_words)
        time_stamp = urllib.quote(dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        query = "AWSAccessKeyId=" + self.aws_access_key_id \
                + "&AssociateTag=" + self.associate_tag\
                + "&Keywords="+ hashed_key_word \
                + "&Operation=ItemSearch&SearchIndex=" + search_index \
                + "&Service=AWSECommerceService&Timestamp="+ time_stamp
        string = "\n".join(["GET", "webservices.amazon.com", "/onca/xml", query])
        new_signature = base64.b64encode(hmac.new(self.aws_access_key_id_hash, msg=string, digestmod=hashlib.sha256).digest())
        hashed_new_signature = urllib.quote(new_signature)
        query = "".join([query, "&Signature=", hashed_new_signature])
        return "".join(["http://webservices.amazon.com/onca/xml?", query])

    def compose_all_item_search_link(self,
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

    def get_item_search_request(self, key_words="the hunger games", search_index="Books"):
        """
        Search item based on input
        """
        item_search_request_link = self.compose_item_search_link(key_words=key_words, search_index=search_index)
        response = requests.get(url=item_search_request_link)
        return response.content

    def get_all_item_search_request(self, key_words="the hunger games", search_index="Books", item_page="1,2,3,4,5,6,7,8,9"):
        all_item_search_request_link = self.compose_all_item_search_link(key_words=key_words, search_index=search_index, item_page=item_page)
        response = requests.get(url=all_item_search_request_link)
        return response.content


def main():
    search_request = SearchRequests()
    res = search_request.get_all_item_search_request()

    print res

if __name__== "__main__":
    main()