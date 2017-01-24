#!/usr/bin/python
"""
This is a restful test service
"""
import os
import requests
import argparse
import pdb

def test_amazon_api_get_all(port, optional1):
    """

    Parameters
    ----------
    port type int port to run service
    Returns
    -------
    None
    """

    # dev mode please use localhost
    url = "".join(["http://localhost:", port, "/amazon_api"])

    resp = requests.get(url, data={"key_words": "harry porter", "search_index": "Books", "item_page": "1"})
    if resp.status_code != requests.codes.ok:
        print("Request failed! ", resp.status_code)
    else:
        print("Resp: ", resp.content)
    return resp.content

def test_amazon_api_get_details(port):
    """

    Parameters
    ----------
    port type int port to run service
    Returns
    -------
    None
    """

    # dev mode please use localhost
    url = "".join(["http://localhost:", port, "/amazon_api"])

    resp = requests.get(url, data={"item_id": "9527114489", "detail": True, "item_page": "1"})
    if resp.status_code != requests.codes.ok:
        print("Request failed! ", resp.status_code)
    else:
        print("Resp: ", resp.content)
    return resp.content

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Amazon API test service")
    parser.add_argument("-p", "--port", dest="port", default="12345", help="default port")
    parser.add_argument("-o", "--optional", dest="opt1", help="option input1")
    args = parser.parse_args()
    #test_amazon_api_get_all(port=args.port, optional1=args.opt1)
    test_amazon_api_get_details(port=args.port)