import imaplib
import email
from email.header import decode_header

EMAIL = "YOUR_EMAIL@gmail.com"
PASSWORD = "YOUR_APP_PASSWORD"

IMAP_SERVER = "imap.gmail.com"


def connect_email():

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)

    mail.login(EMAIL, PASSWORD)

    mail.select("INBOX")

    return mail


def get_unread_messages():

    mail = connect_email()

    status, messages = mail.search(None, "UNSEEN")

    email_ids = messages[0].split()

    return mail, email_ids


def fetch_email(mail, email_id):

    status, msg_data = mail.fetch(email_id, "(RFC822)")

    raw_email = msg_data[0][1]

    msg = email.message_from_bytes(raw_email)

    subject, encoding = decode_header(msg["Subject"])[0]

    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")

    sender = msg["From"]

    return msg, subject, sender