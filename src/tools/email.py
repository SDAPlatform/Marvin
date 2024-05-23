import sys
import email
import quopri
from pprint import pprint
import json
import os.path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from phi.tools import Toolkit
# from phi.tools.email import EmailTools
from phi.utils.log import logger

from utils import get_size_format

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# SCOPES = ["https://mail.google.com/"]

class MarvinEmailTool(Toolkit):
    def __init__(
        self, 
        # user_email: str,
        # pass_key: str,
        oauth_credential_path: str,
        authorized_token_path: Optional[str] = 'gmail_token.json',
    ):
        # self.user_email = user_email,
        # self.pass_key = pass_key

        print("EMAIL")
        self.creds = None

        if os.path.exists(authorized_token_path):
            self.creds = Credentials.from_authorized_user_file(authorized_token_path, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
              self.creds.refresh(Request())
            else:
              flow = InstalledAppFlow.from_client_secrets_file(
                    oauth_credential_path, SCOPES
              )
              self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(authorized_token_path, "w") as token:
              token.write(self.creds.to_json())

        service = build("gmail", "v1", credentials=self.creds)
        self.gmail_service = service.users()

        super().__init__(name="Email Tool")

        self.register(self.read_emails)

    def read_emails(self, number: int) -> str:
        """Use this function to read al
        
        Args:
            coin (int): The number of emails to read
        
        Returns:
            str: The emails with 
        """
        try:
            messages_res = self.gmail_service.messages()

            messages_id_list = [message['id'] for message in messages_res.list(userId='me').execute()['messages']]

            messages_id_list = messages_id_list[:number]

            if not messages_id_list:
                print("No labels found.")
                return

            self.read_message(messages_id_list[0])


            # messages = [messages_res.get(userId='me', id=message_id, format="full").execute() for message_id in messages_id_list]

            # print(len(messages))

            # snippets = [message['snippet'] for message in messages]
            #
            # bodies = [message['payload'] for message in messages]

            print("BODIES")

            # return snippets, bodies
        except Exception as e:
            return str(e)

    def read_message(self, message_id):
        """
        This function takes Gmail API `service` and the given `message_id` and does the following:
            - Downloads the content of the email
            - Prints email basic information (To, From, Subject & Date) and plain/text parts
            - Creates a folder for each email based on the subject
            - Downloads text/html content (if available) and saves it under the folder created as index.html
            - Downloads any file that is attached to the email and saves it in the folder created
        """
        msg = self.gmail_service.messages().get(userId='me', id=message_id, format='full').execute()
        raw_msg = self.gmail_service.messages().get(userId='me', id=message_id, format='raw').execute().get('raw')
        # parts can be the message body, or attachments
        payload = msg.get("payload")
        headers = payload.get("headers")
        parts = payload.get("parts")
        snippet = msg.get("snippet")
        thread_id = msg.get("threadId")
        #
        folder_name = "email"

        has_subject = False
        sender = ''
        receiver = ''
        subject = ''
        date = ''



        # message = email.\
        # message_from_bytes(urlsafe_b64decode(raw_message))
        #
        # subject = message["Subject"]
        # sender = message["From"]
        # pprint(sender)
        # pprint(quopri.decodestring(sender).decode())
        # return

        if headers:
            # this section prints email basic info & creates a folder for the email
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                if name.lower() == 'from':
                    # we print the From address
                    print("From:", value)
                    sender = value
                if name.lower() == "to":
                    # we print the To address
                    print("To:", value)
                    receiver = value
                if name.lower() == "subject":
                    # make our boolean True, the email has "subject"
                    # has_subject = True
                    # # make a directory with the name of the subject
                    # folder_name = clean(value)
                    # # we will also handle emails with the same subject name
                    # folder_counter = 0
                    # while os.path.isdir(folder_name):
                    #     folder_counter += 1
                    #     # we have the same folder name, add a number next to it
                    #     if folder_name[-1].isdigit() and folder_name[-2] == "_":
                    #         folder_name = f"{folder_name[:-2]}_{folder_counter}"
                    #     elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                    #         folder_name = f"{folder_name[:-3]}_{folder_counter}"
                    #     else:
                    #         folder_name = f"{folder_name}_{folder_counter}"
                    # os.mkdir(folder_name)
                    print("Subject:", value)
                    subject = value
                if name.lower() == "date":
                    # we print the date when the message was sent
                    print("Date:", value)
                    date = value
        # if not has_subject:
        #     # if the email does not have a subject, then make a folder with "email" name
        #     # since folders are created based on subjects
        #     if not os.path.isdir(folder_name):
        #         os.mkdir(folder_name)

        body_res = {
        'text': [],
        'attachments': []
        }
        if payload:
            print("PAYLOAD")
            pprint(len(payload))
            body_res = self.parse_chunk(payload, folder_name, message_id)
        if parts:
            print("PARTS")
            pprint(parts)
            pprint(len(parts))
            print("CALLING PARTS")
            parts_res = self.parse_parts(parts, folder_name, message_id)
            print("RETURNED PARTS")

        body = ''
        return {
            "id": message_id,
            "threadId": thread_id,
            "sender": sender,
            "receiver": receiver,
            "subject": subject,
            "date": date,
            "snippet": snippet,
            "body": "\n".join(body_res['text']),
            "attachments": body_res['attachments']
        }
        print("="*50)

    # Chunk can be a part or the body itself
    def parse_chunk(self, chunk, folder_name, message_id):
        chunk_res = {
            'text': [],
            'attachments': []
        }
        filename = chunk.get("filename")
        mimeType = chunk.get("mimeType")
        body = chunk.get("body")
        data = body.get("data")
        file_size = body.get("size")
        chunk_headers = chunk.get("headers")
        if chunk.get("parts"):
            # recursively call this function when we see that a chunk
            # has chunks inside
            parts_res = self.parse_parts(chunk.get("parts"), folder_name, message_id)
            chunk_res['text'] += parts_res['text']
            chunk_res['attachments'] += parts_res['attachments']
        if mimeType == "text/plain":
            # if the email chunk is text plain
            print("-----------PLAIN TEXT")
            if data:
                text = urlsafe_b64decode(data).decode()
                print(text)
                chunk_res['text'].append(text)
        elif mimeType == "text/html":
            # if the email chunk is an HTML content
            # save the HTML file and optionally open it in the browser
            if data:
                raw_html = urlsafe_b64decode(data).decode()
                clean_body = self.clean_email_body(raw_html).replace("\n", "")
                # clean_body = raw_html
                # chunk_res['html'].append(clean_body)
                chunk_res['text'].append(clean_body)
            # if not filename:
            #     filename = "index.html"
            # filepath = os.path.join(folder_name, filename)
            # print("Saving HTML to", filepath)
            # with open(filepath, "wb") as f:
            #     f.write(urlsafe_b64decode(data))
        else:
            # attachment other than a plain text or HTML
            for chunk_header in chunk_headers:
                chunk_header_name = chunk_header.get("name")
                chunk_header_value = chunk_header.get("value")
                print(f"Part Headers: {chunk_header_name}: {chunk_header_value}")
                if chunk_header_name == "Content-Disposition":
                    if "attachment" in chunk_header_value:
                        # we get the attachment ID 
                        # and make another request to get the attachment itself
                        print("Saving the file:", filename, "size:", get_size_format(file_size))
                        attachment_id = body.get("attachmentId")
                        attachment = self.gmail_service.messages() \
                                    .attachments().get(id=attachment_id, userId='me', messageId=message_id).execute()
                        data = attachment.get("data")
                        filepath = os.path.join(folder_name, filename)
                        if data:
                            with open(filepath, "wb") as f:
                                f.write(urlsafe_b64decode(data))
                            chunk_res['attachments'].append(filepath)

        return chunk_res

    def parse_parts(self, parts, folder_name, message_id):
        """
        Utility function that parses the content of an email partition
        """
        parts_res = {
            'text': [],
            'attachments': []
        }
        if parts:
            for i, part in enumerate(parts):
                print(f"Part: {i}")
                chunk_res = self.parse_chunk(part, folder_name, message_id)
                parts_res['text'] += chunk_res['text']
                parts_res['attachments'] += chunk_res['attachments']

        return parts_res

    def clean_email_body(self, body: str) -> str:
        import itertools
        import re
        """Clean email body."""
        def filter_nonprintable(text):
            NOPRINT_TRANS_TABLE = {
                i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
            }

            res = text.translate(NOPRINT_TRANS_TABLE)

            nonprintable = itertools.chain(range(0x00,0x20),range(0x7f,0xa0))
            return res.translate({character:None for character in nonprintable})

        def remove_whitespace(text):
            # return text
            res = re.sub(r"\s+", " ", text)
            res = re.sub(r"[^a-zA-Z.!?0-9\\s]", " ", res)
            # return res.replace("\t", " ").replace("\n", " ")
            return " ".join(res.split())

        try:
            from bs4 import BeautifulSoup

            try:
                soup = BeautifulSoup(str(body), "html.parser")
                body = soup.get_text()
                printable_body = filter_nonprintable(body)
                return str(remove_whitespace(printable_body))
                return str(printable_body.replace("\n", "").replace(r"", ""))
            except Exception as e:
                logger.error(e)
                return str(body)
        except ImportError:
            logger.warning("BeautifulSoup not installed. Skipping cleaning.")
            return str(body)

