import json
from kson.kson import MyEncoder, MyDecoder

# Make sure all the serde get called and registered.
from .serde import *


JSONDecodeError = json.JSONDecodeError

__all__ = ('dump', 'dumps', 'load', 'loads', 'JSONDecodeError')


def dump(*args, **kwargs):

	kwargs['cls'] = MyEncoder
	return json.dump(*args, **kwargs)


def dumps(*args, **kwargs):
	kwargs['cls'] = MyEncoder
	return json.dumps(*args, **kwargs)


def load(*args, **kwargs):
	kwargs['cls'] = MyDecoder
	return json.load(*args, **kwargs)


def loads(*args, **kwargs):
	kwargs['cls'] = MyDecoder
	return json.loads(*args, **kwargs)
