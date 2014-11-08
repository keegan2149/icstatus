#!/usr/local/bin/python2.7

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def ic_sendmail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= [], subject='',payload=''):

	receiver_list = ''
	receiver_addresses = ''
	for name,address in receiver_info.items():
		receiver_list += " %(name)s <%(address)s>," % {'name': name,'address': address}
	receiver_list.rstrip(',')
	receiver_addresses = ', '.join(receiver_info.values())
	receiver_addresses.rstrip(', ')

	if isinstance(payload,list):
		body = MIMEText(''.join(payload), 'plain')
	elif isinstance(payload,str):
		body = MIMEText(payload, 'plain')

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = sender_address
	msg['To'] = receiver_addresses
	msg.preamble = subject
	msg.attach(body)

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender_address, receiver_addresses, msg.as_string())
		print "Successfully sent email"
		return 0
	except Exception , e:
		print e
		print "Error: unable to send email"
		return 1

def ic_mime_mail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= [], subject='',body='',pics=[]):

	receiver_list = ''
	receiver_addresses = ''
	for name,address in receiver_info.items():
		receiver_list += " %(name)s <%(address)s>," % {'name': name,'address': address}
	receiver_list.rstrip(',')
	receiver_addresses = ','.join(receiver_info.values())
	receiver_addresses.rstrip(',')
	COMMASPACE = ', '

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = sender_address
	msg['To'] = receiver_addresses
	msg.preamble = subject

	for pic in pics:
	    fp = open(pic, 'rb')
	    img = MIMEImage(fp.read())
	    fp.close()
	    msg.attach(img)
	msg.attach(body)
	s = smtplib.SMTP('localhost')
	s.sendmail(me, family, msg.as_string())
	s.quit()
