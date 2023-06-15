"""Delay In Datesn Routes."""

from flask import Blueprint, jsonify, request, copy_current_request_context
from security.authorizer import require_api_key
from factories.model_factory import ModelFactory
from routes.async_response import AsyncResponse

class DelayInDatesRoutes:
    """Delay In Dates Routes."""

    def __init__(self):
        self.blue_print = Blueprint(
            "entity_classification", __name__, url_prefix='/delay_in_dates')

    def load_routes(self, app):
        """Load the routes."""

        AsyncResponse(app)

        @app.errorhandler(Exception)
        def handle_error(error):
            response = {"message": str(error)}
            return jsonify(response), 500

        @self.blue_print.route("/train", methods=["POST"])
        @require_api_key
        def train():
            """
            Train model
            """
            
            @app.async_response
            @copy_current_request_context
            @require_api_key
            def train_async_response():
                app.preprocess_request()
                _input = request.get_json()
                model = ModelFactory().create_model(_input["model"]["name"])
                model.train(_input)

            response = {"message": "Accepted"}
            return jsonify(response), 202

        @self.blue_print.route("/predict", methods=["POST"])
        @require_api_key
        def predict():
            """
            Delay In Dates
            """
            _input = request.get_json()
            result = []
            for element in _input:
                model = ModelFactory().create_model(element["model"]["name"])
                result.append(model.predict(element))
            response = {"message": result}
            return jsonify(response), 200

        app.register_blueprint(self.blue_print)
