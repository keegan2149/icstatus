#!/usr/local/bin/python2.7

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def ic_sendmail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= [], subject='',payload=''):

	receiver_list = ''
	receiver_addresses = ''
	for name,address in receiver_info.items():
		receiver_list += " %(name)s <%(address)s>," % {'name': name,'address': address}
		receiver_addresses += " %s," % address
	receiver_list.rstrip(',')
	receiver_addresses.rstrip(',')

	if isinstance(payload,list):
		body_buffer = ''.join(payload)

	message = """From: %(s_name)s <%(s_address)s>
To: %(receiver_list)s
Subject: %(subject)s

%(body)s
""" % {'s_name':sender_address , 's_address':sender_name, 'receiver_list': receiver_list, 'subject': subject, 'body':body_buffer}

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender_address, receiver_addresses, message)
		print "Successfully sent email"
		return 0
	except Exception , e:
		print e
		print "Error: unable to send email"
		return 1

def ic_mime_mail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= [], subject='',body=''):

	receiver_list = ''
	receiver_addresses = ''
	for name,address in receiver_info.items():
		receiver_list += " %(name)s <%(address)s>," % {'name': name,'address': address}
		receiver_addresses += " %s," % address
	receiver_list.rstrip(',')

	COMMASPACE = ', '

	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = sender_address
	msg['To'] = reciever_addresses
	msg.preamble = subject

	for file in pngfiles:
	    fp = open(file, 'rb')
	    img = MIMEImage(fp.read())
	    fp.close()
	    msg.attach(img)

	s = smtplib.SMTP('localhost')
	s.sendmail(me, family, msg.as_string())
	s.quit()
