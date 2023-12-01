

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import joblib
import matplotlib.pyplot as plt
import shap
import os
import time
from st_shape import st_shap
import streamlit.components.v1 as components
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import plotly.graph_objects as go
from sklearn.metrics import make_scorer

#st.set_option('browser.gatherUsageStats', False)
### current directory:
current_directory = os.path.dirname(os.path.abspath(__file__))


### path of model , explainer and scaler:
model_path = os.path.join(current_directory,"..","models","LGBMClassifier.model")
scaler_path = os.path.join(current_directory,"..","models","scaler.model")
explainer_path = os.path.join(current_directory,"..","models","explainer.model")

### path of data
df_path =  os.path.join(current_directory,"..","models","data","df.joblib")
df_origin_path = os.path.join(current_directory,"..","models","data","df_origine.joblib")
test_path = os.path.join(current_directory,"..","models","data","test.joblib")
my_data = joblib.load(df_path)
df_origin = joblib.load(df_origin_path)

### load data:and explainer and model:

df_test = joblib.load(test_path)
scaler = joblib.load(scaler_path)
explainer_model = joblib.load(explainer_path)
model = joblib.load(model_path)
test = df_test[df_test.columns[df_test.columns != "SK_ID_CURR"]]
test_scaler = scaler.transform(test)
df_origin['y_pred'] = my_data['y_pred']
test_origin = df_origin[df_origin.columns[df_origin.columns != "SK_ID_CURR"]]



### --------------configuration de la page--------------------:
st.set_page_config(
    page_title='Profil du Client',layout="wide" )

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
 
# une sidebar( logo de pret à depenser , button select, 
# et 3 autres buttons) 

logo = st.sidebar.image('15510866018677_logo projet fintech.png', use_column_width=True)

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

### -------------------Page principale----------------------
with header:

    st.markdown(
    f'<div style="display: flex; align-items: center;">'
    f'<h1  flex: 1;">Quel est le profil de votre client ?</h1>'
    
    f'</div>',
    unsafe_allow_html=True 
    )

    sel_col, disp_col = st.columns(2)


    # selectionnez l'identifiant de clients:
    with sel_col:
        options = ["Sélectionnez svp !"] + list(my_data['SK_ID_CURR'].unique())
        selected_client = st.selectbox("", options=options, index=0)
        
        
        if selected_client != options[0]:
            st.write("")
            st.write("Vous avez sélectionné l'identifiant n° :", selected_client)
        
    ### Couleur de fond rouge pour messages erronées:
    st.markdown(
        f'<style>.error-text {{ color: white; background-color: rgba(255, 0, 0, 0.5); padding: 13px; border-radius: 5px;font-weight: bold; }}</style>',
        unsafe_allow_html=True
    )

    ## Couleur de fond vert pour messages de succès:
    st.markdown(
        f'<style>.success-text {{ color: white; background-color: rgba(0, 128, 0, 0.4); padding: 13px; border-radius: 5px;font-weight: bold; }}</style>',
        unsafe_allow_html=True
    )
    ###----------------------------------------------###
    #---------header evaluation de la commande avec id_client----------------###
    if case and selected_client in options[1:]:
        st.write(" ")
        st.markdown("<h2 style='color: green;text-align:center'>Evaluation de la demande </h2>", unsafe_allow_html=True)
        st.write(" ")
        st.write(" ")

        selected_row = my_data[my_data["SK_ID_CURR"] == selected_client]
        max_score = selected_row[["Class_0","Class_1"]].max().max()
        result_select = selected_row["y_pred"].iloc[0]
       
        
        if result_select == "Accordé":
            st.markdown(f"<p class='success-text' style='font-size: 18px;'>Crédit accordé</p>", unsafe_allow_html=True)
            
        else:
            
            st.markdown("<p class='error-text' style='font-size: 18px;'>Crédit non accordé</p>", unsafe_allow_html=True)


        ## Affichage de la barre de chargement-----------:
        progress_bar = st.progress(0)
        ## Simulation  de travail en cours
        time.sleep(3) 
        ## mettre a jour de la barre de progression:
        progress_bar.progress(0)  

    ## Une fois le chargement terminé:
        st.success('Loading completed!')
       
        ### jauge pour la probabilité:
        def create_jauge():


            selected_row = my_data[my_data["SK_ID_CURR"] == selected_client]
            
            max_score = selected_row["Class_1"].values[0]
           
            col1, col2 = st.columns(2)
            with col1:
        
                max_score = max_score*100

                fig = go.Figure(go.Indicator(
                    domain={'x': [0, 1], 'y': [0, 1]},
                    value= max_score,
                    mode="gauge+number+delta",
                    title={'text': "Score du client", 'font': {'size': 24}},
                
                    gauge={'axis': {'range': [None, 100],
                            'tickwidth': 3,
                            'tickcolor': 'darkblue'},
                            'bar': {'color': 'white', 'thickness': 0.3},
                            'bgcolor': 'white',
                            'borderwidth': 1,
                            'bordercolor': 'gray',
                            'steps': [{'range': [0, 20], 'color': ' #800080'},
                                    {'range': [20, 40], 'color': '#E6E6FA'},
                                    {'range': [40, 60], 'color': '#C8A2C8'},
                                    {'range': [60, 80], 'color': '#9966CC'},
                                    {'range': [80, 100], 'color': '#8A2BE2'}],
                            'threshold': {'line': {'color': 'white', 'width': 8},
                                        'thickness': 0.8,
                                        'value': max_score}}))

                fig.update_layout(paper_bgcolor='white',
                                height=400, width=400,
                                font={'color': '#772b58', 'family': 'Roboto Condensed'},
                                margin=dict(l=30, r=30, b=5, t=5))
                

                
            st.plotly_chart(fig, use_container_width=True)

                

        if __name__ == '__main__':

            create_jauge()

    
    ###----------------------------------------------###
    #--------- Infos clients( Détails sur le clients------        
    def main():

        info_client = df_origin[df_origin['SK_ID_CURR'] == selected_client ]
        my_client = info_client[["CODE_GENDER","NAME_FAMILY_STATUS","CNT_CHILDREN","OCCUPATION_TYPE","AMT_CREDIT"]]
        melted_df = my_client.melt(var_name='label', value_name='Valeur')
        cmap = LinearSegmentedColormap.from_list("custom_gradient", ["#A40606", "#D98324"])
        if user_choice == '**Détails sur le clients**'and selected_client in options[1:]:
       
            with plt.style.context("fivethirtyeight"):
                fig = plt.figure(figsize=(8, 5))
                plt.fill_betweenx(y=[12, 14], x1=[18, 18], x2=[0, 0], color=cmap(0.5))

                plt.fill_betweenx(y=[11, 12], x1=[16, 18], x2=[2, 0], color=cmap(0), alpha=0.5)
                plt.fill_betweenx(y=[9, 11], x1=[16, 16], x2=[2, 2], color=cmap(0))

                plt.fill_betweenx(y=[8, 9], x1=[14, 16], x2=[4, 2], color=cmap(0.7), alpha=0.5)
                plt.fill_betweenx(y=[6, 8], x1=[14, 14], x2=[4, 4], color=cmap(0.7))

                plt.fill_betweenx(y=[5, 6], x1=[12, 14], x2=[6, 4], color=cmap(1.0), alpha=0.5)
                plt.fill_betweenx(y=[3, 5], x1=[12, 12], x2=[6, 6], color=cmap(1.0))

                plt.fill_betweenx(y=[2, 3], x1=[10, 12], x2=[8, 6], color=cmap(1.0), alpha=0.5)
                plt.fill_betweenx(y=[0, 2], x1=[10, 10], x2=[8, 8], color=cmap(1.0))
                plt.xticks([], [])
                plt.yticks([1, 4, 7, 10,13], melted_df['label'])

                for y, value in zip([1, 4, 7, 10,13], melted_df['Valeur']):
                    plt.text(9, y, value, fontsize=16, color="white", fontweight="bold", ha="center")
                plt.grid(visible=False)
                plt.ylabel("stages")
                st.markdown("<h2 style='color: green;text-align:center'>Information sur le client: </h2>", unsafe_allow_html=True)
    
                st.pyplot(fig)

    if __name__ == '__main__':
        main()





    ### ---------------Features locale---------------###

   
    id_client  = df_test[df_test['SK_ID_CURR']== selected_client]

    explainer_model = joblib.load('../models/explainer.model')
    shap_values_test = explainer_model.shap_values(test_scaler)
    def feature_local():
        
        if user_choice == '**Analyse locale de motifs**':
            st.markdown("<h2 style='color: green;text-align:center'>Analyse locale de motif: </h2>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            instance_idx =  df_test[df_test['SK_ID_CURR']== selected_client].index
            shap.initjs() 

            plt.figure(figsize=(5,5))
            
            st_shap(shap.force_plot(explainer_model.expected_value[1], shap_values_test[1][instance_idx,:],
                 id_client.drop(columns=["SK_ID_CURR"],axis = 1)))
           
            
          
    if __name__ == '__main__':
        feature_local()

  
    ###----------------------------------------------###
    # ##---------partie features globale----------------###

    def feature_global():
        
        if user_choice == '**Analyse globale de motifs**':
            st.markdown("<h2 style='color: green;text-align:center'>Analyse globale de motif: </h2>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            
            shap.initjs()
            st_shap(shap.summary_plot(shap_values_test[1],
                  features = test,
                  feature_names = test.columns,
                  plot_size = (10,8),
                  show = False

                  ))
            plt.title("Interprétation Globale (shap-values)",fontsize = 14)
            plt.tight_layout()
            plt.show()
           
                

    
    if __name__ == '__main__':
        feature_global()
   
          
    
##### ---------------Comparaison avec d'autres clients----------------------

def perspective_client():

    info_client = my_data[my_data['SK_ID_CURR'] == selected_client ]
    # with data origin 
    client = df_origin[df_origin['SK_ID_CURR'] == selected_client]
    if not client.empty:



        val_1 = client['Population_Density'].values[0]
        val_2 = client['CODE_GENDER'].values[0]
        val_3 = client['CNT_CHILDREN'].values[0]
        val_4 = client['NAME_CONTRACT_TYPE'].values[0]
        val_5 = client['FLAG_OWN_CAR'].values[0]
        val_6 = client['DAYS_BIRTH'].values[0]
        df_filtr = df_origin[(df_origin['Population_Density'] == val_1) & (df_origin['CODE_GENDER'] == val_2)& (df_origin['CNT_CHILDREN'] == val_3)& (df_origin['NAME_CONTRACT_TYPE'] == val_4)& (df_origin['FLAG_OWN_CAR'] == val_5)& (df_origin['DAYS_BIRTH'] == val_6)]


        
        variables = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"]
        data = my_data[['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'y_pred']]
        superposed_data = data.melt(id_vars="y_pred", value_vars=["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"])

        #------data for similair client:

        variables = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"]
        df_simil = df_filtr[['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'y_pred']]
        superposed_df = df_simil.melt(id_vars="y_pred", value_vars=["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"])
        
        
        ### ---------groupe de client---------------
        if selected_option == "Groupe Client" :
            st.subheader("Comparaison avec d'autres clients")
            st.dataframe(df_origin.head(5))

            univarie = st.checkbox('Boxplot des caracteristiques principales des clients')
            bivarié = st.checkbox('Analyse bivariée des caractéristiques des clients')

            if univarie:
                
                sns.set_style("whitegrid")
                g = sns.catplot(data=superposed_data, x="variable",y="value", hue="y_pred", kind="box", palette="Set3",showfliers=False, legend=False, height=4, aspect=2)
                plt.title("Analyse univariée des caractéristiques des clients")
                for variable in variables:
                    plt.scatter(x=variable, y=client[variable], 
                                color='#006400', marker='o', s=100)
                g.set_xticklabels(rotation=25)

                plt.legend()
                
                plt.rc('font', size=12)
                st.pyplot(plt)



            if bivarié:

                sel_col, disp_col = st.columns([1,1])
                with sel_col:
                    options = ["Selectionner un caracteristique x"] + list(test.columns)
                    selected_x = st.selectbox("Choisissez X", options=options, index=0)

                with disp_col:
                    options = ["Sélectionner une caracteristique y"] + list(test.columns)
                    selected_y = st.selectbox("Choisissez Y", options=options, index=0)
                if selected_y != options[0] and  selected_x != options[0] : 
                    x = selected_x
                    y = selected_y
                    plt.figure(figsize=(6, 3))
                    palette = sns.color_palette("pastel")
                 
                    sns.scatterplot(x= x, y= y, hue='y_pred', data= my_data, palette="Set1",s = 10)
                    plt.scatter(data = info_client,x = x,y = y , marker='*', color='#006400', s=50, label='Client')

                  

                    plt.legend(fontsize='small')
                    st.pyplot(plt)

        if selected_option == "Similaire Client":

            st.subheader("Comparaison avec d'autres clients")
            st.dataframe(df_filtr.head(5))

            univarie_similaire= st.checkbox('Boxplot des caracteristiques principales des clients similaires')
            bivarié_similaire = st.checkbox('Analyse bivariée des caractéristiques des clients similaires')


            if univarie_similaire:
        


                sns.set_style("whitegrid")
                g = sns.catplot(data=superposed_df, x="variable", y="value", hue="y_pred", kind="box", palette="Set2", showfliers=False, legend=False, height=4, aspect=2)
                plt.title("Analyse univariée des caractéristiques des clients similaires")
                st.write(" ")
                st.write(" ")

                for variable in variables:
                    plt.scatter(x=variable, y=client[variable], color='#006400', marker='o', s=20)

                g.set_xticklabels(rotation=25)


                plt.legend()
               


                plt.rc('font', size=12)
                st.pyplot(plt)


            if bivarié_similaire:

                sel_col, disp_col = st.columns([1,1])
                with sel_col:
                    options = ["Selectionner un caracteristique x"] + list(test_origin.columns)
                    selected_x = st.selectbox("Choisissez X", options=options, index=0)

                with disp_col:
                    options = ["Sélectionner une caracteristique y"] + list(test_origin.columns)
                    selected_y = st.selectbox("Choisissez Y", options=options, index=0)
                if selected_y != options[0] and  selected_x != options[0] : 
                    x = selected_x
                    y = selected_y
                    plt.figure(figsize=(10, 3))
                    palette = sns.color_palette("Set2")
                    sns.scatterplot(x= x, y= y, hue='y_pred', data= df_filtr, palette= palette,s = 10, size = 'y_pred', sizes=(50, 100))
                    plt.scatter(data = client,x = x,y = y , marker='*', color='#006400', s=50, label='Client')


                    plt.legend(fontsize='small')
                    st.pyplot(plt)
    else:
        st.write("")



if __name__ == '__main__':

    perspective_client()



  










    



        
   
        


   