# coding: utf-8
import settings
import re


def _(key):
	"""
	Dictionary for language translation (i18n).
	English terms are used as keys, 
	values are their respective translation. 
	"""

	if (settings.CURRENT_LOCALE=='zh_CN'):

		return {
			u'中文'						:  'English',
			'zh_CN'						:  'en_US',
			'en_US'						:  'zh_CN',
			'name_en'					:  'name_cn',
			'PO'						: u'订货',
			'SP'						: u'供应商',
			'MT'						: u'材料',
			'PD'						: u'商品',
			'Youzan'					: u'有赞',
			'Sign in'					: u'登录',
			'Username'					: u'用户名',
			'Date'						: u'日期',
			'Password'					: u'密码锁',
			'Saved successfully!'		: u'保存成功！',
			'Error! Data was not saved!': u'错误！数据没保存！',
			'Sign-out'					: u'推出',
			'ID'						: u'编号',
			'Chinese Name'				: u'中文名',
			'English Name'				: u'英文名',
			'Quantity'					: u'数量',
			'Unit'						: u'单位',
			'Units'						: u'单位',
			'Price'						: u'单价',
			'Price Unit'				: u'单价单位',
			'Quantity'					: u'数量',
			'Order Unit'				: u'数量单位',
			'Total'						: u'总价',
			'Base Unit'					: u'基本单位',
			'kg'						: u'千克',
			'piece'						: u'个',
			'liter'						: u'升',
			'Packing Unit'				: u'包装单位',
			'contains'					: u'包含',
			'Order Unit'				: u'订货单位',
			'Save'						: u'保存',
			'Materials'					: u'材料',
			'Material'					: u'材料',
			'Add Material'				: u'增加新材料',
			'Edit Material'				: u'编辑材料',
			'Material Group'			: u'材料类型',
			'Material Groups'			: u'材料类型',
			'Add Material Group'		: u'增加新材料类型',
			'Edit Material Group'		: u'编辑材料类型',
			'Purchase Order'			: u'订货单',
			'Purchase Orders'			: u'订货单',
			'New Purchase Order'		: u'增加新订货单',
			'Change Purchase Order'		: u'编辑订货单',
			'Supplier'					: u'供应商',
			'Suppliers'					: u'供应商',
			'Add Supplier'				: u'增加新供应商',
			'Edit Supplier'				: u'编辑供应商',
			'Order Contact'				: u'订货联系人',
			'Order Email'				: u'订货邮箱',
			'Order Phone'				: u'订货电话',
			'Finance Contact'			: u'财务联系人',
			'Finance Email'				: u'财务邮箱',
			'Finance Phone'				: u'财务电话',
			'Bank Name'					: u'银行',
			'Bank Account'				: u'账号',
			'Info'						: u'备注',
			'Next'						: u'下一页',
			'Create'					: u'创建',
			'Edit'						: u'编辑',
			'Products'					: u'商品',
			'Keep'						: u'保留',
			'Delete'					: u'删除',
			'Cancel'					: u'取消',
			'Confirm'					: u'确定',
			'All'						: u'所有的',
			'Sign out'					: u'推出',
			'piece'						: u'个',
			'bag'						: u'包',
			'kg'						: u'千克',
			'liter'						: u'升',
			'roll'						: u'卷',
			'one'						: u'只',
			'can'						: u'听',
			'block'						: u'块',
			'set'						: u'套',
			'sheet'						: u'张',
			'cup'						: u'杯',
			'bar'						: u'根',
			'barrel'					: u'桶',
			'slice'						: u'片',
			'bottle'					: u'瓶',
			'case'						: u'盒',
			'yard'						: u'码',
			'box'						: u'箱',
			'meter'						: u'米',
			'tin'						: u'罐',
			'sack'						: u'袋',
			'Total'						: u'总共',
			'Search'					: u'搜索',
			'Loading...'				: u'加载中...',
			'MERP'						: u'移动企业管理系统',
			'Enterprise Management System': u'企业管理系统',
			'Input order amount and price for this material, specifying the correct order and price units.': u'请输入订货量和订货价格并确认相关的数量单位和单价单位。',
			'Error! Username and/or password not found!' :u'错误：用户名或密码锁不正确！',
			'The item was successfully deleted!' : u'删除成功！',
			'Error! The item was not deleted!' : u'删除失败！',
			'ATTENTION! This item will be permanently deleted!': u'注意！此数据被删除，无法恢复！'
			}.get(key, u'Translation not found!')

	# DEFAULT language = ENGLISH (= using the keys directly)
	else:
		return key



def translate_string(str):
	"""
	Replaces all strings matching "_('..english_key..')"
	with their respective i18n translation
	using the "_" function
	"""

	str2 = str 		# create a copy that can be modified and returned

	pattern = r'_\([^)]*\)' 	# find all "_()" and replace what's inside
	regex = re.compile(pattern, re.IGNORECASE)

	for match in regex.finditer(str):

		s = str[match.start():match.end()]
		s2 = s[3:-2]
		r = _(s2)

		str2 = str2.replace(s,r)

	return str2



'''
def translate_tpl(filename):
	"""
	Returns the HTML code of a given text file as a string,
	replacing all i18n keys with their respective translation.
	"""

	html = ""

	try:
		with open(filename+'.tpl') as inputFileHandle:
			html = inputFileHandle.read()
			close(filename+'.tpl')

		html = translate_string(html)

	except IOError:
		sys.stderr.write( "Error: Could not open %s for translation!\n" % (filename) )
		sys.exit(-1)

	

	return html
'''



def get_html_tpl(bottle, filename, **kvargs):
	"""
	Returns the HTML of a given template text file as a string,
	replacing all i18n keys with their respective translation.
	Injects a variable number of variables, given as a dictionary,
	into the bottle template.
	"""

	kvargs['page_url']  = ''

	if (settings.MODULE):
		kvargs['page_url'] += settings.MODULE + '/'

		if (settings.TASK):
			kvargs['page_url'] += settings.TASK + '/'

	html = bottle.template(filename + '.tpl', kvargs)

	return translate_string(html)
