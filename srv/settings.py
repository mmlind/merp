# coding: utf-8

def globals_init():

	global LANGS, DEFAULT_LOCALE, CURRENT_LOCALE
	global MODULE, TASK, OID

	LANGS = [
    		('en_US', 'English'),
    		('zh_CN', '中文')
			]

	DEFAULT_LOCALE = 'en_US'

	CURRENT_LOCALE = DEFAULT_LOCALE

	MODULE = ''
	TASK = ''
	OID = ''	# Object _ID (set by MongoDB)
