import os
import subprocess

# Obtenir le chemin absolu de api.py et dashboard.py
dashboard_path = os.path.abspath("./dashboard/my_dashboard.py")
# Obtenez les variables d'environnement actuelles
env = os.environ.copy()
env["DASHBOARD_PORT"] = "8000"


###Lancez l'application Streamlit avec streamlit
dashboard_process = subprocess.Popen(["streamlit", "run", dashboard_path], env=env, shell = True)
