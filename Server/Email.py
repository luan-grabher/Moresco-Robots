#send email to and json_return to 
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib
import ssl


def send_email(email, html, subject = 'Moresco Robot'):
    #get email config from 'email_config.ini'
    mailconfig = configparser.ConfigParser()
    mailconfig.read('email_config.ini')

    #get username and password from section 'gmail' of 'email_config.ini'
    username = mailconfig['gmail']['username']
    password = mailconfig['gmail']['password']

    print('Enviando e-mail para ' + email)
    print('Mensagem: ' + html)
    print('------------------------------------------------------')
    print('Username: ' + username)
    print('Password: ' + password)

    try:
        #create email
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(html, 'html'))
        
        text = msg.as_string()


        server = smtplib.SMTP('smtp.gmail.com','587')
        server.ehlo()
        #create context for ssl
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.ehlo()
        server.login(username, password)
        server.sendmail(username, email, text)
        server.quit()

        print('Email enviado para ' + email)
    except Exception as e:
        print('Erro ao enviar e-mail para ' + email)
        print(e)