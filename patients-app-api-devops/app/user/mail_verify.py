from re import T
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.contrib.auth.tokens import default_token_generator
from base64 import urlsafe_b64decode, urlsafe_b64encode

from django.contrib.auth import (
    get_user_model,
)

import json

from django.conf import settings
import datetime,time

username=''
password=''


def get_email_token(email = None) :
    s_time = time.time()
    send_data = {"email" : email,"expired" : str(s_time)}
    data = json.dumps(send_data)

    confirmation_token = urlsafe_b64encode((data).encode('utf-8'))
    token = confirmation_token.decode("utf-8")
    return token

def send_mail(token=None,text='Email_body',subject='Hello word',from_email='',to_emails=[]):
    assert isinstance(to_emails,list)
    msg=MIMEMultipart('alternative')
    msg['From']=from_email
    msg['To']=", ".join(to_emails)
    msg['Subject']=subject
    txt_part=MIMEText(text,'plain')
    msg.attach(txt_part)
    
    url = settings.VALIDATION_URL + token

    html_part = MIMEText(f"<p>Please click to verify</p><h1><link>{url}</link></h1>", 'html')
    msg.attach(html_part)
    msg_str=msg.as_string()
    
    server=smtplib.SMTP(host=settings.EMAIL_HOST,port=settings.EMAIL_PORT)
    print(url)
    server.ehlo()
    server.starttls()
    print(url)
    server.login(username,password)
    print(url)
    server.sendmail(from_email,to_emails,msg_str)
    server.quit()



def verify_token(email_token):
        data = urlsafe_b64decode(email_token).decode("utf-8")
        data = json.loads(data)
        email = data['email']
        sended_time = (float)(data['expired'])

        current_time = time.time()
        delta_time = current_time - sended_time


        if(delta_time > settings.EXPIRE_TIME):
                 return False
        try:
            users = get_user_model().objects.filter(email = email)
            for user in users:
                    user.is_active = True
                    user.save()
                    return True
        except BaseException:
            pass
        return False


