#!/usr/bin/python

import sys
import requests
import json
import smtplib
from lxml import html
import time


def getConf():    
    with open(sys.argv[1],'r') as confFile:
        conf = json.load(confFile)
        return conf

def sendmail(conf, subject, body):
    session = smtplib.SMTP(conf["host"], conf["port"])
    session.ehlo()
    session.starttls()
    session.login(conf["user"], conf["pass"])
    headers = "\r\n".join(["from: " + conf["host"],
                       "subject: " + subject,
                       "to: " + conf["recipient"],
                       "mime-version: 1.0",
                       "content-type: text/html"])
    
    try:
        content = headers + "\r\n\r\n" + body
    except  UnicodeEncodeError, e:
        pass
    session.sendmail(conf["user"], conf["recipient"], content)

def main():
    conf = getConf()
    url = conf["url"]
    resp = requests.get(url)
    print url
    body = html.fromstring(resp.text)[1]
    textBody = body.xpath('//div[@class="entry-content"]//li/a/text()')
    body = '<br />'.join(textBody)
    print body
    body2 = body.replace(u"\u2019","'")
    print body2
    subject = "cList for  " + time.strftime("%c")
    sendmail(conf, subject, body2)

if __name__ == '__main__':
    sys.exit(main())
