import os

import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

#--------- FOR Amazon SES
import boto3
from botocore.exceptions import ClientError
#--------- 

def basicEmailwithAttachement(body = "Body_of_the_mail", subject = "Subject", toEmail = "RecepientEmail@gmail.com", fromEmail = "YourEmail@gmail.com", path = r'C:\Data', filename="excelToSend.xlsx") -> None:
    """
    Args:
        body        (str): body of email.
        subject     (str): subject of email.
        fromEmail   (str): sender.
        toEmail     (str): recipient.
        path        (str): path to file
        filename    (str): file name with format.

    Returns:
        None: no output given.
        
    Description:
        Send an email.
    """
    server_name = 'smtpEmailServerAdress'
    
    #Create Message Body
    messageObject = MIMEMultipart() 
    messageObject['From'] = fromEmail 
    messageObject['To'] = toEmail 
    messageObject['Subject'] = subject
    messageObject.attach(MIMEText(body, 'plain')) 

    #Add attachment
    attachment = open(path+"\\"+filename, "rb")

    #Convert and add file info to message
    #Subclass of message (part of message)
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

    #Attach file
    messageObject.attach(p) 

    #Send an email
    s = smtplib.SMTP(server_name) 
    messageBody = messageObject.as_string() 
    s.sendmail(fromEmail, toEmail, messageBody) 
    s.quit()

    print("OK")

def sesEmail(body, subject, toEmail = "michal.debosz2@sp.woodplc.com", fromEmail = "registeredSESEmail@google.com") -> None:
    """
    Args:
        body        (str): body of email.
        subject     (str): subject of email.
        fromEmail   (str): sender.
        toEmail     (str): recipient.

    Returns:
        None: no output given.
        
    Description:
        Send an email via Amazon SES.
    """
    CHARSET = "UTF-8"
    ses_client = boto3.client('ses',
                        region_name             =   os.environ["SERVER"],
                        aws_access_key_id       =   os.environ["USER"],
                        aws_secret_access_key   =   os.environ["PASSWORD"],
                        aws_session_token       =   ""
    )
    response = ses_client.send_email(
        Destination={
            'ToAddresses': [
                toEmail,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': body,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': subject,
            },
        },
        Source=fromEmail,
    )
    print("OK")
