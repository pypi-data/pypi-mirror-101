from typing import Type

from mongoengine import Document

from .base_business_logic import BaseBusinessLogic
from .base_crud_business_logic import BaseCRUDBusinessLogic


def get_crud_BusinessLogic(model: Type[Document],
                           CRUD_base_cls: Type[BaseCRUDBusinessLogic]) -> Type[BaseCRUDBusinessLogic]:
	"""
	Factory of crud_BusinessLogic

	:param model:
	:param CRUD_base_cls:
	:return:
	"""

	CRUD_BusinessLogic = CRUD_base_cls
	name = model.__name__

	if not CRUD_BusinessLogic:
		CRUD_BusinessLogic = type(f"{name}CRUDBusinessLogic", (BaseCRUDBusinessLogic,), {"model": model})
	else:
		if not issubclass(CRUD_BusinessLogic.__base__, BaseBusinessLogic):
			return None

	return CRUD_BusinessLogic
