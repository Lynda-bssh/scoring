import os
import subprocess





# Chemin relatif pour accéder à api.py et dashboard.py
# scripts_directory_api = "scoring/api"
# scripts_directory_dashboard = "scoring/streamlit"

# Obtenez les variables d'environnement actuelles
env = os.environ.copy()

# Modifiez la variable d'environnement PORT
env["PORT"] =  "5000"
# executer code 
# Exécutez api.py avec python avec la nouvelle variable d'environnement

subprocess.Popen(["python ./app/api.py"] ,env=env )

# Exécutez dashboard.py avec streamlit
subprocess.Popen(["python -m streamlit run ./dashboard/my_dashboard.py" ,"--server.port" ,"8000"],env=env)

