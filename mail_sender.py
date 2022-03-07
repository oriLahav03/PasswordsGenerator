import random
import re
import smtplib
import ssl
import string

import os

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets

from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self):
        load_dotenv()
        self.my_mail = os.getenv('EMAIL')  # TODO: 'Enter your email Here'
        self.my_mail_password = os.getenv('PASSWORD')  # TODO: 'Enter your email's password Here'

    @staticmethod
    def check_email(receiver_mail):
        """
        The function checks if the receiver email is valid email address.
        :param receiver_mail: The receiver email address.
        :return: None (exit if Invalid email).
        """

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # Checks if the email format is valid.
        if not re.search(regex, receiver_mail):  # If it's not valid:
            raise Exception('Invalid email address!')

    @staticmethod
    def check_length(password_length):
        """
        The function checks if the length of the password wanted is valid (number).
        :param password_length: The chosen length of the password.
        :return: The length of the password / exit if Invalid length.
        """

        try:
            return int(password_length)
        except ValueError as e:
            raise Exception('Invalid password length (Only numbers allowed!)') from e

    def get_info_from_user(self, email, purpose, length):
        """
        The function takes all inputs from user.
        :return: None
        """

        self.check_email(email)
        int_length = self.check_length(length)
        self.send_mail(email, purpose, int_length)

    def send_mail(self, receiver_mail, password_purpose, password_length):
        """
        The function send the email message to the receiver.
        :param receiver_mail: The email to send to.
        :param password_purpose: The title / purpose of the password.
        :param password_length: The length of the password.
        :return: None
        """
        # Generate new random password.
        new_password = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(password_length))

        # The receiver username (before the '@' of the email address).
        receiver_name = receiver_mail.split('@')[0]

        message = MIMEMultipart("alternative")
        message["Subject"] = f"{password_purpose}'s Password"
        message["From"] = self.my_mail
        message["To"] = receiver_mail

        html = f"""\
        <html>
          <body>
            <p>Hey {receiver_name}!\n<br>
               Here is your password for {password_purpose} with length of {password_length}: \n
               {new_password}<br>
               <a href="https://github.com/oriLahav03">Creator Of This Code</a> 
            </p>
          </body>
        </html>
        """

        minetext = MIMEText(html, "html")
        message.attach(minetext)

        context = ssl.create_default_context()

        try:
            QMessageBox.about(QtWidgets.QWidget(), 'Success!', 'sending...\nmight take a few seconds!')
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.my_mail, self.my_mail_password)
                server.sendmail(
                    self.my_mail, receiver_mail, message.as_string()
                )
            raise Exception('Email send successfully!')
        except smtplib.SMTPAuthenticationError as e:
            raise Exception('Incorrect email or password!') from e
