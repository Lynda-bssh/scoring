
import streamlit as st
import pandas as pd
import numpy as np
from function import generate_gauge, feature_local
import matplotlib.pyplot as plt
import seaborn as sns
import time
import shap
from io import BytesIO
#from st_shape import st_shap
import streamlit.components.v1 as components
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import plotly.graph_objects as go
from sklearn.metrics import make_scorer
import requests


def get_client_ids():
    response = requests.get(ids_url)
    return pd.read_json(response.json(), orient = 'split')


def get_image():
    response = requests.get(globale_url)
    return BytesIO(response.content)





# def get_prediction(sk_id_curr):
#     data = {'SK_ID_CURR': sk_id_curr}
#     response = requests.post(predict_url, json=data)
#     if response.status_code == 200:
#         result = response.json()
#         return result, response.status_code
#     else:
#         st.error(f"Erreur lors de la requête à l'API : {response.status_code}")
#         return None, response.status_code

def predict(sk_id_curr):
    # Faites la requête à votre API
    api_url = "http://127.0.0.1:5000/predict"  # Remplacez par l'URL réelle de votre API
    data = {"SK_ID_CURR": sk_id_curr}
    response = requests.post(api_url, data=data)

    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        st.error(f"Erreur lors de la requête à l'API : {response.status_code}")
        return None

# explainer_path = ("./models/explainer.model")
# explainer_model = load(explainer_path)

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

# st.set_page_config(
#     page_title='Profil du Client',layout="wide" )


st.markdown(
    f"""
    <style>
    .stButton > button {{
        width: 220px;  
        height: 60px; 
        font-size: 28px;  
        display:center;
        margin-left: 30px;
   
    }}
    </style>
    """,
    unsafe_allow_html=True,

)
st.sidebar.write(" ")

case = st.sidebar.button("Etat de la requette")

options = [":green[***Examination de l'évaluation:***\n  👇] ", '**Détails sur le clients**', '**Analyse locale de motifs**', '**Analyse globale de motifs**']

# Demandez à l'utilisateur de sélectionner une option
user_choice = st.sidebar.radio("", options)
st.sidebar.write(" ")




st.sidebar.write('<span style="color: red;">Mise en perspective des autres clients</span>', unsafe_allow_html=True)

case_option  = ["<Select>","Groupe Client", "Similaire Client"]
selected_option = st.sidebar.selectbox("", case_option)
ids_url = "http://127.0.0.1:5000/reference_list"
predict_url = "http://127.0.0.1:5000/predict"
globale_url = "http://127.0.0.1:5000/images/globale"



test_ids = get_client_ids()
id_list = sorted(list(test_ids['SK_ID_CURR']))




with header:

       ### Couleur de fond rouge pour messages erronées:
  

    ## Couleur de fond vert pour messages de succès:
    st.markdown(
        f'<style>.success-text {{ color: white; background-color: rgba(0, 128, 0, 0.4); padding: 13px; border-radius: 5px;font-weight: bold; }}</style>',
        unsafe_allow_html=True
    )

    st.markdown(
    f'<div style="display: flex; align-items: center;">'
    f'<h1  flex: 1;">Quel est le profil de votre client ?</h1>'
    
    f'</div>',
    unsafe_allow_html=True 
    )

    options = ["Sélectionnez svp !"] + list(test_ids['SK_ID_CURR'].unique())
    selected_client = st.selectbox("", options=options, index=0)

        
            
    if selected_client != options[0] :
            
        st.write("Vous avez sélectionné l'identifiant n° :", selected_client)
        sk_id_curr = selected_client
        #---------header evaluation de la commande avec id_client----------------###
        if case :
            st.write(" ")
            st.markdown("<h2 style='color: green;text-align:center'>Evaluation de la demande </h2>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            if sk_id_curr:
                prediction= predict(sk_id_curr)
                # result = predict(sk_id_curr)

                if prediction :


                    progress_bar = st.progress(0)
                    time.sleep(2) 
                    ## mettre a jour de la barre de progression:
                    progress_bar.progress(0) 
                    
                    if prediction['probability'] < 0.5:
                       
                        st.markdown(f"<p class='success-text' style='font-size: 18px;'>Félécitation votre crédit est accordé avec une probabilité de risque:</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='error-text' style='font-size: 18px;'>Crédit non accordé</p>", unsafe_allow_html=True)

                    gauge_figure = generate_gauge(prediction['probability'])
                    st.plotly_chart(gauge_figure)
                else:
                    st.warning("Veuillez entrer une valeur pour SK_ID_CURR.")



        

                    st.markdown(
                        f'<style>.error-text {{ color: white; background-color: rgba(255, 0, 0, 0.5); padding: 13px; border-radius: 5px;font-weight: bold; }}</style>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<style>.error-text {{ color: white; background-color: rgba(255, 0, 0, 0.5); padding: 13px; border-radius: 5px;font-weight: bold; }}</style>',
                        unsafe_allow_html=True
                    )

    
                    st.markdown(
                        f'<style>.success-text {{ color: white; background-color: rgba(0, 128, 0, 0.4); padding: 13px; border-radius: 5px;font-weight: bold; }}</style>',
                        unsafe_allow_html=True
                    )
# #     ###----------------------------------------------###
 

    if user_choice == '**Analyse globale de motifs**':
        st.markdown("<h2 style='color: green;text-align:center'>Analyse globale de motif: </h2>", unsafe_allow_html=True)

        image = st.image(get_image(), caption='Image provenant de l\'API Flask', use_column_width=True)
        ###______________analyse locale_____________________
        
    if user_choice == '**Analyse locale de motifs**':
            st.markdown("<h2 style='color: green;text-align:center'>Analyse locale de motif: </h2>", unsafe_allow_html=True)
            st.write(" ")
            if selected_client != options[0] :
                sk_id_curr = selected_client
                if sk_id_curr:
                    prediction= predict(sk_id_curr)

                    if prediction :
                        expected_value = prediction['expected_value']
                        shape_values = prediction['shap_values']
                        feature_names = prediction['feature_names']
                        #feature_values = prediction['feature_values']
                        


                        shap_figure = shap.force_plot(expected_value, shape_values[0], feature_names)
                        st.pyplot(shap_figure)
        
    
    
    



    








        

     
        
    
       




