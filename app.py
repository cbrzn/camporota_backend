from os import environ

import api as app
import api.db as database

if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.server.start.run(host='0.0.0.0', port=port)