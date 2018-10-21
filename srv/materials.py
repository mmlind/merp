# coding: utf-8

# internal modules
import settings
from language import _,get_html_tpl
import merp_mongo
from data_model import *

# external modules
import bottle
import json
from collections import namedtuple
from bson import json_util

# used by Youzan
# def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
# def json2obj(data): return json.loads(data, object_hook=_json_object_hook)





def insert_purchaseorder():
    """
    Returns the HTML template for the "Insert Purchase Order" screen
    Includes a list of all suppliers as an injected variable so that
    user can select a supplier when creating a new purchase order.
    """
    
    obj = PurchaseOrder()

    setattr(obj, 'supplier_id', '')

    page_title = _("New Purchase Order")

    suppliers = merp_mongo.get_records(Supplier)

    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "purchaseorder_insert", page_title=page_title, page_object=obj, submit_result="", suppliers=suppliers, locale=settings.CURRENT_LOCALE)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def submit_insert_purchaseorder():
    """
    Inserts a new purchase order (WITHOUT ITEMS/MATERIALS!!) into the database and
    returns the HTML template following a SUBMIT of the "Insert Purchase Order" form/screen.
    All purchase order attributes/fields must be passed as form parameters.
    """

    p = bottle.request.forms.decode()   # get all form-submitted parameters

    obj = PurchaseOrder()

    # copy all submitted attributes that exist in the object to the object
    for attr,value in obj.__dict__.iteritems():
        if attr in p.dict:
            # bottle's FormsDict is a subclass of MultiDict  
            # parameters are passed in arrays => use [0] to get the 1st element
            setattr(obj, attr, p.dict[attr][0])     

    # add the supplier matching the submitted supplier_id
    supplier = merp_mongo.get_record(Supplier, p.dict['supplier_id'][0])
    setattr(obj, 'supplier', supplier)
    setattr(obj, 'supplier_id', supplier._id)   # needed ?

    obj_id = merp_mongo.insert_record(obj)

    if (obj_id):
        submit_result = "success"
        setattr(obj, '_id', obj_id)

    else:
        submit_result = "error"

    page_title = _("New Purchase Order")

    # Load a list of all suppliers and inject them into the template.
    # In case the SUBMIT failed then user can try again and will need to (re)select a supplier.
    # If the SUBMIT succeeded, this list is actually not needed.
    suppliers = merp_mongo.get_records(Supplier) 

    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, 'purchaseorder_insert', page_title=page_title, submit_result=submit_result, page_object=obj, suppliers=suppliers, locale=settings.CURRENT_LOCALE)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl





def update_purchaseorder(oid):
    """
    Returns the HTML template of the "Update Purchase Order" screen.
    Injects a list of materials
    """
    
    obj = merp_mongo.get_record(PurchaseOrder, oid)

    if (obj._id=="" or len(obj._id) < 2):
        return "<h1>ERROR: Record not found!</h1>"

    # add the supplier matching the submitted supplier_id
    setattr(obj, 'supplier_id', obj.supplier._id)

    page_title = _("Change Purchase Order")

    materials = merp_mongo.get_records(Material)

    items = []
    counter = 0
    for m in materials:
        item = PurchaseOrderItem()
        # item.row_id = counter
        item.qty_unit   = m.order_unit  # default unit is the material's order_unit
        item.price_unit = m.order_unit  # default price_unit is same as order_unit
        setattr(item, 'material', m)
        items.append(item)
        # counter += 1


    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "purchaseorder_update", page_title=page_title, page_object=obj, submit_result="", materials=materials, items=items, locale=settings.CURRENT_LOCALE)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def submit_update_purchaseorder(oid):
    """
    Adds/updates items=materials to/in an existing purchase order.
    """

    # load existing purchaseorder which includes supplier object
    obj = merp_mongo.get_record(PurchaseOrder, oid)

    success = (oid == obj._id)

    if (success):

        p = bottle.request.forms.decode()

        # copy all submitted attributes that exist in the object to the object
        for attr,value in obj.__dict__.iteritems():

            if attr in p.dict:
                val = p.dict[attr][0]
                # if attr=='total':
                #     val = "%.2f" % float(val)   # format to 2 decimals
                # bottle's FormsDict is a subclass of MultiDict  
                # parameters are passed in arrays => use [0] to get the 1st element
                setattr(obj, attr, val)

        # add all submitted items into the po object

        # material_ids are passed as a list
        material_ids     = p.dict['material_ids']                   if ('material_ids')     in p.dict else []

        # all other fields are passed as COMMA separated strings
        item_qtys        = p.dict['item_qtys'][0].split(',')        if ('item_qtys')        in p.dict else []
        item_qty_units   = p.dict['item_qty_units'][0].split(',')   if ('item_qty_units')   in p.dict else []
        item_prices      = p.dict['item_prices'][0].split(',')      if ('item_prices')      in p.dict else []
        item_price_units = p.dict['item_price_units'][0].split(',') if ('item_price_units') in p.dict else []
        item_totals      = p.dict['item_totals'][0].split(',')      if ('item_totals')      in p.dict else []

        obj.items = []

        for i, sid in enumerate(material_ids):

            poi = PurchaseOrderItem()
            setattr(poi, 'qty'       , round(float(item_qtys[i]),2))
            setattr(poi, 'qty_unit'  , item_qty_units[i])
            setattr(poi, 'price'     , round(float(item_prices[i]),2))
            setattr(poi, 'price_unit', item_price_units[i])
            setattr(poi, 'total'     , round(float(item_totals[i]),2))
            setattr(poi, 'material'  , merp_mongo.get_record(Material, material_ids[i]))

            obj.items.append(poi)

        page_title = _("Change Purchase Order")
        success = merp_mongo.update_record(obj)


    if (success):
        submit_result = "success"
    else:
        submit_result = "error"


    materials = merp_mongo.get_records(Material)

    # count = 0
    items = []
    for m in materials:
        # count += 1
        item = PurchaseOrderItem()
        # item.row_id     = count
        item.qty_unit   = m.order_unit
        item.price_unit = m.order_unit
        setattr(item, 'material', m)
        items.append(item)

    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, 'purchaseorder_update', page_title=page_title, submit_result=submit_result, page_object=obj, materials=materials, items=items, locale=settings.CURRENT_LOCALE)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl





def delete_purchaseorder(oid):
    """
    Removes a purchase order, referenced by its "_id", from the database
    and returns an HTML template specyfying whether the delete was successful or not. 
    """
    
    success = merp_mongo.delete_record(PurchaseOrder, oid)

    if success:
        page_title = _("The item was successfully deleted!")
        delete_result  = "success"
    else:
        page_title = _("Error! The item was not deleted!")
        delete_result  = "error"


    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "purchaseorder_delete", delete_result=delete_result)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def list_purchaseorders():
    """
    Loads all purchase orders from the database and
    returns an HTML template for listing them.
    """

    objs = merp_mongo.get_records(PurchaseOrder)

    tpl  = get_html_tpl(bottle, "page_header", page_title=_("Purchase Orders"))
    tpl += get_html_tpl(bottle, "purchaseorders_list", list_items=objs, items_count=len(objs), locale=settings.CURRENT_LOCALE)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def upsert_supplier(oid):
    """
    Returns the HTML template for the "Insert or update supplier" screen.
    """
    
    obj = merp_mongo.get_record(Supplier, oid)

    if (obj._id==""):
        page_title = _("Add Supplier")
        page_mode  = "insert"
    else:
        page_title = _("Edit Supplier")
        page_mode  = "update"


    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "supplier_upsert", page_title=page_title, page_mode=page_mode, page_object=obj, submit_result="")
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def submit_upsert_supplier():
    """
    Updates or inserts a supplier object in/into the database.
    Existing records are referenced by their _ID. 
    All object fields are taken from the form-submitted parameters.
    Whenever the form-submitted field matches the object's attribute name
    the respective submitted value is updated. 
    For all other fields a default is set based on an INIT_DICT defined in the CLASS.
    """

    p = bottle.request.params.decode()

    obj = Supplier(p)   # Construct a supplier object based on the form-submitted fields

    if (obj._id==""):
        page_title = _("Add Supplier")
        page_mode  = "insert"
        success = merp_mongo.insert_record(obj)
    else:
        page_title = _("Edit Supplier")
        page_mode  = "update"
        success = merp_mongo.update_record(obj)

    if (success):
        submit_result = "success"
    else:
        submit_result = "error"


    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "supplier_upsert", page_title=page_title, page_mode=page_mode, submit_result=submit_result, page_object=obj)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def delete_supplier(oid):
    """
    Removes a supplier object, referenced by its _ID, from the database
    and returns the respective success/error HTML template.
    """
    
    success = merp_mongo.delete_record(Supplier, oid)


    if success:
        page_title = _("The item was successfully deleted!")
        delete_result  = "success"
    else:
        page_title = _("Error! The item was not deleted!")
        delete_result  = "error"


    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "supplier_delete", delete_result=delete_result)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def list_suppliers():
    """
    Returns the HTML template for listing all suppliers.
    """

    objs = merp_mongo.get_records(Supplier)

    tpl  = get_html_tpl(bottle, "page_header", page_title=_("Suppliers"))
    tpl += get_html_tpl(bottle, "suppliers_list", list_items=objs, items_count=len(objs))
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl





def upsert_materialgroup(oid):
    """
    Returns the HTML template for updating or inserting a new material group.
    """
    
    mg = merp_mongo.get_record(Materialgroup, oid)

    if (mg._id==""):
        page_title = _("Add Material Group")
        page_mode  = "insert"
    else:
        page_title = _("Edit Material Group")
        page_mode  = "update"


    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "materialgroup_upsert", page_title=page_title, page_mode=page_mode, page_object=mg, submit_result="")
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def submit_upsert_materialgroup():
    """
    Updates or inserts a material group in the database.
    All object fields and values are passed via form submit parameters. 
    """

    p = bottle.request.params.decode()
    mg = Materialgroup(p)       # Construct new object based on form-submitted fields and values

    if (mg._id==""):
        page_title = _("Add Material Group")
        page_mode  = "insert"
        success = merp_mongo.insert_record(mg)
    else:
        page_title = _("Edit Material Group")
        page_mode  = "update"
        success = merp_mongo.update_record(mg)

    if (success):
        submit_result = "success"
    else:
        submit_result = "error"


    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "materialgroup_upsert", page_title=page_title, page_mode=page_mode, submit_result=submit_result, page_object=mg)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def delete_materialgroup(oid):
    """
    Removes a material group, referenced by its _ID, from the database.
    """

    success = merp_mongo.delete_record(Materialgroup, oid)


    if success:
        page_title = _("The item was successfully deleted!")
        delete_result  = "success"
    else:
        page_title = _("Error! The item was not deleted!")
        delete_result  = "error"


    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "materialgroup_delete", delete_result=delete_result)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def list_materialgroups():
    """
    Returns the HTML template for listing all material groups.
    """

    mgs = merp_mongo.get_records(Materialgroup)

    tpl  = get_html_tpl(bottle, "page_header", page_title=_("Material Groups"))
    tpl += get_html_tpl(bottle, "materialgroups_list", list_items=mgs, items_count=len(mgs))
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl






def upsert_material(oid):
    """
    Returns the HTML template for inserting or updating a material object.
    If an material _ID is passed, its existing values are loaded and returned.
    """
    
    m = merp_mongo.get_record(Material, oid)

    if (m._id==""):
        page_title = _("Add Material")
        page_mode  = "insert"
    else:
        page_title = _("Edit Material")
        page_mode  = "update"

    units = merp_mongo.get_units()
    mgs = merp_mongo.get_records(Materialgroup)

    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "material_upsert", page_title=page_title, page_mode=page_mode, page_object=m, submit_result="", units=units, mgs=mgs, locale=settings.CURRENT_LOCALE)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def submit_upsert_material():
    """
    Inserts or updates as material in the database.
    Object fields and values are passed via form submit.
    """

    p = bottle.request.params.decode()

    m = Material(p)     # Constructs a new material based on the form-submitted fields and values

    if (m._id==""):
        page_title = _("Add Material")
        page_mode  = "insert"
        success = merp_mongo.insert_record(m)
    else:
        page_title = _("Edit Material")
        page_mode  = "update"
        success = merp_mongo.update_record(m)

    if (success):
        submit_result = "success"
    else:
        submit_result = "error"


    units = merp_mongo.get_units()
    mgs = merp_mongo.get_records(Materialgroup)

    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "material_upsert", page_title=page_title, page_mode=page_mode, submit_result=submit_result, page_object=m, units=units, mgs=mgs, locale=settings.CURRENT_LOCALE)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def delete_material(oid):
    """
    Removes an exiting material, referenced by its _ID, from the database
    and returns the respective success/error HTML template.
    """

    success = merp_mongo.delete_record(Material, oid)


    if success:
        page_title = _("The item was successfully deleted!")
        delete_result  = "success"
    else:
        page_title = _("Error! The item was not deleted!")
        delete_result  = "error"


    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "material_delete", delete_result=delete_result)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl




def list_materials():
    """
    Returns the HTML template for listing all materials, 
    including their respective materialgroups
    """

    ms = merp_mongo.get_records(Material)

    mgs = merp_mongo.get_records(Materialgroup)

    # material lists for display on the screen
    # mls = []
    # for mg in mgs:

    #     ml = {}
    #     ml['_id']       = mg._id
    #     ml['name_cn']   = mg.name_cn
    #     ml['name_en']   = mg.name_en
    #     ml['m_count']   = 0
    #     ml['materials'] = []

    #     for m in ms:
    #         if (m.mg_id == mg._id):
    #             ml['materials'].append(m)
    #             ml['m_count'] += 1

    #     mls.append(ml)

    tpl  = get_html_tpl(bottle, "page_header", page_title=_("Materials"))
    tpl += get_html_tpl(bottle, "materials_list", list_items=ms, items_count=len(ms), mgs=mgs, locale=settings.CURRENT_LOCALE)
    # tpl += get_html_tpl(bottle, "materials_list", mls=mls, locale=settings.CURRENT_LOCALE)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl





def homepage(username):
    """
    Returns the HTML template for the homepage.
    """

    page_title = _('MERP')

    tpl  = get_html_tpl(bottle, "page_header", page_title=page_title)
    tpl += get_html_tpl(bottle, "home", username=username)
    tpl += get_html_tpl(bottle, "page_footer")

    return tpl





