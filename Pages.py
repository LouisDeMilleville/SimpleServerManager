import config

login_page = f"""
<!doctype html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SimpleServerManager Login</title>
</head>
<body>
    <h1>Page de connexion</h1>
    Saisissez le mot de passe d'accès : <input id="password_input" type="password"></input> <br />
    <button id="button_login">Connexion</button>
</body>
<script>
    const buttonLogin = document.getElementById("button_login");
    //Function to create a cookie
    function setCookie(name, value, days) {{
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        let expires = "expires=" + date.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/";
    }}
    
    // Login endpoint
    const url = "{config.SERVER_IP}:{config.SERVICE_PORT}/login"

    //Function executed when the login button is clicked
    buttonLogin.onclick = function(){{
        const authToken = document.getElementById("password_input").value;

        //Function to make a POST request to the login endpoint
        async function postData(url = '') {{
            try {{
                // Configuration de la requête
                const response = await fetch(url, {{
                    method: 'POST',
                    headers: {{
                        'Authorization': `${{authToken}}`
                    }}
                }});

                const result = await response.text(); //The server will return True if the password is correct and False if it's not

                if (result === 'True') {{
                    console.log('Autorisation réussie.');
                    setCookie("login", authToken, 365); //Saving the panel password in a cookie
                    console.log('Cookie créé. Redirection vers le panel...');
                    window.location.href = '{config.SERVER_IP}:{config.SERVICE_PORT}/panel'; //Redirecting the user to the panel
                }} else {{
                    alert("Mot de passe incorrect");
                }}
            }} catch (error) {{
                console.error('Erreur:', error);
            }}
        }}

        // Calling the function to make the POST request to the login endpoint
        postData(url);
    }}
</script>
</html>
"""















panel_page = f"""
    <!doctype html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SimpleServerManager Panel</title>
    </head>
    <script>
        // Function to get the value of a cookie
        function getCookie(name) {{
            const nameEQ = name + "=";
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {{
                let cookie = cookies[i];
                while (cookie.charAt(0) === ' ') {{
                    cookie = cookie.substring(1, cookie.length);
                }}
                if (cookie.indexOf(nameEQ) === 0) {{
                    return cookie.substring(nameEQ.length, cookie.length);
                }}
            }}
            return null;
        }}

        // The script get the value of the login cookie to make sure the user is authentified
        const loginCookieValue = getCookie('login');

        // Then verifies with the login endpoint that the cookie's value is correct
        if (loginCookieValue) {{
            console.log("Le cookie 'login' existe, sa valeur est : " + loginCookieValue);
            // API endpoint for login
            const url = '{config.SERVER_IP}:{config.SERVICE_PORT}/login';

            // Function to make the POST request to the login endpoint
            async function postData(url = '') {{
                try {{
                    const response = await fetch(url, {{
                        method: 'POST',
                        headers: {{
                            'Authorization': `${{loginCookieValue}}`
                        }}
                    }});

                    const result = await response.text(); // The login endpoint returns True if the login value is correct and False if it's not

                    if (result === 'True') {{
                        console.log('Cookie valide.');
                        //The user can stay on the page if the login is correct
                    }} else {{
                        console.log('Cookie présent mais invalide, redirection');
                        document.cookie = "login=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                        window.location.href = '{config.SERVER_IP}:{config.SERVICE_PORT}';
                        // If the cookie's value is incorrect, the cookie is deleted then the user is redirected to the login page
                    }}
                }} catch (error) {{
                    console.error('Erreur:', error);
                }}
            }}

            // Calling the login function to make sure the value is correct
            postData(url);
        }} else {{
            console.log("Le cookie 'login' n'existe pas.");
            window.location.href = '{config.SERVER_IP}:{config.SERVICE_PORT}';
            // The user is redirected to the login page if there's no login cookie
        }}
    </script>
    <body>
        <h1>Panel de gestion</h1>
        <label for="duree_shutdown">Eteindre dans:</label>

        <select name="duree_shutdown" id="shutdown-select">
            <option value="NOW">Maintenant</option>
            <option value="5M">5 minutes</option>
            <option value="15M">15 minutes</option>
            <option value="30M">30 minutes</option>
            <option value="1H">1 heure</option>
            <option value="3H">3 heures</option>
            <option value="6H">6 heures</option>
            <option value="12H">12 heures</option>
            <option value="24H">24 heures</option>
        </select>
        <button id="button_shutdown">Eteindre</button>
        <br>
        <label for="duree_reboot">Redémarrer dans:</label>

        <select name="duree_reboot" id="reboot-select">
            <option value="NOW">Maintenant</option>
            <option value="5M">5 minutes</option>
            <option value="15M">15 minutes</option>
            <option value="30M">30 minutes</option>
            <option value="1H">1 heure</option>
            <option value="3H">3 heures</option>
            <option value="6H">6 heures</option>
            <option value="12H">12 heures</option>
            <option value="24H">24 heures</option>
        </select>
        <button id="button_reboot">Redémarrer</button>
    </body>
    <script>
        const buttonShutdown = document.getElementById("button_shutdown");
        const buttonReboot = document.getElementById("button_reboot");
        
        // Function executed when the user clicks on the Shutdown button
        buttonShutdown.onclick = function(){{
            let shutdown_value = document.getElementById("shutdown-select").value;
            
            // Function to send the shutdown request
            async function requestShutdown(url = '') {{
                try {{
                    // Configuration de la requête
                    const response = await fetch(url, {{
                        method: 'POST',
                        headers: {{
                            'Authorization': `${{loginCookieValue}}`,
                            'ShutdownType': `${{shutdown_value}}`
                        }}
                    }});
                }} catch (error) {{
                    console.error('Erreur:', error);
                }}
            }}

            // Calling the function to make the shutdown request
            requestShutdown('{config.SERVER_IP}:{config.SERVICE_PORT}/shutdown');
        }}
         
        // Function executed when the user clicks on the Reboot button
        buttonReboot.onclick = function(){{
            let reboot_value = document.getElementById("reboot-select").value;
            
            // Function to send the reboot request
            async function requestReboot(url = '') {{
                try {{
                    const response = await fetch(url, {{
                        method: 'POST',
                        headers: {{
                            'Authorization': `${{loginCookieValue}}`,
                            'RebootType': `${{reboot_value}}`
                        }}
                    }});
                }} catch (error) {{
                    console.error('Erreur:', error);
                }}
            }}

            // Calling the function to make the Reboot request
            requestReboot('{config.SERVER_IP}:{config.SERVICE_PORT}/reboot');
        }}
    </script>
</html>
"""
