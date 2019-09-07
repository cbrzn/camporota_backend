from os import environ

import api.server as server
import api.db as database

app = server.start.app 

if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)