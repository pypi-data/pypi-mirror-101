def writeConfig():
    server = input("Server: ")
    port = input("Port: ")
    username = input("Username for the mailserver: ")
    password = input("Password for the mailserver: ")

    with open("mailConfig.py", "w") as f:
        f.write(f'cfgmail = {{\n"username" : {username},\n"password" : {password},\n"server" : {server},\n"port" : {port}\n}}')