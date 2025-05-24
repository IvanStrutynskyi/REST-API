from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from resources.book import BookResource

app = Flask(__name__)

swagger = Swagger(app)

api = Api(app)

api.add_resource(BookResource, "/books", "/books/<string:book_id>")

if __name__ == "__main__":
    app.run(debug=True)
