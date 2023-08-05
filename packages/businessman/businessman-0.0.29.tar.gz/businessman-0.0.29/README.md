# Businessman Package

CRUD Business Logic with auto-generator controller for flask-restx.

example:

import what you need

```python
from flask import Blueprint
from flask_mongoengine import Document
from mongoengine import StringField

from businessman import crud_controller_factory


```
MongoEngine model:
```python
from flask_mongoengine import Document
from mongoengine import StringField

class SampleModel(Document):
	meta = {"collection": "SampleModel"}
	name = StringField()
	code = StringField()
```

Restx Schema model:
```python
from flask_restx import Api, fields
sample_schema = {
	'name': fields.String(required=True, description=''),
	'code': fields.String(required=True, description=''),
}
```

Blueprint and NameSpace:
```python

blueprint = Blueprint('api', __name__)
api = Api(
	blueprint,
	title='Calendar API Service',
	version='1.0',
	description='A description',
	# All API metadatas
)

ns1 = crud_controller_factory(model=SampleModel, schema_class=sample_schema)
api.add_namespace(ns1)
```
all of the above is for `api.py`:

1. define a flask blueprint
2. create a `restx.Namespace` from defined model with `crud_controller_factory` function tools
3. add this namespace to the blueprint
4. add the blueprint to the `flask.App` object

flask `app.py`:
```python
from flask import Flask
from flask_mongoengine import MongoEngine

from api import blueprint

app = Flask(__name__)
db = MongoEngine()
app.config.from_pyfile("config.py")
db.init_app(app)

app.register_blueprint(blueprint)
if __name__ == "__main__":
	app.run(debug=True)

```