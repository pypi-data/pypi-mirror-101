from flask_restx import fields


class CustomDtaTimeField(fields.Raw):
	def format(self, value):
		value = value['$date']
		return super(CustomDtaTimeField, self).format(value)


class CustomIDField(fields.Raw):
	def format(self, value):
		value = value['$oid']
		return super(CustomIDField, self).format(value)


class CustomNestedField(fields.Nested):

	def __init__(self, model, allow_null=False, skip_none=False, as_list=False, **kwargs):
		model_name = kwargs.get("model_name")
		if not model_name:
			raise Exception("You don't set [model_name]. It's required.")
		try:
			self.model_name = kwargs.pop("model_name")
		except:
			raise Exception("You have some issue in [model_name].")

		super().__init__(model, allow_null, skip_none, as_list, **kwargs)
