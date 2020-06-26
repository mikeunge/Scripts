#!/bin/usr/python3
# -*- coding: utf-8 -*-
#
# mailman.py
# version: 1.0.0
#
# Author:	Ungerböck Michele
# Github:	github.com/mikeunge
# Company:	GEDV GmbH
#
# All rights reserved.
import smtplib
import ssl
from credentials import credentials as cred
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():
    # Create the message and the email headers.
    message = MIMEMultipart("alternative")
    message["Subject"] = "IP address has changed!"
    message["From"] = cred["sender_name"]
    message["To"] = cred["receiver_email"]

    # Create the mail content.
    text = f"""\
        Status,\n
        sender: {cred["sender_email"]}\n
        status: {cred["sender_name"]}
    """
    html = f"""\
    <html>
        <body>
            <p>Status,<br>
            sender: {cred["sender_email"]}<br>
            sender: {cred["sender_name"]}<br>
            </p>
        </body>
    </html>
    """

    # Define the MimeTexts (plain/html)
    plain_text = MIMEText(text, "plain")
    html_text = MIMEText(html, "html")

    # Attach the text's to the email message.
    message.attach(plain_text)
    message.attach(html_text)

    # Create an ssl connection.
    context = ssl.create_default_context()
    with smtplib.SMTP(cred["mail_server"], cred["port"]) as conn:
        try:
            conn.ehlo()  # Can be omitted
            conn.starttls(context=context)
            conn.ehlo()  # Can be omitted
            
            # Connect to the mail server.
            conn.login(cred["sender_email"], cred["password"])
            # Send the email.
            conn.sendmail(cred["sender_email"], cred["receiver_email"], message.as_string())
        except Exception as ex:
            print(f"Something went wrong while sending the email.. Error: {ex}")
        finally:
            print("Ende")


if __name__ == '__main__':
    main()