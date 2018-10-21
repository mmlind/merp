# coding: utf-8

# internal modules
import settings
from language import _,get_html_tpl
from data_model import *


import bottle
import json
from collections import namedtuple

# import web
import yzauth
from yzclient import YZClient
import csv


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)



def get_products():
    """
    Returns a list of all products stored in a defined Youzan store.
    Using Youzan's 'youzan.retail.products.online.search' API
    """

    token = yzauth.Token(token='a8840c7499cc332baaa5e93767684de2')
    client = YZClient(token)

    params={}
    params['page_no']=1
    params['page_size']=100

    params['source']="OPEN_XXXX"

    files=[]

    # api = "youzan.item.search"
    # api = "youzan.items.onsale.get"
    # api = "youzan.items.inventory.get"

    response_json = client.invoke('youzan.retail.products.online.search', '3.0.0', 'POST', params=params, files=files)


    response_obj = json2obj(response_json)

    response = response_obj.response

    products=[]


    for item in response.items:

        p = Product()

        p.id    = str(item.item_id)
        p.name  = item.title.encode('utf-8')

        products.append(p)

    return products




def list_products_yz():
    """
    Returns the HTML template for listing all YOUZAN products.
    The products are loaded via Youzan's 'youzan.retail.products.online.search' API
    """

    objs = get_products()

    tpl  = bottle.template("page_header", page_title=_("Products"))
    tpl += get_html_tpl(bottle, "products_list", list_items=objs, items_count=len(objs))
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def list_products():
    """
    Returns the HTML template for an empty LOADING screen
    The menu button loads this loading page which then loads the actual prodycts_yz screen
    """

    tpl  = bottle.template("page_header", page_title=_("Products"))
    tpl += get_html_tpl(bottle, "products_list_loading")
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl
