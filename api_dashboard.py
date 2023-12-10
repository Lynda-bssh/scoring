import os
import subprocess
# Obtenir le chemin absolu de api.py et dashboard.py
api_path = os.path.abspath("./app/api.py")
dashboard_path = os.path.abspath("./dashboard/my_dashboard.py")
# Obtenez les variables d'environnement actuelles
env = os.environ.copy()
# Modifiez la variable d'environnement PORT pour l'API
env["API_PORT"] = "5000"
# Modifiez la variable d'environnement PORT pour Streamlit
#env["DASHBOARD_PORT"] = "8000"
# Lancez l'API Flask avec python avec la nouvelle variable d'environnement
api_process = subprocess.Popen(["python", api_path], env = env, shell=True)
###Lancez l'application Streamlit avec streamlit
#dashboard_process = subprocess.Popen(["streamlit", "run", dashboard_path], env=env, shell = True)
