##
## MALEK PROJECT, 2023
## scrapping_wttj
## File description:
## send_mail
##

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

def send_crash(email, text):
    msg = MIMEMultipart()
    msg['From'] = "jean-marie.scofield@outlook.com"
    msg['To'] = email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Reporting Candidat"
    msg.attach(MIMEText("Attention votre programme a crash\n" + text + "\n"))
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login("jean-marie.scofield@outlook.com", "Futuramax77350FG")
    server.sendmail("jean-marie.scofield@outlook.com", email, msg.as_string())
    server.close()

