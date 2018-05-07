"""Handle email."""
from email.mime.text import MIMEText
import base64
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from django.conf import settings

GMAIL_API = getattr(settings, 'GMAIL_API', {})
if not GMAIL_API:
    print('-------------------------------------')
    print('GMAIL_API settings is not set up set.')
    print('-------------------------------------')


def get_credentials():
    """Get valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.

    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(
        credential_dir,
        'aji'
    )
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(
            GMAIL_API.get('CLIENT_SECRET_FILE'),
            GMAIL_API.get('SCOPES'),
        )
        flow.user_agent = GMAIL_API.get('APPLICATION_NAME')
        flags = tools.argparser.parse_args(['--noauth_local_webserver'])
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_service():
    """Get service."""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service


def send_mail(to, subject, message_text):
    """Create a message and send email."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = 'me'
    message['subject'] = subject
    body = {
        'raw':
        base64.urlsafe_b64encode(
            message.as_string().encode('utf-8')
        ).decode('utf-8')
    }

    service = get_service()
    try:
        message = service.users().messages().send(
            userId='me',
            body=body,
        ).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)
