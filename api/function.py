
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template
import plotly.graph_objects as go
import joblib 
import shap


def feature_local(client, explainer_model, test_scaler):
      
    shap_values_test = explainer_model.shap_values(test_scaler)
    instance_idx =  client.index
    shap.initjs() 
    plt.figure(figsize=(5,5))
    force_plot = shap.force_plot(explainer_model.expected_value[1], shap_values_test[1][instance_idx,:],
                client.drop(columns=["SK_ID_CURR"],axis = 1))
    force_plot_fig = go.Figure(force_plot.data)
    force_plot_fig.update_layout(
        paper_bgcolor='white',
        font={'color': '#772b58', 'family': 'Roboto Condensed'},
        margin=dict(l=30, r=30, b=5, t=5)
    )
    return force_plot_fig.to_html(full_html=False)





def generate_gauge(max_score):
    max_score = max_score * 100

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
                    height=200, width=400,
                    font={'color': '#772b58', 'family': 'Roboto Condensed'},
                    margin=dict(l=30, r=30, b=5, t=5))

    return fig.to_html(full_html=False)