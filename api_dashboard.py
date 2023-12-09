import os
import subprocess



# import os
# import subprocess

# Obtenir le chemin absolu de api.py et dashboard.py
api_path = os.path.abspath("./app/api.py")
dashboard_path = os.path.abspath("./dashboard/my_dashboard.py")

# Obtenez les variables d'environnement actuelles
env = os.environ.copy()

# Modifiez la variable d'environnement PORT pour l'API
env["API_PORT"] = "5000"

# import time
# time.sleep(5)

# Modifiez la variable d'environnement PORT pour Streamlit
env["DASHBOARD_PORT"] = "8000"

# Lancez l'API Flask avec python avec la nouvelle variable d'environnement
api_process = subprocess.Popen(["python", api_path])

# # Attendez un peu pour laisser le serveur Flask s'initialiser
# # Vous pouvez ajuster le délai en fonction de la charge de votre application


###Lancez l'application Streamlit avec streamlit
dashboard_process = subprocess.Popen(["streamlit", "run", dashboard_path], env=env)













# # Chemin relatif pour accéder à api.py et dashboard.py
# # scripts_directory_api = "scoring/api"
# # scripts_directory_dashboard = "scoring/streamlit"

# # Obtenez les variables d'environnement actuelles
# # env = os.environ.copy()

# # # Modifiez la variable d'environnement PORT
# # env["PORT"] =  "5000"
# # executer code 
# # Exécutez api.py avec python avec la nouvelle variable d'environnement

# # subprocess.Popen(["python ./app/api.py"] ,env=env )

# # api_path = os.path.join(os.path.dirname(__file__), "app", "api.py")
# # subprocess.Popen(["python", api_path], env=env)


# # # Exécutez dashboard.py avec streamlit
# # subprocess.Popen(["python -m streamlit run ./dashboard/my_dashboard.py" ,"--server.port" ,"8000"],env=env)

api_process = subprocess.Popen(["python", api_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = api_process.communicate()
print("API Process Output:", stdout.decode())
print("API Process Error:", stderr.decode())
