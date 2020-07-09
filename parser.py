import imaplib
import email
from email.header import decode_header

username = "your username"
password = "your password"

imap = imaplib.IMAP4_SSL("imap.gmail.com")

imap.login(username, password)

status, messages = imap.select("INBOX")

N = 6

messages = int(messages[0])



for i in range(messages, messages-N, -1):
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])

            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):

                subject = subject.decode()

            from_ = msg.get("From")
            print("Subject:", subject)
            print("From:", from_)
            if "Discord" in from_:
                imap.expunge()
            # if discord spams me, then I am able to delete the message
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        print(body)
                        print("=" * 100)
            else:
                content_type = msg.get_content_type()
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    print(body)
imap.close()
imap.logout()