# How to install
(French below)
- Clone this repo on your server
- Edit the config.py file and replace the values by the ones you want to use (SERVICE_PORT = the port the service will be running on, AUTH_TOKEN = the password to access the panel, SERVER_IP = the IP address of your server)
- Create a new service file to run the service on your server:
> sudo nano /etc/systemd/system/SimpleServerManager.service

Paste the following inside the file and change the values needed:
```
[Unit]
Description=Service for SimpleServerManager
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/your/install/directory
ExecStart=/bin/bash -c "source /path/to/your/install/directory/venv/bin/activate && exec python3 /path/to/your/install/directory/server.py"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Save the file, then start the service:
> sudo systemctl start SimpleServerManager.service

Verify that the service is running:
> sudo systemctl status SimpleServerManager.service

Set the service to start automatically when your server boot:
> sudo systemctl enable SimpleServerManager.service

Now you can access your instance of SimpleServerManager from another device by typing your_server_ip_address:service_port in your web browser, then type the password you specified in the config file


# Comment installer
- Clonez ce dépot sur votre serveur
- Editez le fichier config.py et remplacez les valeurs par celles que vous souhaitez utiliser (SERVICE_PORT = le port sur lequel écoutera le service, AUTH_TOKEN = le mot de passe à utiliser pour accéder au panel, SERVER_IP = l'adresse IP de votre serveur)
- Créez un nouveau fichier de service pour lancer le service sur votre serveur:
> sudo nano /etc/systemd/system/SimpleServerManager.service

Collez ceci dans le fichier et modifiez les valeurs nécessaires:
```
[Unit]
Description=Service pour SimpleServerManager
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/chemin/vers/votre/dossier/d'installation
ExecStart=/bin/bash -c "source /chemin/vers/votre/dossier/d'installation/venv/bin/activate && exec python3 /chemin/vers/votre/dossier/d'installation/server.py"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Sauvegardez le fichier, puis démarrez le service:
> sudo systemctl start SimpleServerManager.service

Vérifiez que le service est lancé:
> sudo systemctl status SimpleServerManager.service

Faites démarrer le service à chaque redémarrage de votre serveur:
> sudo systemctl enable SimpleServerManager.service

Maintenant vous pouvez accéder à votre instance de SimpleServerManager depuis un autre appareil en tapant adresse_ip_de_votre_serveur:port_du_service dans votre navigateur web, puis en entrant le mot de passe spécifié dans le fichier de config
