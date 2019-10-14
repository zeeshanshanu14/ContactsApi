from flask import Blueprint
from flask_restful import Api
from resources.Contact import ContactResource


api_bp = Blueprint('contactapi', __name__)
api = Api(api_bp)

# Routes
api.add_resource(ContactResource, '/Contact')