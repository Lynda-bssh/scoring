import subprocess
import os



# Chemin relatif pour accéder à api.py et dashboard.py
# scripts_directory_api = "scoring/api"
# scripts_directory_dashboard = "scoring/streamlit"

# Obtenez les variables d'environnement actuelles
env = os.environ.copy()

# Modifiez la variable d'environnement PORT
env["PORT"] =  "5000"
# executer code 
# Exécutez api.py avec python avec la nouvelle variable d'environnement
subprocess.Popen(["pwd"] ,shell = True )
subprocess.Popen(["ls"] ,shell = True )
subprocess.Popen(["python ./app/api.py"] ,shell = True )

# Exécutez dashboard.py avec streamlit
subprocess.Popen(["python -m streamlit run ./dashboard/my_dashboard.py"",--server.port", "8080"], shell=True)
# "--server.port", "8080"
