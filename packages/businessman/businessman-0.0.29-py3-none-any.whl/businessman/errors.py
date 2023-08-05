class NotFound(Exception):
	def __init__(self, key, model):
		super().__init__(f"{key} not found in {model}!")