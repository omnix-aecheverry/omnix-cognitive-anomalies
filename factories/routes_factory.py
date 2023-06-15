"""Routes factory module."""
from routes.delay_in_dates import DelayInDatesRoutes

def create_routes(app):
    """Create routes."""
    DelayInDatesRoutes().load_routes(app)