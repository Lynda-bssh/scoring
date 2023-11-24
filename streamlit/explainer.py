import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt
import seaborn
import streamlit as st

scaler = joblib.load("../models/scaler.model")
df_test = pd.read_csv('../Data/traitement_test/test.csv')

test = df_test[df_test.columns[df_test.columns != "SK_ID_CURR"]]
test_scaler = scaler.transform(test)
explainer = joblib.load("../models/explainer.model")
shap_values_test = explainer.shap_values(test_scaler)

# def explainer_model():
#     explainer = joblib.load("../models/explainer.model")
#     shap_values_test = explainer.shap_values(test_scaler)
#     return shap_values_test, explainer



matplotlib.use('Agg')

def features_global(shap_values_test, test):
    shap.initjs()
    fig, ax = plt.subplots()
    shap.summary_plot(
        shap_values_test[0],
        features=test,
        feature_names=test.columns,
        plot_size=(10, 8),
        show=False,
        ax=ax  # Passer l'axe de la figure à shap.summary_plot
    )
    plt.title("Interprétation Globale (shap-values)", fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)
# def features_global():

#     shap.initjs()
#     shap.summary_plot(shap_values_test[0],
#                   features = test,
#                   feature_names = test.columns,
#                   plot_size = (10,8),
#                   show = False

#                   )
#     plt.title("Interprétation Globale (shap-values)",fontsize = 14)
#     plt.tight_layout()
#     plt.show()
#     plt.fig()
#     return 





