# coding: utf-8

import datetime


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())

def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


DB_COLLECTIONS = {'PurchaseOrder'  :'purchaseorders',
                  'Supplier'       :'suppliers',
                  'Material'       :'materials',
                  'Materialgroup'  :'materialgroups'}



# MODULES                            => STATUS               CAN CHANGE     WORKFLOW
# input purchaseOrder           订货  => INPUT                YES            send email to approver
# approve/place purchaseOrder   下单  => PLACED               now            send email to requester+supplier
#                                       add ordered amounts to masterdata field: PENDING_ORDER_QTY (by 3 unit types!)
#                                       REJECTED
# receive goods                 收货  => RECEIVING/RECEIVED?  NO             
#                   purchaseDelivery =>  subtract received amounts from masterdata field: PENDING_ORDER_QTY
#                                        
#                                        if receive less than ordered: offer a checkbox "check as fully delivered"

# REQUIRED MODULES
# 
# status {INPUT, SUBMITTED, PLACED, REJECTED}
#
# list purchaseOrders
# list columns: date, supplier, amount
# multiple, additive filters: by status {INPUT,PLACED,REJECTED}, by time {THIS MONTH, LAST MONTH} 
# in list: if PO is [INPUT,REJECTED]: click opens upsert
#          if PO is [SUBMITTED, PLACED]: click opens view

# how to store prices and pending order quantities
# OPTION 1: by supplier [Supplier123, {m1, 45 RMB, kg}, {m2, 123 RMB, box}]
# price for the same material can be stored using multiple/different units

# make the input of a new purchaseOrder a 2-step process:
# step 1: select supplier => which then loads prices
# step 2: select products, qtys and prices


# insert purchaseOrder
# select supplier
# [NEXT] or [SELECT PRODUCTS] button then saves order and launches PO EDIT


# update purchaseOrder
# if status {PLACED;SUBMITTED}: cannot edit
# pass all supplier prices to client
# change supplier not possible
# after save: set status to [INPUT]
# during save: if insert: add qtys to materials' pending_order_qty
#              if update: first subtract (before change qty), then add (after change qty) to pending_order_qtys
# if permission: show SAVE/SUBMIT button
# edit item popup:
#      show (mutiple) available prices set for this material

# view/approve po
# view only
# if permission: show APPROVE/REJECT buttons => confirm in popup => update status => send email


# list purchaseDeliveries
# list columns: date, supplier, amount
# multiple, additive filters: by status {INPUT,PLACED,REJECTED}, by time {THIS MONTH, LAST MONTH} 

# upsert purchaseDelivery
# in add-mode: show pending_order_qty per item
# can only be viewed, not edited
# when save: subtract from pending_order_qtys



class Product(object):          
    """
    Simplified product mapping of a YOUZAN product
    """

    def __init__(self, cursor={'id':'', 'name':''}):
        self.id             = cursor[u'id']
        self.name           = cursor[u'name']




class Materialgroup(object):
    """
    Category string, in English and Chinese, to classify materials.
    """

    init_dict = {
                 '_id'                 : '', 
                 'id'                  : '', 
                 'name_cn'             : '', 
                 'name_en'             : '' 
                }

    def __init__(self, d=init_dict):
        for k,v in d.iteritems():
            setattr(self, k, v)




class Material(object):
    """
    Material with 3 types of units and conversion factors to base_unit.
    """

    init_dict = {
                 '_id'                 : '' , 
                 'id'                  : '' , 
                 'name_cn'             : '' , 
                 'name_en'             : '' , 
                 'mg_id'               : '' , 
                 'base_unit'           : '' , 
                 'pack_unit'           : '' , 
                 'pack_unit_qty'       : '0', 
                 'order_unit'          : '' , 
                 'order_unit_qty'      : '0'
                }

    def __init__(self, d=init_dict):
        for k,v in d.iteritems():
            setattr(self, k, v)




class Supplier(object):
    """
    Supplier record with general purchase-related information
    """

    init_dict = {
                 '_id'                 : '', 
                 'id'                  : '', 
                 'name_cn'             : '', 
                 'name_en'             : '', 
                 'order_contact'       : '', 
                 'order_email'         : '',
                 'order_phone'         : '', 
                 'finance_contact'     : '', 
                 'finance_email'       : '', 
                 'finance_phone'       : '', 
                 'bank_name'           : '', 
                 'bank_account'        : '', 
                 'info'                : ''
                }

    def __init__(self, d=init_dict):

        for k,v in d.iteritems():
            setattr(self, k, v)



"""
class PurchasePrice(object):

    init_dict = {
                 '_id'         : '' , 
                 'supplier_id' : '' , 
                 'material_id' : '' , 
                 'unit'        : '' , 
                 'price'       : '0'
                }


    def __init__(self, d=init_dict):

        for k,v in d.iteritems():
            setattr(self, k, v)
"""


class PurchaseOrderItem(object):
    """
    A material added to a purchase order.
    It includes the underlying MATERIAL object plus order-related info.
    """

    init_dict = {
                 'qty'          : '0', 
                 'qty_unit'     : '' , 
                 'price'        : '0', 
                 'price_unit'   : '' , 
                 'total'        : '0',
                 'material'     : Material.init_dict
                }

    def __init__(self, d=init_dict):

        for k,v in d.iteritems():
            if (k == 'material'):
                v = Material(v)

            setattr(self, k, v)



class PurchaseOrder(object):
    """
    PurchaseOrder including a list of purchase order items.
    """

    init_dict = {
                 '_id'          : '' , 
                 'datetime'     : datetime.datetime.now().strftime('%Y-%m-%d %H:%M') , 
                 'status'       : 'INPUT' , 
                 'supplier'     : Supplier.init_dict, 
                 'items'        : [] , 
                 'total'        : '0'
                }


    def __init__(self, d=init_dict):

        for k,v in d.items():

            if (k == 'supplier'):
                v = Supplier(v)

            if (k == 'items'):
                items = []
                for i in v:
                    item = PurchaseOrderItem(i)
                    items.append(item)
                v = items

            setattr(self, k, v)

