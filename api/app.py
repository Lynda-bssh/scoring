import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
df_origin_path = os.path.join(current_directory,"..","models","data","df_origin.joblib")
test_path = os.path.join(current_directory,"..","models","data","test.joblib")

def load(path):
    return joblib.load(path)

df = load(df_path)
df_test = load(test_path)
scaler = load(scaler_path)
explainer_model = load(explainer_path)
model = load(model_path)

test = df_test[df_test.columns[df_test.columns != "SK_ID_CURR"]]
test_scaler = scaler.transform(test)





app = Flask(__name__)


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/predict',methods=['POST'])
def predict():

    sk_id_curr = request.form['SK_ID_CURR']
    if int(sk_id_curr) in df['SK_ID_CURR'].values:
        client = df[df['SK_ID_CURR'] == int(sk_id_curr)]
        client_a = df_test[df_test['SK_ID_CURR'] == int(sk_id_curr)]
        client_pred = client['y_pred'].iloc[0]
        max_score =  client["Class_1"].values[0]
        
        output = client_pred
        gauge_html = generate_gauge(max_score)
        #local = feature_local(client_a)
        return render_template("index.html",gauge_html = gauge_html, prediction_text = f'Votre credit est bien: {output}')
       
    else:
        return render_template('index.html', prediction_text="Veuillez renseigner le bon identifiant svp!")

# result for predictions:
@app.route('/result')
def show_result():
    return render_template('index.html', prediction_text=request.args.get('prediction_text'), gauge_html=request.args.get('gauge_html'))



### features local:
@app.route('/locale_features',methods=['POST'])
def locale_features():

    sk_id_curr = request.form['SK_ID_CURR']
    if int(sk_id_curr) in df['SK_ID_CURR'].values:
        
        client_a = df_test[df_test['SK_ID_CURR'] == sk_id_curr]
       
        local_html = feature_local(client_a)
        return render_template("index.html",local_html = local_html)
       
    else:
        return render_template('base.html', prediction_text="Veuillez renseigner le bon identifiant svp!")

    
   
# result for predictions:
@app.route('/features_local')
def show_features():
    return render_template('index.html', gauge_html=request.args.get('local_html'))
     

### Features globale:
@app.route('/afficher_features_globales', methods=['POST'])
def afficher_features_globales():
    return render_template('global_features.html')

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_file('static/css/features_globales.png', mimetype='image/png')



if __name__ == "__main__":
    app.run(debug=True)

