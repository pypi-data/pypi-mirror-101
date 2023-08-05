def writeConfig():
    with open("mailConfig.py", "w") as f:
        f.write('cfgmail = {\n"username" : "Your Username",\n"password" : "Your Password",\n"server" : "Your Server",\n"port" : "Your Port"\n}')