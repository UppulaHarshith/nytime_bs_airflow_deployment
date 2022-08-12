"""
Send emails using SMTP Server

Author : Harshith Uppula
Date created: 08/09/2022
Date modified: 08/11/2022
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import ast

def send_email(final_str, receiver):

    """
        sending best sellers weekly emails
        :final_str : The bestsellers string which is sent in the email
        :receiver : list of email addresses of recipients

    """


    ctx = ssl.create_default_context()
    password = "mhuykeoupfpbruet"    # App password goes here
    sender = "harshithu888@gmail.com"    # Sender e-mail address
    receiver = ast.literal_eval(receiver) # Recipient's address

    for recipient in receiver:
        message = MIMEMultipart("alternative")
        message["Subject"] = "NYTimes Bestsellers"
        message["From"] = sender
        message["To"] = recipient
        

        plain = f"""
        Checkout the Latest Bestsellers from NYTimes

        {final_str}

        Regards,
        Uppula Harshith,
        Data Engineer Aspirant
        San Jose State University
        """

        message.attach(MIMEText(plain, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())