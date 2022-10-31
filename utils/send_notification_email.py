import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email_password, send_from, send_to) -> None:
    """Send notification email that data was uploaded"""

    message = MIMEMultipart("alternative")
    message["Subject"] = "Data Uploaded To S3"
    message["From"] = send_from
    message["To"] = send_to

    # Create the plain-text and HTML version of your message
    html = """\
    <html>
      <body>
        <p>Dear User,<br><br>
           New data has been uploaded to the Amazon S3 bucket. <br>
           Please check out the newest version of visualised data: 
           <a href="https://eu-central-1.quicksight.aws.amazon.com/sn/dashboards/2ab4aa4c-c6d9-4e2a-adcb-cd8b19567d76/views/7486a422-f4ec-4737-b309-368bfd8625f4"> Top 5 Countries By The Big Mac Index</a>
        </p><br>

        Best regards,<br>
        Daniel
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(send_from, email_password)
        server.sendmail(send_from, send_to, message.as_string())
