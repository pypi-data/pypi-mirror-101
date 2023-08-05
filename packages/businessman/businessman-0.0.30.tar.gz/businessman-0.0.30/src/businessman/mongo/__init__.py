import flask_mongoengine
import mongoengine_goodjson


class QuerySet(flask_mongoengine.BaseQuerySet, mongoengine_goodjson.QuerySet):
	"""Queryset."""
	pass


class Document(flask_mongoengine.Document, mongoengine_goodjson.Document):
	"""Document."""
	meta = {
		'abstract': True,
		'queryset_class': QuerySet
	}
