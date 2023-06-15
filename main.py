"""Main entry point for the application."""
import os
from flask import Flask
from flask_cors import CORS
from docs.api_doc import generate_doc
from factories.routes_factory import create_routes


app = Flask(__name__)
CORS(app)
create_routes(app)
generate_doc(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, host="0.0.0.0", port=port)
