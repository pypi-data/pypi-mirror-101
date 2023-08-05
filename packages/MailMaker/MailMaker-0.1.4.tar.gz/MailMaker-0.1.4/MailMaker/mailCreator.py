import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from MailMaker.createConfig import writeConfig
import os
import traceback


class eMail:
    def __init__(self, to=[], subject="TestMail", body="TestMail", attachments=[], bodytype='plain'):
        if (len(to) == 0) | (type(to) != list):
            raise KeyError("to has to be a non empty list")
        self.an = to
        self.betreff = subject
        self.text = body
        self.anhaenge = attachments
        self.bodytype = bodytype

        if not os.path.exists("mailConfig.py"):
            writeConfig()
            from mailConfig import cfgmail
        else:
            from mailConfig import cfgmail



    @property
    def username(self):
        return cfgmail['username']
    @property
    def password(self):
        return cfgmail['password']
    @property
    def server(self):
        return cfgmail['server']
    @property
    def port(self):
        return cfgmail['port']


    def send(self):
        try:
            for tomail in self.an:
                body = self.text

                msg = MIMEMultipart()
                msg["From"] = self.username
                msg["To"] = tomail
                msg["Subject"] = self.betreff
                msg.attach(MIMEText(body, self.bodytype))

                if len(self.anhaenge) != 0:
                    for pfad in self.anhaenge:
                        filename = pfad.split("/")[-1]

                        attachment = open(pfad, "rb")
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("content-disposition", f"attachment; filename = {filename}")
                        msg.attach(part)

                text = msg.as_string()
                server = smtplib.SMTP(self.server, self.port)
                server.starttls()
                server.login(self.username, self.password)

                server.sendmail(self.username, tomail, text)
                server.quit()

        except:
            raise
