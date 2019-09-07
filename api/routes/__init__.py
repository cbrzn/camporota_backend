from api.server.start import api
from api.controllers.Users import Users, Authentication

api.add_resource(Users, '/user/<string:email>', '/user')
api.add_resource(Authentication, '/login', '/logout')
