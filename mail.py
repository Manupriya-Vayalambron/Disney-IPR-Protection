import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime, timedelta

# Function to send email
def send_ipr_violation_email(to_email, subject, body):
    # Email sender credentials (Use a secure method to handle email passwords)
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"  # Use App Password if using Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Prepare email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Setup the server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()

        print(f"Email sent successfully to {to_email}")

    except Exception as e:
        print(f"Error sending email: {e}")


# Function to generate and send the IPR violation email
def handle_ipr_violation(violator_email, violated_website):
    subject = "URGENT: IPR Violation Notification"
    
    # Set the time span for resolution (1 day)
    resolution_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    
    # Body of the email
    body = f"""
    Dear Sir/Madam,

    We have detected an IPR violation on your website/content page. You are hereby requested to 
    take down the violating content within the next 24 hours. 

    Failure to do so will result in your website or the content page being banned.

    Deadline for takedown: {resolution_time}

    Please address this issue immediately to avoid further legal actions.

    Regards,
    Google Solutions Challenge Team
    """

    # Send email to violator (or violated website)
    send_ipr_violation_email(violator_email, subject, body)
    
    # Optionally, send an email to the violated website (if you want them informed as well)
    if violated_website:
        violated_website_email = violated_website  # Use the violated website’s admin contact email
        send_ipr_violation_email(violated_website_email, subject, body)

# Example usage:
violator_email = "violator_email@example.com"  # Email of the violator
violated_website_email = "violated_website@example.com"  # Email of the violated website (optional)

# Handle IPR violation
handle_ipr_violation(violator_email, violated_website_email)
