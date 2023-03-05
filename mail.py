import os
import random
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
from dotenv import load_dotenv

server_name = 'smtp.gmail.com'
port = 465

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")


# setting variable for E-mail
def calling_mail(receiver_email, name, subject, folder_path, random_file):
    # Create a multipart message object
    msg = MIMEMultipart('alternative')
    msg['Subject'] = (subject + ' {}'.format(name.upper()))
    msg['From'] = sender
    msg['To'] = receiver_email
    # reading the file_content
    source = os.path.join(current_dir, folder_path)
    with open(os.path.join(source, random_file), 'r') as f:
        content = f.read().split("==html==")
        f.close()
        text = content[0]
        message_content = (content[1].replace('%s', name))

        # Adding the image
        image_path = current_dir / 'Templates' / 'images' / 'guinea-pig.jpg'
        # image_list = os.listdir(image_path)
        # image = random.choice(image_list)
        with open(image_path, "rb") as img_data:
            img = img_data.read()
            img_data.close()
        image = MIMEImage(img)
        image.add_header('Content-ID', '<image1>')
        msg.attach(image)

    # Add the plain text and HTML content to the message
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(message_content, 'html')
    msg.attach(part1)
    msg.attach(part2)


    # sending the email
    if server:
        send_mail(server, sender, receiver_email, msg.as_string())


# server side configuration
def smtp_login(server_name, port, sender, password_email):
    try:
        print(f'{datetime.now()} --> server login has been initiated')

        server = smtplib.SMTP_SSL(server_name, port)
        server.login(sender, password_email)
        return server
    except Exception as e:
        print("Error occurred while logging in: ", e)
        return None


def send_mail(server, sender, receiver_email, message_content):
    try:
        server.sendmail(sender, receiver_email, message_content)
        print(f'{datetime.now()} --> Email sent to {receiver_email}')
    except Exception as e:
        print(e)


def smtp_logout(server):
    server.quit()
    print("{} --> Logged out from the server".format(datetime.now()))


server = smtp_login(server_name, port, sender, password_email)
