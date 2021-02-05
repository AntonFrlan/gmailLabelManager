Script which read all unread mails and tags them according to sender.

In order to use the script you first need to download credentials.json from:
https://developers.google.com/gmail/api/quickstart/python

Place a copy of credentials.json in folder with gmailManager.py and in folder label with
labelManager.py 

During the first launch you'll need to log in twice in order to generate tokens which'll enable you to
run the script without further logins.

In folder "label" you'll find txt file named "labelNames.txt" in which you'll write e-mails and labels
with which you want to tag mails from said e-mails. It needs to be written in following format:
tag1: mail1@gmail.com , mail2@gmail.com , 
tag2: mgail13@gmail.com , mail@riteh.hr , 

If the written tag doesn't exist it'll creat a new one. Also if the mail is unread and older than a day
it'll tag it with "OLD"

DISCLAIMER: The code was written on Windovs so in case your using some other OS you might need to change relative
paths in labelManager.py. Also I used library "os-win" so I don't know if they're diffrent for other operating systems.