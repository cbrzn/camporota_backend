from api.server.start import api
from api.controllers.Users import Users, Authentication
from api.controllers.Properties import Properties

api.add_resource(Users, '/user/<string:email>', '/user')
api.add_resource(Authentication, '/login', '/logout')
api.add_resource(Properties, '/properties')
