#!/bin/usr/python3
# -*- coding: utf-8 -*-
#
# mailman.py
# version: 1.0.2
# build: alpha
#
# Author:	Ungerböck Michele
# Github:	github.com/mikeunge
# Company:	GEDV GmbH
#
# All rights reserved.
#
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Get the configuration.
from config import mail, config


class Mail:
    def __init__(self):
        """
            Initialize and define the config items.
        """
        self.smtp_server = config['server']['smtp_server']
        self.smtp_port = int(config['server']['smtp_port'])     # MUST be an integer.
        self.send_mail = mail['sender']['email']
        self.send_name = mail['sender']['name']
        self.send_pass = mail['sender']['password']
        self.rec_mail = mail['receiver']['email']
        self.rec_name = mail['receiver']['name']
        self.subject = config['mail']['subject']
        self.prefix = config['mail']['prefix']


    def create_message(self):
        """
            Get all the information the message needs and construct it.
            Returns the actual message.
            ! Plain-Text only !
        """
        # Create the message and the email headers.
        message = MIMEMultipart("alternative")
        message["Subject"] = f"{self.prefix} - {self.subject}"
        message["From"] = self.send_name
        message["To"] = self.rec_mail

        # Create the mail content.
        text = f"""\
            Status,\n
            sender: {self.send_name}\n
            status: {self.send_mail}
        """
        # Define the MimeTexts (plain/html)
        plain_text = MIMEText(text, "plain")
        # Attach the text's to the email message.
        message.attach(plain_text)
        return message


    def send(self):
        """
            This function connects to the server and sends the e-mail.
        """
        message = self.create_message()
        # Create an ssl connection.
        context = ssl.create_default_context()
        # TODO: New/Better error handling..
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as conn:
            try:
                conn.ehlo()  # Can be omitted
                conn.starttls(context=context)
                conn.ehlo()  # Can be omitted
                
                # Connect to the mail server.
                conn.login(self.send_mail, self.send_pass)
                # Send the email.
                conn.sendmail(self.send_mail, self.rec_mail, message.as_string())
            except Exception as ex:
                print(f"Something went wrong while sending the email.. Error: {ex}")
            finally:
                print("Ende")


if __name__ == '__main__':
    # TODO: implement the logging handler..
    # Get logging information, create the logger.
    #log_file = config['logging']['file']
    #log_level = config['logging']['level']
    mail = Mail()
    mail.send()
    # TODO: Exit with errors, redo the actual handling and exiting proccess.
    exit()