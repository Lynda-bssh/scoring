import streamlit as st
import pandas as pd
import numpy as np
from function import generate_gauge, feature_local,detail_client_function,group_client,scatter_plot
import time
import joblib
import shap
import os
from io import BytesIO
import requests


base_url = 'http://localhost:5000'

def get_client_ids():
    response = requests.get(ids_url)
    return pd.read_json(response.json(), orient = 'split')


def get_image():
    response = requests.get(globale_url)
    return BytesIO(response.content)



def predict(sk_id_curr):
   
    api_url = base_url + "/predict" 
    data = {"SK_ID_CURR": sk_id_curr}
    response = requests.post(api_url, data=data)

    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        st.error(f"Erreur lors de la requête à l'API : {response.status_code}")
        return None
    

def details_client(sk_id_curr):
    #on fait la requête à notre API
    api_url = base_url +  "/d%C3%A9tails_clients"  
    data = {"SK_ID_CURR": sk_id_curr}
    response = requests.post(api_url, data=data)

    # Vérifiez si la requête a réussi:
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        st.error(f"Erreur lors de la requête à l'API : {response.status_code}")
        return None


ids_url = base_url + '/reference_list'
predict_url = base_url + "/predict"
globale_url = base_url + "/images/globale"
detail_client_url = base_url +  "/d%C3%A9tails_clients"

test_ids = get_client_ids()
id_list = sorted(list(test_ids['SK_ID_CURR']))

st.set_page_config(layout="wide")

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()





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

options = [":green[***Examination de l'évaluation:***\n  👇] ", '**Détails sur le clients**', '**Analyse globale de motifs**', '**Analyse locale de motifs**','**Fin-Examination**']

# Demandez à l'utilisateur de sélectionner une option
user_choice = st.sidebar.radio("", options)
st.sidebar.write(" ")

st.sidebar.write('<span style="color: red;">Mise en perspective des autres clients</span>', unsafe_allow_html=True)

case_option  = ["<Select>","Groupe Client", "Similaire Client"]
selected_option = st.sidebar.selectbox("", case_option)






with header:

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
                        unsafe_allow_html=True)
    
    
    ###--------------détail sur le client:---------------------------------------
    if user_choice == '**Détails sur le clients**' :
        st.markdown("<h2 style='color: green;text-align:center'>Détails de client: </h2>", unsafe_allow_html=True)

        if selected_client != options[0] :
            sk_id_curr = selected_client
            if sk_id_curr:
                detail_client_feature= details_client(sk_id_curr)
                if detail_client_feature:
                   
                    feature_names = detail_client_feature['featur_name_avant_transf']
                    feature_values =detail_client_feature['featur_values_avant_transf']
                  
                    fig_client = detail_client_function(feature_names,feature_values)
                  
                    st.pyplot(fig_client)

     #####--------------prespective avec d'autre client----------------------
    if selected_option == "Groupe Client" :
        st.subheader("Comparaison avec d'autres clients")
        

        if selected_client != options[0] :
            sk_id_curr = predict
            current_directory = os.path.dirname(os.path.abspath(__file__))
            df_origin_path = os.path.join(current_directory,"..","models","data","df.joblib")
            df_origin = joblib.load(df_origin_path)
            if sk_id_curr:
                df_origin = pd.DataFrame(df_origin.head(5))  
                df_origin = df_origin.drop(columns = ['SK_ID_CURR'])
                st.dataframe(df_origin.head(5))
                st.write("")   
                univarie = st.checkbox('Boxplot des caracteristiques principales des clients')
                bivarié = st.checkbox('Analyse bivariée des caractéristiques des clients')            
                if univarie:
                    fig_univarie = group_client(selected_client)
                    st.pyplot(fig_univarie )

                if bivarié:
                    st.write("")
                    sel_col, disp_col = st.columns([1,1])
                    with sel_col:
                        options = ["Selectionner un caracteristique x"] + list(df_origin.columns)
                        selected_x = st.selectbox("Choisissez X", options=options, index=0)
                    with disp_col:
                        options = ["Sélectionner une caracteristique y"] + list(df_origin.columns)
                        selected_y = st.selectbox("Choisissez Y", options=options, index=0)
                    if selected_y != options[0] and  selected_x != options[0] : 
                        x = selected_x
                        y = selected_y 

                        fig_scater = scatter_plot(x, y , selected_client)
                        st.pyplot(fig_scater)



    if selected_option == "Similaire Client":
        st.subheader("Comparaison avec d'autres clients")
        

        if selected_client != options[0] :
            
            current_directory = os.path.dirname(os.path.abspath(__file__))
            df_origin_path = os.path.join(current_directory,"..","models","data","df.joblib")
            df_origin = joblib.load(df_origin_path)
            sk_id_curr = predict
            if sk_id_curr:
                df_origin = pd.DataFrame(df_origin.head(5))  
                df_origin = df_origin.drop(columns = ['SK_ID_CURR'])
                st.dataframe(df_origin.head(5))
                st.write("")   
               
                #bivarié = st.checkbox('Analyse bivariée des caractéristiques des clients')            
                # if bivarié:

                 
                  

                #     sel_col, disp_col = st.columns([1,1])
                #     with sel_col:
                #         options = ["Selectionner un caracteristique x"] + list(df_origin.columns)
                #         selected_x = st.selectbox("Choisissez X", options=options, index=0)
                #     with disp_col:
                #         options = ["Sélectionner une caracteristique y"] + list(df_origin.columns)
                #         selected_y = st.selectbox("Choisissez Y", options=options, index=0)
                #     if selected_y != options[0] and  selected_x != options[0] : 
                #         x = selected_x
                #         y = selected_y 
                #         fig_bivarie =similarite_client(x, y,selected_client)
                        
                #         st.pyplot(fig_bivarie )

   



        
    
    
    
    
    
    
    
                  
# #     ###-------------------Analyse globale---------------------------###
 

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
                      
                        


                        shap_figure = feature_local(expected_value, np.array(shape_values), feature_names)
                        st.pyplot(shap_figure)
        
    
    
    



    








        

     
        
    
       




