import json

JSONEncoder = json.JSONEncoder
JSONDecoder = json.JSONDecoder


class MyEncoder(JSONEncoder):

	def default(self, o):
		if hasattr(o, '__json_encode__'):
			return o.__json_encode__()
		try:
			return JsonTypeRegister.encode(type(o).__name__, o)
		except KeyError:
			pass
		return super(MyEncoder, self).default(o)


class MyDecoder(JSONDecoder):

	def __init__(self, *args, **kwargs):
		super(MyDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

	def object_hook(self, dct):
		if '__json_type__' in dct:
			return JsonTypeRegister.decode(dct['__json_type__'], dct)
		return dct


class JsonTypeRegister(object):

	encoders = dict()
	decoders = dict()

	def __init__(self):
		super(JsonTypeRegister, self).__init__()

	@classmethod
	def register(cls, type_name, encoder=None, decoder=None):
		if encoder:
			cls.register_encoder(type_name, encoder)
		if decoder:
			cls.register_decoder(type_name, decoder)

	@classmethod
	def register_encoder(cls, type_name, encoder):
		cls.encoders[type_name] = encoder

	@classmethod
	def register_decoder(cls, type_name, decoder):
		cls.decoders[type_name] = decoder

	@classmethod
	def encode(cls, type_name, obj):
		if type_name in cls.encoders:
			return cls.encoders[type_name](obj)
		elif hasattr(obj, '__json_encode__'):
			return obj.__json_encode__()
		raise KeyError('Failed to find encoder for {}'.format(obj))

	@classmethod
	def decode(cls, type_name, dct):
		if type_name in cls.decoders:
			return cls.decoders[type_name](dct)
		raise KeyError('Failed to find decoder for {}'.format(dct))

