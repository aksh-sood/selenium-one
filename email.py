import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email():
    sender="" # your email id
    password="" #your password
    reciever="" #recievers email id
    msg=MIMEMultipart()
    msg["From"]=sender
    msg["To"]=reciever
    msg["Subject"]="Movies Result From Bot"
    body="hey this is the attchment dontaining the data that i collected from the web "
    msg.attach(MIMEText(body,"plain"))
    attachment=open("moviesdata.csv","rb")
    p=MIMEBase("application","octect-stream")
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment; filename=moviesdata.csv")
    msg.attach(p)
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender,password)
    server.send_message(msg)
    server.quit()
