#!/usr/bin/python
"""
This is a restful test service
"""
import os
import requests
import argparse
import pdb

def test_amazon_api(port, optional1):
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

    resp = requests.get(url, data={"optional1": optional1})
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
    test_amazon_api(port=args.port, optional1=args.opt1)