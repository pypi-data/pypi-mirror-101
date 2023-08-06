from cfjson.cfjson import JsonTypeRegister


def path_decode(dct):
	"""Decode json dict into class objects."""
	from pathlib import Path
	cls_name = dct['__json_type__']
	if cls_name in ('Path', 'WindowsPath'):
		return Path(dct['path'])
	raise TypeError()


def path_encode(obj):
	"""Encode the object into a json safe dict."""
	return {
		'__json_type__': type(obj).__name__,
		'path': str(obj)
	}


JsonTypeRegister.register('Path', path_encode, path_decode)
JsonTypeRegister.register('WindowsPath', path_encode, path_decode)
