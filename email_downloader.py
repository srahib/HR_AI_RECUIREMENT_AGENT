import os

DOWNLOAD_FOLDER = "resumes"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def download_attachments(msg):

    downloaded_files = []

    for part in msg.walk():

        content_disposition = str(part.get("Content-Disposition"))

        if "attachment" not in content_disposition:
            continue

        filename = part.get_filename()

        if not filename:
            continue

        filename = os.path.basename(filename)

        if not (
            filename.lower().endswith(".pdf")
            or filename.lower().endswith(".docx")
        ):
            continue

        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(part.get_payload(decode=True))

        downloaded_files.append(filepath)

    return downloaded_files