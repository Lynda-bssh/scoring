import pytest
import os
import joblib
import os
import sys
from pathlib import Path


parent_directory = Path(__file__).resolve().parent.parent
api_directory = parent_directory / "api"
sys.path.append(str(api_directory))

from app import app, current_directory



### testing le chargement de data_prediction pour le module api:
def test_loading_predict_data():
    
    df_predict_path = os.path.join(current_directory,"..","models","data","df.joblib")

    df_predict = joblib.load(df_predict_path)
    assert df_predict is not None, "Erreur de chargement de modèle"

### testing le chargement du modele lgbmclassifier pour le module api
def test_loading_model():

    model_path = os.path.join(current_directory,"..","models","LGBMClassifier.model")

    model = joblib.load(model_path)
    assert model is not None, "Erreur de chargement de modèle"

### testing home route


@pytest.fixture
def web_client():
    return 'http://127.0.0.1:5000/predict'


def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Home Page' in response.data


def test_predict_route(client):
    
    response = client.post('/predict', data={'SK_ID_CURR': '10001'})
    assert response.status_code == 200
    assert b'Your credit prediction:' in response.data