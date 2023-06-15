"""Model factory module."""
from business.delay_in_dates.isolation_forest import IsolationForestAnomalyDetector

models = {
    "isolation_forest" : IsolationForestAnomalyDetector,
}

class ModelFactory:
    """Model factory class."""
    def create_model(self, model_name):
        """Create model."""
        return models[model_name]()