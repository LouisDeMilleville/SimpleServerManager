from flask import Flask, request, jsonify, Response
import subprocess
import config
import Pages

app = Flask(__name__)

# Route for when the user access the API without specifying an endpoint
@app.route('/', methods=['GET'])
def default():
    return Pages.login_page #Returns the login page to the user
    
# Route for the panel endpoint
@app.route('/panel', methods=['GET'])
def panel():
    return Pages.panel_page # Returns the panel page

# Route for the shutdown endpoint
@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Saving the headers values in variables
    auth_token = request.headers.get('Authorization')
    shutdown_type = request.headers.get('ShutdownType')
    # Verifying the values sent by the user
    if auth_token and shutdown_type:
        if auth_token == config.AUTH_TOKEN:
            duree = ''
            # Converting the shutdown delay to something understandable by the server
            if shutdown_type == "NOW":
                duree = 'now'
            elif shutdown_type == '5M':
                duree = '+5'
            elif shutdown_type == '15M':
                duree = '+15'
            elif shutdown_type == '30M':
                duree = '+30'
            elif shutdown_type == '1H':
                duree = '+60'
            elif shutdown_type == '3H':
                duree = '+180'
            elif shutdown_type == '6H':
                duree = '+360'
            elif shutdown_type == '12H':
                duree = '+720'
            elif shutdown_type == '24H':
                duree = '+1440'
            try:
                # Executing the shutdown command
                subprocess.run(['sudo', 'shutdown', duree], check=True)
                return "True"
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'exécution de la commande shutdown : {e}")
        
    else:
            return "False"
        
# Route for the login endpoint    
@app.route('/login', methods=['POST'])
def login():
    # Comparing the value sent by the user with the one saved in the config file
    auth_token = request.headers.get('Authorization')
    if auth_token == config.AUTH_TOKEN:
        return "True"
    else:
        return "False"
        
# Route for the reboot endpoint  
@app.route('/reboot', methods=['POST'])
def reboot():
    # Saving the headers values in variables
    auth_token = request.headers.get('Authorization')
    reboot_type = request.headers.get('RebootType')
    # Verifying the values sent by the user
    if auth_token and reboot_type:
        if auth_token == config.AUTH_TOKEN:
            duree = ''
            # Converting the reboot delay to something understandable by the server
            if reboot_type == "NOW":
                duree = 'now'
            elif reboot_type == '5M':
                duree = '+5'
            elif reboot_type == '15M':
                duree = '+15'
            elif reboot_type == '30M':
                duree = '+30'
            elif reboot_type == '1H':
                duree = '+60'
            elif reboot_type == '3H':
                duree = '+180'
            elif reboot_type == '6H':
                duree = '+360'
            elif reboot_type == '12H':
                duree = '+720'
            elif reboot_type == '24H':
                duree = '+1440'
            try:
                # Executing the reboot command
                subprocess.run(['sudo', 'shutdown', '-r', duree], check=True)
                return "True"
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'exécution de la commande reboot : {e}")
    else:
            return "Commande invalide X"
   
# Route for the aptupdate endpoint         
@app.route('/aptupdate', methods=['POST'])
def apt_update():
    # Saving the header value in variable
    auth_token = request.headers.get('Authorization')
    # Verifying the value sent by the user
    if auth_token:
        if auth_token == config.AUTH_TOKEN:
            try:
                # Executing the update & upgrade commands
                subprocess.run(['sudo', 'apt-get', 'update'])
                subprocess.run(['sudo', 'apt', 'upgrade'])
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'exécution de la commande d'update : {e}")
            return "Commande valide !"
        else:
            return "Token d'authentification invalide"
    else:
            return "Commande invalide X"
    
    

if __name__ == '__main__':
    # Running the API on the port specified in the config file
    app.run(host='0.0.0.0', port=config.SERVICE_PORT)
