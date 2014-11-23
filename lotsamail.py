#!/usr/local/bin/python2.7

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_a_mail(number):
	body = 'test email ' + str(number)
	msg = MIMEMultipart('alternative')
	msg['Subject'] = str(number)
	msg['From'] = 'sgtest@ixlink.com'
	msg.add_header('to','rama@live.ixlink.org')
	msg.preamble = str(number)
	txt_body = MIMEText(body, 'plain')
	msg.attach(txt_body)
	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail('sgtest@ixlink.com', msg.get_all('to'), msg.as_string())
		print "sent email " + str(number)
		return 0
	except Exception , e:
		print e

end = 10
for number in range(0,end):
	send_a_mail(number)

	
