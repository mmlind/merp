# coding: utf-8
"""
Mobile ERP
Mini ERP system (mainly purchasing) targeting mobile devices
"""

import os 
import settings
settings.globals_init()

import materials
import products

from auth import *
import bottle


# app = bottle.Bottle()

srv_path = os.path.dirname(os.path.realpath(__file__))


# Static Routes
@bottle.get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return bottle.static_file(filepath, root=srv_path+"/../static/css")

@bottle.get("/static/webfonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def webfonts(filepath):
    return bottle.static_file(filepath, root=srv_path+"/../static/webfonts")

@bottle.get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return bottle.static_file(filepath, root=srv_path+"/../static/img")

@bottle.get("/static/js/<filepath:re:.*\.js>")
def js(filepath):
    return bottle.static_file(filepath, root=srv_path+"/../static/js")





@bottle.error(404)
def error404(error):
    return "Page not found!"


@bottle.route('/')
def url_index():
	bottle.redirect('/'+settings.DEFAULT_LOCALE+'/')


@bottle.route('/en_US/')
def url_home_en():
	settings.CURRENT_LOCALE = 'en_US'
	settings.MODULE = ''
	settings.TASK   = ''
	settings.OID    = ''
	session = bottle.request.environ.get('beaker.session')
	aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
	return materials.homepage(aaa.current_user.username)


@bottle.route('/zh_CN/')
def url_home_cn():
	settings.CURRENT_LOCALE = 'zh_CN'
	settings.MODULE = ''
	settings.TASK   = ''
	settings.OID    = ''
	session = bottle.request.environ.get('beaker.session')
	aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
	return materials.homepage(aaa.current_user.username)


@bottle.route('/<locale>/purchaseorders/')
def url_module(locale=settings.DEFAULT_LOCALE):
	aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
	settings.CURRENT_LOCALE = locale
	settings.MODULE = 'purchaseorders'
	settings.TASK   = ''
	settings.OID    = ''
	return materials.list_purchaseorders()


@bottle.route('/<locale>/suppliers/')
def url_module(locale=settings.DEFAULT_LOCALE):
	aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
	settings.CURRENT_LOCALE = locale
	settings.MODULE = 'suppliers'
	settings.TASK   = ''
	settings.OID    = ''
	return materials.list_suppliers()


@bottle.route('/<locale>/materialgroups/')
def url_module(locale=settings.DEFAULT_LOCALE):
	aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
	settings.CURRENT_LOCALE = locale
	settings.MODULE = 'materialgroups'
	settings.TASK   = ''
	settings.OID    = ''
	return materials.list_materialgroups()


@bottle.route('/<locale>/materials/')
def url_module(locale=settings.DEFAULT_LOCALE):
	aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
	settings.CURRENT_LOCALE = locale
	settings.MODULE = 'materials'
	settings.TASK   = ''
	settings.OID    = ''
	return materials.list_materials()

@bottle.route('/<locale>/products/')
def url_module(locale=settings.DEFAULT_LOCALE):
	aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
	settings.CURRENT_LOCALE = locale
	settings.MODULE = 'products'
	settings.TASK   = ''
	settings.OID    = ''
	return products.list_products()

@bottle.route('/<locale>/products_yz/')
def url_module(locale=settings.DEFAULT_LOCALE):
	aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
	settings.CURRENT_LOCALE = locale
	settings.MODULE = 'products'
	settings.TASK   = ''
	settings.OID    = ''
	return products.list_products_yz()



@bottle.route('/<locale>/<module>/<task>/<oid>')
@bottle.route('/<locale>/<module>/<task>/<oid>', method='POST')
def url_module_task_oid(locale=settings.DEFAULT_LOCALE, module='',task='', oid='', method=''):
	aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')

	settings.CURRENT_LOCALE = locale
	settings.MODULE = module
	settings.TASK   = task
	settings.OID    = oid


	if module=='materialgroups':

		if task=='upsert':

			if (bottle.request.POST):
				return materials.submit_upsert_materialgroup()
			else:
				return materials.upsert_materialgroup(oid)

		elif task=='delete':

			return materials.delete_materialgroup(oid)


	elif module=='materials':

		if task=='upsert':

			if (bottle.request.POST):
				return materials.submit_upsert_material()
			else:
				return materials.upsert_material(oid)

		elif task=='delete':

			return materials.delete_material(oid)


	elif module=='suppliers':

		if task=='upsert':

			if (bottle.request.POST):
				return materials.submit_upsert_supplier()
			else:
				return materials.upsert_supplier(oid)

		elif task=='delete':

			return materials.delete_supplier(oid)


	elif module=='purchaseorders':

		if task=='insert':

			if (bottle.request.POST):
				return materials.submit_insert_purchaseorder()
			else:
				return materials.insert_purchaseorder()

		elif task=='update':

			if (bottle.request.POST):
				return materials.submit_update_purchaseorder(oid)
			else:
				return materials.update_purchaseorder(oid)

		elif task=='delete':

			return materials.delete_purchaseorder(oid)


	else:
		return "ERROR: Unknown module!"





if __name__ == "__main__":

	srv_path = os.path.dirname(os.path.realpath(__file__))
	views_path = srv_path + "/../views"

	bottle.TEMPLATE_PATH.insert(0, views_path)

	bottle.debug(True)
	bottle.run(app=app, quiet=False, reloader=True, host='0.0.0.0', port=8080)
	# bottle.run(app, host='0.0.0.0', port=8080)
