# COGNITIVE

Este proyecto tiene como objetivo proporcionar una solución para procesar datos, clasificando entidades y extrayendo entidades de un texto, utilizando modelos de aprendizaje automático, como Deep Neural Networks y NLPs.

La solución se compone de dos contextos:
    - entity_classification: Clasifica una entidad en una de las categorías definidas.
    - entity_extraction: Extrae entidades de un texto en una estructura de procesos.

## Estructura del proyecto

El proyecto tiene la siguiente estructura:

1. **business**: Contiene las soluciones de problemas específicos utilizando modelos de aprendizaje automático.
2. **factories**: Contiene las clases necesarias para crear instancias de los modelos utilizados en el contexto de negocio
3. **routes**: Contiene las rutas necesarias para acceder a los endpoint de entrenamiento y predicción.
4. **security**: Contiene las medidas de seguridad necesarias para proteger la API.
5. **services**: Contiene los servicios necesarios para el funcionamiento de la API, como el servicio de storage y mensajes.
6. **main.py**: Contiene la configuración necesaria para iniciar el servidor Flask.

## Instalación

1. Instalar las dependencias necesarias, ejecute el siguiente comando:

    ```bash
    $ pip install -r requirements.txt
    ```

3. Ejecutar el script de python "main.py" para iniciar el servidor Flask:

    ```bash
    $ cd src/<contexto>
    $ python main.py
    ```

python version 3.10
También puedes ejecutar el proyecto usando un "run.sh" que contenga las variables de entorno necesarias y el comando de ejecución:

```bash
$ ./run.sh
```

## Entrenamiento

Para entrenar un modelo, se debe enviar una petición POST a la ruta `{domain}/<use_case>/train` con los siguientes parámetros minimos requeridos:

| Parámetro | Descripción | Tipo |
| --------- | ----------- | ---- |
| entity | Entidad con la que se entrenara el modelo | String |
| model | Modelo a entrenar | JSON |
| model.version | Versión del modelo | String |
| model.name | Nombre del modelo | String |
| model.params | Parámetros del modelo | JSON |
| model.params.type | Tipo de dataset (csv, ...) | String |
| model.params.url | URL del dataset | String |

### Contexto de clasificación de entidades

Entrenamiento de una deep neural network para clasificar entidades.

Parametros adisionales requeridos del modelo:

| Parámetro | Descripción | Tipo |
| --------- | ----------- | ---- |
| model.params.labels | Etiquetas de las entidades | Array |


Ejemplo: 

```
POST `http://localhost:3000/entity_classification/train`
```

```JSON
{
    "entity":"omnix",
    "trainProcessId": "123456789",
    "model": {
        "name": "deep_neural_network",
        "version": "v1.0.0",
        "params":{
            "type": "csv",
            "url": "signed.url/data.csv",
            "labels": ["Order", "ShippingGroup", "Channel", "Item", "Reserve", "Stock", "Source","ItemSource","Transaction"] 
        }
    }
}
```

## Inferencia

Para hacer una inferencia con un modelo entrenado, utilice el endpoint "/predict" con la siguiente estructura de datos minima requerida:

| Parámetro | Descripción | Tipo |
| --------- | ----------- | ---- |
| entity | Entidad con la que se entrenara el modelo | String |
| trainProcessId | Identificador del proceso de entrenamiento | String |
| model | Modelo a entrenar | JSON |
| model.version | Versión del modelo | String |
| model.name | Nombre del modelo | String |
| model.params | Parámetros del modelo | JSON |
| data | Datos a inferir/predecir | JSON |

Las rutas de prediccion se component igual que las de entrenamiento.

### Contexto de lenguaje

Clasificacion de entidades usando una deep neural network.

Ejemplo:

```
POST `http://localhost:3000/entity_classification/predict`
```

```JSON
[
    {
        "model": {
            "version": "v1.0.0",
            "name": "deep_neural_network"
        },
        "data": [
            "id",
            "omnixCreationDate"
        ]
    }
]
```

## Variables de entorno

### Variables de entorno generales

| Variable | Descripción | Valor por defecto |
| -------- | ----------- | ----------------- |
| API_KEY | Clave de la API | EMPTY |
| MESSAGE_BROKER_IMPL | Implementacion de message broker | rabbitmq*, aws, azure |
| STORAGE_IMPL | Implementacion de storage | local, aws, azure* |

### Variables de entorno AZURE

| Variable | Descripción | Valor por defecto |
| -------- | ----------- | ----------------- |
| AZURE_STORAGE_CONNECTION_STRING | Cadena de conexión al servicio de Azure Storage | EMPTY |
| AZURE_STORAGE_SAS_TOKEN | Token de acceso a Azure Storage | EMPTY |
| AZURE_STORAGE_CONTAINER_NAME | Nombre del contenedor de Azure Storage | EMPTY |

### Variables de entorno AWS

| Variable | Descripción | Valor por defecto |
| -------- | ----------- | ----------------- |
| AWS_ACCESS_KEY_ID | ID de la llave de acceso a AWS | EMPTY |
| AWS_SECRET_ACCESS_KEY | Llave de acceso a AWS | EMPTY |
| AWS_REGION_NAME | Región de AWS | EMPTY |
| AWS_SNS_TOPIC_ARN | ARN del topic de AWS SNS | EMPTY |
| AWS_S3_BUCKET_NAME | Nombre del bucket de AWS S3 | EMPTY |

### Variables de entorno RABITMQ

| Variable | Descripción | Valor por defecto |
| -------- | ----------- | ----------------- |
| RABBITMQ_URL | URL del servicio de RabbitMQ | EMPTY |
| RABBITMQ_QUEUE | Nombre de la cola de RabbitMQ | EMPTY |
| COGNITIVE_CLOSE_STAGE_EXC | Nombre del exchange de RabbitMQ | EMPTY |


## API DOC

La documentación de la API se encuentra en el siguiente enlace: [API DOC](http://127.0.0.1:3000/api/docs/#/)

Que tiene la forma: `http://localhost:PORT/api/docs/#/`, PORT por defecto: 3000

