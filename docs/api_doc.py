"""Docs"""
from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/docs/openapi.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Omnix Cognitive Language"
    }
)

def generate_doc(app):
    """Generate docs"""

    @app.route("/docs/<path:path>")
    def send_doc(path):
        """Send docs"""
        return send_from_directory('docs', path)

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
