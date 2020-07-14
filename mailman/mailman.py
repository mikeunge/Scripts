#!/bin/usr/python3
# -*- coding: utf-8 -*-
#
# mailman.py
# version: 1.0.3
# build: alpha
#
# Author:	Ungerböck Michele
# Github:	github.com/mikeunge
# Company:	GEDV GmbH
#
# All rights reserved.
#
import os
import sys
import ssl
import logging
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
# Get the configuration.
from config import mail, config


class Mail:
    def __init__(self, template, status):
        """
            Initialize and define the config items.
        """
        self.status = status
        self.template = template    # Template to use.
        self.smtp_server = config['server']['smtp_server']
        self.smtp_port = int(config['server']['smtp_port'])     # MUST be an integer.
        self.send_mail = mail['sender']['email']
        self.send_name = mail['sender']['name']
        self.send_pass = mail['sender']['password']
        self.rec_mail = mail['receiver']['email']
        self.rec_name = mail['receiver']['name']
        self.subject = config['mail']['subject']
        self.prefix = config['mail']['prefix']
        self.attachments = mail['attachments']


    def check_placeholder(self, arg):
        """
            Check if a placeholder is used or not.
        """
        defined_placeholder = {
            "status": self.status,
            "name": self.send_name
        }
        # Check if the length of the argument is larger then 2.
        # If it's 1, it doesn't contain a placeholder; if it's 2, it contains the placeholder trigger but isn't actually a placholder.
        #   correct: %status%
        #   wrong(2): %status
        s_arg = arg.split("%")
        if len(s_arg) > 2:
            for x in defined_placeholder:
                if x == s_arg['1']:
                    return str(defined_placeholder[x])
        return False


    def create_message(self):
        """
            Get all the information the message needs and construct it.
            Returns the actual message.
            ! Plain-Text only !
        """
        # TODO: Need to move this section -> serialize() ?
        ######
        tmp_prefix = self.check_placeholder(self.prefix)
        if tmp_prefix != False:
            self.prefix == tmp_prefix
            
        # Create the message and the email headers.
        message = MIMEMultipart("alternative")
        message["Subject"] = f"{self.send_name} - {self.prefix} - {self.subject}"
        message["From"] = self.send_name
        message["To"] = self.rec_mail
        attachments = []    # All attachment (paths) are going to be stored in here.

        # Loop over the defined attachments in the config.py file.
        # It checks if
        #   1) the path exists.
        #   2) the defined path is an actual readable file.
        #   3) fil is not larger than defined size.
        for x in self.attachments:
            if not os.path.exists(self.attachments[x]):
                logger.error(f"Attachment [{self.attachments[x]}] does not exist!")
                next
            if not os.path.isfile(self.attachments[x]):
                logger.error(f"Attachment [{self.attachments[x]}] is not a file!")
                next
            if not os.stat(self.attachments[x]).st_size < int(config['max_attachment_size']):
                logger.error(f"Attachment [{self.attachments[x]}] size is too big ({self.attachments[x].st_size}B)")
                next
            attachments.append(self.attachments[x])

        # Create the mail content.
        if self.template != None:
            # Read the template and set it as mail-text.
            with open(self.template, 'a') as temp:
                text = temp
        else:
            text = "No template defined.."

        # Define the MimeTexts (plain/html)
        mail_text = MIMEText(text, "plain")
        # Attach the text's to the email message.
        message.attach(mail_text)

        # Add the attachments to the message
        for file in attachments:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                    encoders.encode_base64(msg)
                    msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                    message.attach(msg)
            except Exception as ex:
                logger.error(f"Unable to open one of the attachments. Error: {ex}")
        return message


    def send(self):
        """
            This function connects to the server and sends the e-mail.
        """
        message = self.create_message()     # Create the message to send.
        context = ssl.create_default_context()  # Establish an SSL connection.
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as conn:
            # TODO: Better error handling..
            #       Get more/detailed errors.
            try:
                conn.ehlo()
                conn.starttls(context=context)
                conn.ehlo()
                # Connect to the mail server.
                conn.login(self.send_mail, self.send_pass)
                conn.sendmail(self.send_mail, self.rec_mail, message.as_string())
                conn.close()
                logger.info("Info successfully sent!")
            except Exception as ex:
                logger.fatal(f"Something went wrong while sending the email.. Error: {ex}")
                return False
        return True

# Function for creating the logger and setting the correct log_level.
def setup_logger(level, path):
	# Change the logging format below..
	log_format = "%(asctime)s - %(levelname)s - %(message)s"
	try:
		# Check the different cases, default: DEBUG
		if level.upper() == "DEBUG":
			logging.basicConfig(filename=path, level=logging.DEBUG, format=log_format)
		elif level.upper() == "INFO":
			logging.basicConfig(filename=path, level=logging.INFO, format=log_format)
		elif level.upper() == "WARNING":
			logging.basicConfig(filename=path, level=logging.WARNING, format=log_format)
		elif level.upper() == "ERROR":
			logging.basicConfig(filename=path, level=logging.ERROR, format=log_format)
		else:
			logging.basicConfig(filename=path, level=logging.DEBUG, format=log_format)
		return logging.getLogger()
	except Exception as ex:
		print(f"Could not setup the logger, exiting the program.\nError: {ex}")
		sys.exit(1)
    

if __name__ == '__main__':
    # Setup the logger.
    logger = setup_logger(config['logging']['level'], config['logging']['path'])

    # Check if a argument was passed.
    # Map the argument with the correct template.
    try:
        status = sys.argv[1]
        template_key = status
        logger.info(f"Passed argument: {status}")
    except IndexError as ix:
        template_key = config['template_default']   # load the defined default from config.
        logger.warning(f"No argument found, fallback to default: {template_key}")

    # If special cases are needed/wanted, extend the dict with a key and define the template path/file.
    defined_templates = {
        "success": f"{config['template_path']}/assets/success.template",
        "warning": f"{config['template_path']}/assets/warning.template",
        "error": f"{config['template_path']}/assets/error.template",
        "default": f"{config['template_path']}/assets/error.template"      # default/fallback template
    }

    # Check if the case exists.
    if template_key in defined_templates:
        template_to_use = defined_templates[template_key]
    else:
        # The template doesn't exist, define the default template.
        logger.error("Template doesn't exist!")
        template_to_use = defined_templates['default']
    # Make sure the template to load exists!
    if not os.path.exists(template_to_use):
        logger.error("Template not found!")
        template_to_use = None

    mail = Mail(template_to_use, status)
    if mail.send():
        sys.exit(0)
    else:
        sys.exit(1)
