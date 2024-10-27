import smtplib

EMAIL = "XXXXXXXXXXXX"
PASSWORD = "XXXXXXXX "

def send_text(msg):
    destination = "XXXXXXXXXX"
    
    auth = (EMAIL, PASSWORD)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
    msg = msg.encode(encoding='UTF-8')
    server.sendmail(auth[0], destination, msg)
    