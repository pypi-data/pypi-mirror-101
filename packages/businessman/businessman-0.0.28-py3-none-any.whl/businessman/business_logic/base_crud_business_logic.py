from typing import List, Type, Union
import json

from mongoengine import Document

from businessman.errors import NotFound
from .base_business_logic import BaseBusinessLogic


def document_json_serializer(obj):
	obj_dict = json.loads(obj.to_json())
	return obj_dict


class BaseCRUDBusinessLogic(BaseBusinessLogic):
	model: Type[Document] = Type[Document]

	#
	# @classmethod
	# def get_form(cls):
	# 	# TODO get form from model
	# 	form = cls.form
	# 	if not form:
	# 		pass
	# 	return form

	@classmethod
	def get_all(cls) -> List[model]:
		"""
		:return: all object of model
		"""
		object_list = cls.model.objects.all()
		object_list = list(map(document_json_serializer, object_list))
		return object_list

	# @classmethod
	# def get_all_pagination(cls, after: Union[str, int] = None, first: int = 0, ) -> Dict[str, Any]:
	# 	"""
	# 	:param first: count of object after $after
	# 	:param after: first object as courser
	# 	:return: List of [model] object paginated
	#
	# 	"""
	# 	# TODO from $after object count of $first
	# 	# TODO It must Contain filter for object
	# 	# TODO add [hasNextPage], [hasPreviousPage], [Count]
	# 	# TODO add filtering for object
	# 	res = {
	# 		"hasNextPage": True,
	# 		"hasPreviousPage": True,
	# 		"data": []
	# 	}
	# 	return res

	@classmethod
	def get_by_id(cls, pk: Union[str, int]) -> model:
		selected_users = cls.model.objects(pk=pk)
		if len(selected_users) > 0:
			return selected_users[0]
		raise NotFound(pk, cls.model)

	@classmethod
	def create(cls, kwargs) -> model:
		item = cls.model(**kwargs)
		item = item.save()
		item = cls.model.objects.get(id=item.id)
		return json.loads(item.to_json())

	# @classmethod
	# def create(cls, payload: Dict) -> model:
	# 	# TODO check with form
	# 	# TODO create new object
	#
	# 	# model_form = cls.get_form()
	# 	# form = model_form(payload)
	# 	# if form.validate():
	# 	# 	pass
	# 	pass

	@classmethod
	def update(cls, pk: str, **item_info) -> model:
		item = cls.get(pk)
		for key, val in item_info.items():
			setattr(item, key, val)
		return item.save()

	@classmethod
	def delete(cls, pk: str) -> None:
		item = cls.get(pk)
		item.delete()
