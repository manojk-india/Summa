import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = "smtp.office365.com"
port = 587
sender_email = "your_email@yourcompany.com"
receiver_email = "recipient@yourcompany.com"
password = "your_password"  # Use a secure method to store/retrieve

subject = "Ingestion Complete"
body = "The ingestion process has finished successfully."

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

with smtplib.SMTP(smtp_server, port) as server:
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
