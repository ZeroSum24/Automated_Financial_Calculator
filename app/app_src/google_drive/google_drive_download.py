
# Dependencies: json, logging

# Google Drive Api link:
# https://developers.google.com/drive/api/v3/manage-downloads#examples


# Google drive api Dependencies
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials

import json
import logging
from os.path import join

from src.utils.misc_methods import set_up_logging

logger = logging.getLogger()

# Download all the spreadsheats with key values
def download_all_spreadsheets(keys_location: str, json_storage: str, logger_name= ""):

    global logger
    logger = set_up_logging(logger_name)

    # will be called if the account is not already authorised
    drive_key_path = join(json_storage, keys_location)
    drive_authorise(json_storage)

    # calling the value keys and for each downloading them from the drive
    key_dict = read_keys(drive_key_path)
    for file_key in key_dict.values():
        download_spreadsheets(file_key)

# From Google Drive API documentation used to perform a file download
def download_spreadsheets(file_key: str, json_storage: str):

    # Getting credentials
    credentials_path = join(json_storage, 'credentials.json')

    # Drive initialisation
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)

    # Downloading the files
    file_id = file_key
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download {0:%d%%}".format(int(status.progress() * 100)))


def drive_authorise(json_storage: str):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

    credentials_path = join(json_storage, 'credentials.json')
    token_path = join(json_storage, 'token.json')

    store = file.Storage(token_path)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(cred_path, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))


# Gets the file keys by reading the json
def read_keys(key_location: str):

    # reading json keys from location
    with open(key_location) as json_keys:

        loaded_txt = json_keys.read()
        logger.debug("Loaded text {0}".format(loaded_txt))

        # loading json from txt
        key_dict = json.loads(loaded_txt)
        json_keys.close()

    logger.debug("Loaded api dictionary {0}".format(key_dict))

    return key_dict
