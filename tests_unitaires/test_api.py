import pytest
import requests
from bs4 import BeautifulSoup
import sys
from pathlib import Path
from flask import Flask, request, jsonify, render_template
parent_directory = Path(__file__).resolve().parent.parent
api_directory = parent_directory / "api"
sys.path.append(str(api_directory))
from api import app



### test qui permet de tester la base route de l'api qui plante vers base.html:
def test_base_route():
    url = 'http://127.0.0.1:5000/'
    client = app.test_client()
    response = client.get(url)
    
    soup = BeautifulSoup(response.data, 'html.parser')
    assert soup.find('title').text == 'Credit scoring'

    assert response.status_code == 200


#   pytest -v test_api.py::test_client_ids_route
### verifier la route de recuperation des ID_client(sk_id_curr):
def test_client_ids_route():

    url = 'http://127.0.0.1:5000/reference_list'  
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    # Vérifiez que 'data' est une chaîne JSON valide
    assert 'SK_ID_CURR' in data


### tester si cette clé est bien dans response.json:
def test_id_client_in_json():

    url = 'http://127.0.0.1:5000/reference_list'  
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    # Vérifiez que 'data' est une chaîne JSON valide
    assert '14525' in data


### test pour verifier la prediction:
def test_predict_route():

    url = 'http://127.0.0.1:5000/predict'  
    sk_id_curr = 150224
    data = {'SK_ID_CURR': sk_id_curr}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    data = response.json()
    ### verifier si la probabilité de risque est dans data collectée:
    assert 'probability' in data
   
  














       
        





