import os
import connexion
from flask_cors import CORS

print(os.environ)

def create_app():
    app = connexion.FlaskApp(__name__, specification_dir='openapi/')
    app.add_api('my_api.yaml', arguments={"server_url": os.environ["SERVER_URL"]})
    CORS(app.app)
    return app
