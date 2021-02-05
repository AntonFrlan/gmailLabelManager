from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
import base64
from bs4 import BeautifulSoup
import dateutil.parser as parser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import datetime
import label.labelManager as LB


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    creds = None
    labelNames = LB.labelManager()

    currentTime = datetime.datetime.now()
    timeLimit = datetime.timedelta(days=1)

    procitano = False

    response = ""
    while response != 'n' and response != 'y':
        print("Do you want to mark all unread messages as read? Type y / n")
        response = input()
        response = response.lower()
    if response == 'y':
        procitano = True

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    user_id = 'me'
    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'
    msg_from = None
    m_date = None

    results = service.users().messages().list(userId=user_id, labelIds=[label_id_one, label_id_two]).execute()
    mssg_list = results.get('messages', [])

    print("Total unread messages in inbox: ", str(len(mssg_list)))

    final_list = []

    for mssg in mssg_list:
        temp_dict = {}
        m_id = mssg['id']
        message = service.users().messages().get(userId=user_id, id=m_id).execute()
        payld = message['payload']
        headr = payld['headers']

        for one in headr:
            if one['name'] == 'Subject':
                msg_subject = one['value']
                temp_dict['Subject'] = msg_subject
                print("You received a mail from", msg_from, "about", msg_subject + ".")
                if currentTime.date() - m_date >= timeLimit:
                    service.users().messages().modify(userId=user_id, id=m_id, body={'addLabelIds': [labelNames.old]}).execute()
                    print("You still have an unread message from: " + msg_from + "!!!!")
                print()

            if one['name'] == 'Date':
                msg_date = one['value']
                date_parse = (parser.parse(msg_date))
                m_date = (date_parse.date())
                temp_dict['Date'] = str(m_date)

            if one['name'] == 'From':
                msg_from = one['value']
                temp_dict['Sender'] = msg_from
                for i in labelNames.lab:
                    if one['value'].find(i[1]) > -1:
                        service.users().messages().modify(userId=user_id, id=m_id, body={'addLabelIds': [i[2]]}).execute()

        temp_dict['Snippet'] = message['snippet']

        try:

            mssg_parts = payld['parts']
            part_one = mssg_parts[0]
            part_body = part_one['body']
            part_data = part_body['data']
            clean_one = part_data.replace("-", "+")
            clean_one = clean_one.replace("_", "/")
            clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))
            soup = BeautifulSoup(clean_two, "lxml")
            mssg_body = soup.body()
            temp_dict['Message_body'] = mssg_body

        except:
            pass

        final_list.append(temp_dict)

        if procitano:
            service.users().messages().modify(userId=user_id, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()

    print("Total messaged retrived: ", str(len(final_list)))

    with open('CSV_NAME.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Sender', 'Subject', 'Date', 'Snippet', 'Message_body']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        for val in final_list:
            writer.writerow(val)


if __name__ == '__main__':
    main()