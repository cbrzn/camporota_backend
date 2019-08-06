from app import create_app
import os
if __name__ == '__main__':
    server = create_app()
    port = int(os.environ.get("BACKEND_PORT", 5000))
    server.run(host='0.0.0.0', port=port)