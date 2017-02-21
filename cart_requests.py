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

class CartRequests(object):
    """
    class to handle all search requests
    """
    def __init__(self, aws_key, aws_key_hash, search_page_factor=3):
        self.class_name = "CartRequests"
        self.__aws_access_key_id = aws_key
        self.__associate_tag = "hyperbolechi-20"
        self.__version = "2013-08-01"
        self.__aws_access_key_id_hash = aws_key_hash
        self.__search_page_factor = search_page_factor

    def __compose_get_cart_link(self, asin, quantity):
        """
        compose get cart link
        :param asin:
        :return:
        """
        time_stamp = urllib.quote(dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        query = "AWSAccessKeyId=" + self.__aws_access_key_id + "&AssociateTag=" + self.__associate_tag + "&Item.1.ASIN=" + str(asin) + "Item.1.Quantity=" + str(quantity) + "&Operation=CartCreate&Service=AWSECommerceService&Timestamp=" + time_stamp

        string = "\n".join(["GET", "webservices.amazon.com", "/onca/xml", query])
        new_signature = base64.b64encode(hmac.new(self.__aws_access_key_id_hash, msg=string, digestmod=hashlib.sha256).digest())
        hashed_new_signature = urllib.quote(new_signature)
        query = "".join([query, "&Signature=", hashed_new_signature])
        return "".join(["http://webservices.amazon.com/onca/xml?", query])

    def get_cart(self, asin, quantity):
        """

        :param asin:
        :param quantity:
        :return:
        """
        link = self.__compose_get_cart_link(asin=asin, quantity=quantity)
        try:
            response = requests.get(url=link)
        except response.status_code != 200:
            return
        return response.content


def main():
    with open("config.json", "rb") as file:
        data = json.load(file)
    aws_key = str(data['aws_key'])
    aws_key_hash = str(data['aws_key_hash'])

    cart = CartRequests(aws_key=aws_key, aws_key_hash=aws_key_hash)
    asin = "B000062TU1"
    quantity = 1
    result = cart.get_cart(asin=asin, quantity=quantity)
    print result

if __name__ == "__main__":
    main()