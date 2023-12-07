
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template
import plotly.graph_objects as go
import joblib 
import shap
import os
import joblib
import streamlit.components.v1 as components
from matplotlib.colors import LinearSegmentedColormap

### -------------fonction features_local-----------------
def feature_local(expected_value,shape_values, feature_names):
      
    
    plt.figure(figsize=(28,28))
    plt.title('Force Plot SHAP')
    
    shap.force_plot(expected_value, shape_values, feature_names, matplotlib = True)
    plt.tight_layout()
    shap_fig = plt.gcf()
    return shap_fig
#------------------------------fonction détails sur le client------------------

def detail_client_function(feature_names,feature_values):

    data = {'Feature': feature_names, 'Value': feature_values}
    data_client = pd.DataFrame(data)
    my_client = data_client.loc[0:4]
    cmap = LinearSegmentedColormap.from_list("custom_gradient", ["#A40606", "#D98324"])

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
        plt.yticks([1, 4, 7, 10,13], my_client['Feature'])

        for y, value in zip([1, 4, 7, 10,13], my_client['Value']):
            plt.text(9, y, value, fontsize=16, color="white", fontweight="bold", ha="center")
        plt.grid(visible=False)
        plt.ylabel("stages")
        return fig
    



    ####----------comparaison avec d'autre clients--------------------

current_directory = os.path.dirname(os.path.abspath(__file__))
df_origin_path = os.path.join(current_directory,"..","models","data","df_origine.joblib")
df_path = os.path.join(current_directory,"..","models","data","df.joblib")
df_origin = joblib.load(df_origin_path)
my_data = joblib.load(df_path)
       
variables = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"]
data = my_data[['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'y_pred']]
superposed_data = data.melt(id_vars="y_pred", value_vars=["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY"])

        #------data for similair client:



import seaborn as sns

def group_client(selected_client):
    client = df_origin[df_origin['SK_ID_CURR'] == selected_client]  
    sns.set_style("whitegrid")
    g = sns.catplot(data=superposed_data, x="variable",y="value", hue="y_pred", kind="box", palette="Set3",showfliers=False, legend=False, height=4, aspect=2)
    plt.title("Analyse univariée des caractéristiques des clients")
    for variable in variables:
            plt.scatter(x=variable, y=client[variable], 
                        color='#006400', marker='o', s=100)
    g.set_xticklabels(rotation=25)

    plt.legend()
        
    plt.rc('font', size=12)

    return plt


def scatter_plot(x, y,selected_client):
    info_client = my_data[my_data['SK_ID_CURR'] == selected_client ]
    plt.figure(figsize=(6, 3))
    palette = sns.color_palette("pastel")
                 
    sns.scatterplot(x= x, y= y, hue='y_pred', data= my_data, palette="Set1",s = 10)
    plt.scatter(data = info_client,x = x,y = y , marker='*', color='#006400', s=50, label='Client')
    plt.legend(fontsize='small')
    return plt
       

def generate_gauge(max_score):

    max_score = max_score*100
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=max_score,
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
                    height=600, width=800,
                    font={'color': '#772b58', 'family': 'Roboto Condensed'},
                    margin=dict(l=30, r=30, b=5, t=5))

    return fig