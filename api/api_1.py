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
explainer = load(explainer_path)
model = load(model_path)

test = df_test[df_test.columns[df_test.columns != "SK_ID_CURR"]]
test_scaler = scaler.transform(test)

shap_values_test = explainer.shap_values(test_scaler)
expected_value = explainer.expected_value




app = Flask(__name__)


@app.route('/',methods=['GET'])
def home():
    return render_template('base.html')



@app.route('/reference_list', methods=['GET'])
def client_ids():
    return jsonify(df_test[['SK_ID_CURR']].to_json(orient = 'split'))


# @app.route('/shap', methods=['GET'])
# def explain_img():
#     return send_file('glob_exp.png')

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

        client_pred = client['y_pred'].iloc[0]
        prob_risque =  client["Class_1"].values[0]
        output = client_pred
        
        # Supprimer la colonne ID pour la prédiction
        columns_to_exclude = ['SK_ID_CURR', 'Class_0', 'Class_1', 'y_pred']
        client = client.drop(columns=columns_to_exclude)
        index_client = client.index
    
        # client_scaled = scaler.transform(client)
        # shap_values = explainer.shap_values(client_scaled)
        #gauge_html = generate_gauge(max_score)

        response = {   
                   "probability":prob_risque,
                   'expected_value':expected_value[1],
                   'shap_values': shap_values_test[1][index_client].tolist(),
                    'feature_names': client.columns.tolist(),
                   # 'feature_values': client.values[0].tolist(),
                  

                                
                   }
        return jsonify(response) 
        


  
# @app.route('/features', methods=['POST'])
# def features():

#     sk_id_curr = request.form['SK_ID_CURR']
#     if int(sk_id_curr) in df['SK_ID_CURR'].values:
#         client = df_test[df_test['SK_ID_CURR'] == int(sk_id_curr)]
#         # Supprimer la colonne ID pour la prédiction
#         client = client.drop(columns=['SK_ID_CURR'])
#         client_scaled = scaler(client)
#         explainer = shap.TreeExplainer(model)
#         shap_values = explainer.shap_values(client_scaled)
        
       
#         #gauge_html = generate_gauge(max_score)
#         response = {   
#             'shap_values': shap_values[1][0].tolist(),
#             'feature_names': client.columns.tolist(),
#             'feature_values': client.values[0].tolist()
                        
#                    }
#         return jsonify(response) 




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
     

# ### Features globale:
# @app.route('/afficher_features_globales', methods=['POST'])
# def afficher_features_globales():
#     return render_template('global_features.html')

# @app.route('/images/<path:filename>')
# def serve_image(filename):
#     return send_file('static/css/features_globales.png', mimetype='image/png')



if __name__ == "__main__":
    app.run(debug=True)

