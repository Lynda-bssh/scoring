import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
import plotly.graph_objects as go
from function import generate_gauge, feature_local
import joblib 
import os
import shap

current_directory = os.path.dirname(os.path.abspath(__file__))
### load model, explainer and scaler
model_path = os.path.join(current_directory,"..","models","LGBMClassifier.model")
scaler_path = os.path.join(current_directory,"..","models","scaler.model")
explainer_path = os.path.join(current_directory,"..","models","explainer.model")

### 
df_path =  os.path.join(current_directory,"..","models","data","df.joblib")
df_origin_path = os.path.join(current_directory,"..","models","data","df_origine.joblib")
test_path = os.path.join(current_directory,"..","models","data","test.joblib")

def load(path):
    return joblib.load(path)

df = load(df_path)
df_test = load(test_path)
scaler = load(scaler_path)
explainer = load(explainer_path)
model = load(model_path)

test = df_test[df_test.columns[df_test.columns != "SK_ID_CURR"]]
test_scaler = scaler.transform(test)

shap_values_test = explainer.shap_values(test_scaler)
expected_value = explainer.expected_value

df_origin = load(df_origin_path)




app = Flask(__name__)


@app.route('/',methods=['GET'])
def home():
    return render_template('base.html')



@app.route('/reference_list', methods=['GET'])
def client_ids():
    return jsonify(df_test[['SK_ID_CURR']].to_json(orient = 'split'))



### Features globale:
@app.route('/afficher_features_globales', methods=['POST'])
def afficher_features_globales():
    return render_template('global_features.html') 

@app.route('/images/globale')
def serve_image():
    return send_file('./static/css/features_globales.png', mimetype='image/png')



@app.route('/predict',methods=['POST'])
def predict():

    sk_id_curr = request.form['SK_ID_CURR']
    if int(sk_id_curr) in df['SK_ID_CURR'].values:
        client = df[df['SK_ID_CURR'] == int(sk_id_curr)]
        prob_risque =  client["Class_1"].values[0]
        ###Supprimer la colonne ID pour la prédiction
        columns_to_exclude = ['SK_ID_CURR', 'Class_0', 'Class_1', 'y_pred']
        client = client.drop(columns=columns_to_exclude)
        index_client = client.index
        #gauge_html = generate_gauge(max_score)

        response = {   
                   "probability":prob_risque,
                   'expected_value':expected_value[1],
                   'shap_values': shap_values_test[1][index_client].tolist(),
                    'feature_names': client.columns.tolist(),
                    'feature_values': client.values[0].tolist(),
              

                  

                                
                   }
        return jsonify(response) 
        


# result for predictions:
@app.route('/result')
def show_result():
    return render_template('index.html', prediction_text=request.args.get('prediction_text'), gauge_html=request.args.get('gauge_html'))



### features local:
@app.route('/détails_clients',methods=['POST'])
def détails_clients():

    sk_id_curr = request.form['SK_ID_CURR']
    if int(sk_id_curr) in df_origin['SK_ID_CURR'].values:
        ##gerer le client dans le dataframe avent d'encodage pour tirer les information sur le client :
        client_info_origin = df_origin[df_origin['SK_ID_CURR'] == int(sk_id_curr)]
        client_info_origin = client_info_origin.drop(columns=['SK_ID_CURR'])


        response = {   
           "featur_name_avant_transf" :client_info_origin.columns.tolist(),
           "featur_values_avant_transf" :client_info_origin.values[0].tolist()}
        return jsonify(response) 




if __name__ == "__main__":
    #port = os.environ.get("PORT",5000)
    app.run(debug=True)

