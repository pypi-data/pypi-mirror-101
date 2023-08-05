
class BaseBusinessLogic:
	form: object = None

	@classmethod
	def get_form(cls):
		return cls.form
