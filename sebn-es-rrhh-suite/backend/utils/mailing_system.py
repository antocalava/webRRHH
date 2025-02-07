import base64
from email import base64mime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import smtplib


def send_email(addressee, subject, message):
    smtp_server = '130.30.2.7'
    smtp_port = 25

    sender = 'sebnessuite@sebn.com'

    additional_message = "Sumitomo Electric Bordnetze SE<br/>Sucursal Ibérica<br/>Polígono Iruregaña 71, 2º izda.<br/>E-31195 Aizoain<br/>España"

    mail = MIMEMultipart()
    mail['From'] = sender
    mail['To'] = addressee
    mail['Subject'] = subject

    html_message = f"""\
    <html>
    <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background-color: #2E008B;
            color: #fff;
            padding: 20px;
            text-align: center;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
        .content {{
            padding: 20px;
        }}
        .content p {{
            margin-bottom: 15px;
        }}
        .content img {{
            display: block;
            margin: 0 auto;
            max-width: 100%;
        }}
        </style>
    </head>
    <body>
        <div class="container">
        <div class="header">
            <h2>{subject}</h2>
        </div>
        <div class="content">
            <p>{message}</p>
            <p style="margin-top:160px">{additional_message}</p>
            <img src="cid:attached_image">
        </div>
        </div>
    </body>
    </html>
    """

    mail.attach(MIMEText(html_message, 'html'))

    attached_image = os.path.join(os.getcwd(), "static", "images", "banner.png")

    with open(attached_image, 'rb') as file:
        data_image = file.read()
    mime_image = MIMEImage(data_image)
    mime_image.add_header('Content-ID', '<attached_image>')
    mail.attach(mime_image)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(sender, addressee, mail.as_string())
        server.quit()
        
    except Exception as e:
        print("Error sending e-mail:", e)
        return False
    return True


#TODO: test_send_feedback_email
def send_feedback_email(sender, tag, subject, title, message):
    smtp_server = '130.30.2.7'
    smtp_port = 25

    additional_message = "Sumitomo Electric Bordnetze SE<br/>Sucursal Ibérica<br/>Polígono Iruregaña 71, 2º izda.<br/>E-31195 Aizoain<br/>España"
    addressees = "cristina.lopez@sebn.com, antonio.calahorra@sebn.com"
    in_copy = f"{sender}, cristina.lopez@sebn.com" #"SEBN.SCM-SCA-Everyone-ES@sebn.com" #TODO: DESCOMENTAR EN PROD (cambiar email cris por el comentado)
        
    mail = MIMEMultipart()
    mail['From'] = sender
    mail['To'] = addressees
    mail['Subject'] = subject
    mail['Cc'] = in_copy
    
    tag_color = "#D7D8D9" #default, grey for "OTHER" tag
    if tag == "BUG": tag_color = "#b61e1e" #red
    elif tag == "MOD": tag_color = "#e9a30d" #yellow
    elif tag == "ADD": tag_color = "#47a51c" #green 
    elif tag == "QNA": tag_color = "#9134c7" #purple 
    elif tag == "INF": tag_color = "#007bff" #blue

    html_message = f"""\
    <html>
    <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background-color: {tag_color};
            color: #fff;
            padding: 20px;
            text-align: center;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
        .content {{
            padding: 20px;
            margin-bottom: 10px;
        }}
        .content p {{
            margin-bottom: 15px;
        }}
        .content img {{
            display: block;
            margin: 0 auto;
            max-width: 100%;
        }}
        </style>
    </head>
    <body>
        <div class="container">
        <div class="header">
            <h2>{title}</h2>
        </div>
        <div class="content">
            <p>{message}</p>
            <p style="margin-top:160px">{additional_message}</p>
            <img src="cid:attached_image">
        </div>
        </div>
    </body>
    </html>
    """

    mail.attach(MIMEText(html_message, 'html'))

    attached_image = os.path.join(os.getcwd(), "static", "images", "banner.png")

    with open(attached_image, 'rb') as file:
        data_image = file.read()
    mime_image = MIMEImage(data_image)
    mime_image.add_header('Content-ID', '<attached_image>')
    mail.attach(mime_image)

    try:
        recipients = addressees.split(", ")
        for in_copy_email in in_copy.split(", "): recipients.append(in_copy_email)
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(sender, recipients, mail.as_string())
        server.quit()
        
    except Exception as ex:
        print("ERROR sending e-mail: " + str(ex))
        return False
    return True