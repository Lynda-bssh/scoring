import subprocess
import os

# Chemin relatif pour accéder à api.py et dashboard.py
scripts_directory_api = "./api"
scripts_directory_dashboard = "./streamlit"

# Obtenez les variables d'environnement actuelles
env = os.environ.copy()

# Modifiez la variable d'environnement PORT
env["PORT"] =  "5000"
# executer code 
# Exécutez api.py avec python avec la nouvelle variable d'environnement
subprocess.Popen(["python", f"{scripts_directory_api}/api.py"], env=env)

# Exécutez dashboard.py avec streamlit
subprocess.Popen(["streamlit", "run", f"{scripts_directory_dashboard}/my_dashboard.py", "--server.port", "8080"], env=env)