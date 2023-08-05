from argparse import Namespace
from typing import Type

from flask_restx import Model, Resource
from mongoengine import Document

from businessman.business_logic.utils import get_crud_BusinessLogic


def crud_controller_factory(model: Type[Document],
                            schema_class: Model,
                            **kwargs) -> Namespace:
	"""
	:param model:
	:param schema_class: restx model as output schema
	:return:
	"""
	name = "Object"
	route = f"{name.lower()}"
	api = Namespace(route, description=f'{name} related operations')

	schema_class = api.model(name, schema_class)

	CRUD_service = get_crud_BusinessLogic(kwargs.get("CRUD_service_class"), name, model)

	@api.route("/")
	class ObjectList(Resource):
		CRUD_Service = CRUD_service
		schema = schema_class

		@api.doc(f"object_list {name}")
		# @api.marshal_list_with(schema)
		def get(self):
			"""Object List"""
			return self.CRUD_Service.get_all()

		@api.doc('create_object')
		@api.expect(schema)
		# @api.marshal_with(schema, code=201)
		def post(self):
			"""Create Object"""
			return self.CRUD_Service.create(api.payload), 201

	@api.route(f'/<int:pk>')
	@api.param('pk', 'The Object identifier')
	@api.response(404, 'Object not found')
	class ObjectByParam(Resource):
		CRUD_Service = CRUD_service
		schema = schema_class

		@api.doc('get_object')
		@api.marshal_with(schema)
		def get(self, pk):
			"""Object Detail"""
			obj = self.CRUD_Service.get_by_id(pk)
			if obj:
				return obj
			else:
				api.abort(404)

		@api.doc('update_object')
		@api.expect(schema)
		@api.marshal_with(schema, code=201)
		def put(self, pk):
			"""Update Object"""
			pass

		@api.doc('delete_object')
		def delete(self, pk):
			"""Delete Object"""
			pass

	return api
