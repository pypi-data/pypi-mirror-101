from cfjson.cfjson import JsonTypeRegister


def datetime_decode(dct):
	"""Decode json dict into class objects."""
	from datetime import datetime
	cls_name = dct['__json_type__']
	if cls_name == 'datetime':
		return datetime.fromisoformat(dct['datetime'])
	raise TypeError()


def datetime_encode(obj):
	"""Encode the object into a json safe dict."""
	return {
		'__json_type__': 'datetime',
		'datetime': obj.isoformat()
	}


JsonTypeRegister.register('datetime', datetime_encode, datetime_decode)
