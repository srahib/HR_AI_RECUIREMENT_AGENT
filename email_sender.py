import smtplib

from email.message import EmailMessage

from config import *


def send_excel_report(filename):

    msg = EmailMessage()

    msg["Subject"] = "Top Candidates Report"

    msg["From"] = EMAIL_ADDRESS

    msg["To"] = HR_EMAIL

    msg.set_content(
        "Please find the attached Top Candidates Excel Report."
    )

    with open(filename, "rb") as f:

        file_data = f.read()

        file_name = f.name

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        smtp.send_message(msg)

    return {
        "message": "Excel Report Sent Successfully"
    }