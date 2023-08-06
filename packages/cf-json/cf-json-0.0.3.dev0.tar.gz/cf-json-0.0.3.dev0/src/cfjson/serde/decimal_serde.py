from cfjson.cfjson import JsonTypeRegister


def decimal_decode(dct):
	"""Decode json dict into class objects."""
	from decimal import Decimal
	cls_name = dct['__json_type__']
	if cls_name == 'Decimal':
		return Decimal(dct['decimal'])
	raise TypeError()


def decimal_encode(obj):
	"""Encode the object into a json safe dict."""
	return {
		'__json_type__': 'Decimal',
		'decimal': str(obj)
	}


JsonTypeRegister.register('Decimal', decimal_encode, decimal_decode)


def decimal_test():

	from decimal import Decimal
	d = Decimal('1.23')
	from kson import dumps
	j = dumps({'blah': d})
	print(j)
	from kson import loads
	e = loads(j)
	print(e)


if __name__ == '__main__':
	decimal_test()
