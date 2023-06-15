"""Deep Neural Network Entity Classifier"""
import os
import pickle
import requests
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from factories.storage_factory import StorageFactory
from factories.message_broker_factory import MessageBrokerFactory


class IsolationForestAnomalyDetector:
    """IsolationForestAnomalyDetector Class"""
    _model = None
    _version_loaded = None
    _scaler = None
    _le = None
    _labels = None
    _models_path = "business/delay_in_dates/models"
    _data_path = "business/delay_in_dates/data"

    def download_dataset(self, url, file_name):
        """Download dataset from url"""
        if not os.path.exists(f"{self._data_path}/{file_name}"):
            if not os.path.exists(f"{self._data_path}"):
                os.makedirs(f"{self._data_path}")
            with open(f"{self._data_path}/{file_name}", "wb") as dataset:
                response = requests.get(url, timeout=5000)
                dataset.write(response.content)

    def load_data(self, url, file_name):
        """Load dataset for training"""
        self.download_dataset(url, file_name)

        # Cargar los datos
        return pd.read_csv(f"{self._data_path}/{file_name}")

    def upload_model(self, model_path, le_path):
        """Upload model to storage"""
        storage = StorageFactory().create_storage()
        model_url = storage.upload(model_path, model_path)
        le_url = storage.upload(le_path, le_path)
        return model_url, le_url

    def download_model(self, model_path, le_path):
        """Download model from storage"""
        storage = StorageFactory().create_storage()
        storage.download(model_path)
        storage.download(le_path)

    def save_model(self, version):
        """Save model in directory and upload to storage"""
        model_name = f"model_{version}.pkl"
        le_name = f"le_{version}.pkl"

        # Save model in directory that not exists
        if not os.path.exists(f"{self._models_path}/{version}"):
            os.makedirs(f"{self._models_path}/{version}")

        model_path = f"{self._models_path}/{version}/{model_name}"
        le_path = f"{self._models_path}/{version}/{le_name}"

        # Save model in directory
        pickle.dump(self._model, open(model_path, "wb"))
        pickle.dump(self._le, open(le_path, "wb"))

        # Upload model to storage
        model_url, le_url = self.upload_model(model_path, le_path)
        return {
            "model": model_url["link"],
            "label_encoder": le_url["link"]
        }

    def load_model(self, version):
        """Load model from storage"""
        if not self._model or self._version_loaded != version:
            self._version_loaded = version

            model_path = f"{self._models_path}/{version}/model_{version}.pkl"
            labels_path = f"{self._models_path}/{version}/labels_{version}.pkl"

            if not os.path.exists(model_path):
                self.download_model(model_path, labels_path)

            self._model = pickle.load(
                open(model_path, "rb"))
            self._labels = pickle.load(
                open(labels_path, "rb"))

    def train(self, _input):
        """Train model"""
        print("Training model...")
        print("Input: ", _input)
        # Obtener la url del dataset
        url = _input.get("model", {}).get("params", {}).get("url", None)
        file_name = _input.get("model", {}).get(
            "params", {}).get("fileName", None)

        # Cargar los datos
        data = self.load_data(url, file_name)

        # Obtener las variables categóricas
        self._labels = _input.get("model", {}).get(
            "params", {}).get("labels", None)

        #TODO INICIA IMPL
        # Seleccionar las características que vamos a usar
        X = data[['activeTime', 'desviation', 'label']]

        # Codificar variables categóricas
        le = LabelEncoder()
        X['label'] = le.fit_transform(X['label'])

        # Escalar las características
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(X)

        # Entrenar el modelo de detección de anomalías
        model = IsolationForest(contamination='auto')
        model.fit(x_scaled)

        # Guardar el encoder y el scaler
        self._scaler = scaler
        self._le = le

        # Obtener la versión del modelo
        version = _input.get("model", {}).get("version", None)

        # Guardar el modelo
        urls = self.save_model(version)

        # Get loss and accuracy
        loss = 0
        accuracy = 0
        #FINALIZA IMPL

        message = {
            "trainProcessId": _input.get("trainProcessId", None),
            "stageTag": _input.get("stageTag", None),
            "result": {
                "urls": urls,
                "loss": loss,
                "accuracy": accuracy,
                "algorithmId": _input.get("algorithmId", None),
            }
        }

        topic = MessageBrokerFactory().create_message_broker()

        topic.publish(message)
        print("Message published")

        print("Output: ", message)
        return message

    def predict(self, input_data):
        """Predict model"""
        print("Predicting model...")
        print("Input: ", input_data)
        # Version del modelo
        version = input_data.get("model", {}).get("version", None)

        # Cargar el modelo
        self.load_model(version)

        # Obtener los datos de entrada que se van a inferir
        data = input_data.get("data", [])

        # Obtener las variables categóricacas

        # Escalar los datos

        # Predecir

        # Obtener la predicción

        # print("Output: ", label[0])
        return label[0]
