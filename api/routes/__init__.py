from api.server.start import api
from api.controllers.Users import Users

api.add_resource(Users, '/user/<string:email>')