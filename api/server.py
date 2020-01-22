import os
import connexion
from flask_cors import CORS
from tx.connexion.utils import ReverseProxied

api_readonly = os.environ.get("API_READONLY", "")
def create_app():
    app = connexion.FlaskApp(__name__, specification_dir='openapi/')
    if api_readonly == "1":
        app.add_api('api_readonly.yaml')
    else:
        app.add_api('my_api.yaml')
    CORS(app.app)
    flask_app = app.app
    proxied = ReverseProxied(
        flask_app.wsgi_app
    )
    flask_app.wsgi_app = proxied
    return app
