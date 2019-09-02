from api.server.start import instance

@instance.route('/test')
def this_is_a_test():
    return "It works"