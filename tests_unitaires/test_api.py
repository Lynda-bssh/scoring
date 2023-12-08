
import requests
from bs4 import BeautifulSoup
import sys
import json
import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template

parent_directory = Path(__file__).resolve().parent.parent
api_directory = parent_directory / "app"
sys.path.append(str(api_directory))
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from api import app
import pytest

### creation d'un client web:
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


### test qui permet de tester la base route de l'api qui plante vers base.html:
def test_base_route(client):
    url = 'http://127.0.0.1:5000/'
    client = app.test_client()
    response = client.get(url)
    
    soup = BeautifulSoup(response.data, 'html.parser')
    assert soup.find('title').text == 'Credit scoring'

    assert response.status_code == 200


### verifier la route de recuperation des ID_client(sk_id_curr):
def test_client_ids_route(client):
    response = client.get('/reference_list')  
    assert response.status_code == 200

    # Renommez la variable 'json' à 'data_response'
    data_response = json.loads(response.get_data(as_text=True))  
    assert 'SK_ID_CURR' in data_response



#   pytest -v test_api.py::test_client_ids_route
# ### tester si cette clé est bien dans response.json:
def test_id_client_in_json(client):

    response = client.get('/reference_list')
    
    assert response.status_code == 200
    # on va s'assurer que la reponse et en json
    assert response.headers['Content-Type'] == 'application/json'
    # Obtenez les données JSON de la réponse
    data_response = response.get_json()
    # Vérifiez que '14525' est présent dans les données JSON
    assert '14525' in data_response





# # ### test pour verifier la prediction:
# def test_predict_route(client):
#     sk_id_curr = 150224
#     data = {'SK_ID_CURR': sk_id_curr}
#     response = client.post('/predict', data=data)

#     assert response.status_code == 200
#     response_data = response.json()

#     # Vérifier si la clé 'probability' est présente dans les données
#     assert 'probability' in response_data



  














       
        





