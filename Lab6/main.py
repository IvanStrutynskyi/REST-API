from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from app.resources.book import BookResource

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

api.add_resource(BookResource, '/books')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
