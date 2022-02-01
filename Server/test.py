#configparser
import configparser
import ssl

#get gmail.username and gmail.password from 'email_config.ini'
config = configparser.ConfigParser()
config.read('email_config.ini')
gmail_username = config['gmail']['username']
gmail_password = config['gmail']['password']

#Print "Using gmail username: " + gmail_username
print("Using gmail username: " + gmail_username)
#Print "Using gmail password: " + gmail_password
print("Using gmail password: " + gmail_password)

#test login on SMTP server
import smtplib
server = smtplib.SMTP('smtp.gmail.com','587')
server.ehlo()
#create context for ssl
context = ssl.create_default_context()
server.starttls(context=context)
server.ehlo()
server.login(gmail_username, gmail_password)
server.quit()

