import imaplib, re
import email
from email.header import decode_header

pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')

def parse_uid(data):
    match = pattern_uid.match(data)
    return match.group('uid')

username = "my email"
password = "my password"

imap = imaplib.IMAP4_SSL("imap.gmail.com")

imap.login(username, password)

status, messages = imap.select("INBOX")

N = 6

messages = int(messages[0])



for i in range(messages, messages-N, -1):
    data, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])

            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):

                subject = subject.decode()
            print("=" * 100)
            from_ = msg.get("From")
            print("Subject:", subject)
            print("From:", from_)
            print("=" * 100)
            if "YouTube" in from_:
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

                    msg_uid = parse_uid(data[0])
                    result = imap.uid('COPY', msg_uid, 'Trash')

                    if result[0] == 'OK':
                        mov, data = imap.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')
                        imap.expunge()

imap.close()
imap.logout()
