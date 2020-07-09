import imaplib, re
import email
from email.header import decode_header
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
from pynput.keyboard import Key, Controller, Listener
import os

keyboard = Controller()

username = "<insert email here>"
password = "<insert password here>"

imap = imaplib.IMAP4_SSL("imap.gmail.com")

imap.login(username, password)

status, messages = imap.select("INBOX")

N = 1

messages = int(messages[0])
num = 1

def delete_message():
    imap.select(mailbox='Inbox', readonly=False)
    resp, items = imap.search(None, 'All')
    email_ids = items[0].split()
    latest_email_id = email_ids[-1]  # Assuming that you are moving the latest email.

    resp, data = imap.fetch(latest_email_id, "(UID)")
    msg_uid = parse_uid(data[0])

    result = imap.uid('COPY', msg_uid, 'Trash')

    if result[0] == 'OK':
        mov, data = imap.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')
        imap.expunge()


def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("Alaska : ", output)

    toSpeak = gTTS(text=output, lang='en', slow=False)
    # saving the audio file given by google text to speech
    file = str(num) + ".mp3"
    toSpeak.save(file)

    # playsound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)

def driver_code():
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
                assistant_speaks("subject is " + subject)
                print("From:", from_)
                assistant_speaks("From " + from_)
                print("=" * 100)
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

    imap.close()
    imap.logout()

if __name__ == '__main__':
    try:
        driver_code()
        yoink = input("Would you like to delete the message (y/n)? ")
        if yoink == "y":
            try:
                delete_message()
            except:
                assistant_speaks("An error occurred, please try again")
    except:
        assistant_speaks("An error occurred, please try again")

