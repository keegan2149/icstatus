#!/usr/local/bin/python2.7

import smtplib

def ic_sendmail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= [], subject='',body=''):

	receiver_list = ''
	receiver_addresses = ''
	for name,address in receiver_info.items():
		receiver_list += " %(name)s <%(address)s>," % {'name': name,'address': address}
		receiver_addresses += " %s," % address
	receiver_list.rstrip(',')

	if isinstance(body,list):
		''.join(body)

	message = """From: %(s_name)s <%(s_address)s>
To: %(receiver_list)s
Subject: %(subject)s

%(body)s
""" % {'s_name':sender_address , 's_address':sender_name, 'receiver_list': receiver_list, 'subject': subject, 'body':body}

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender_address, receiver_addresses, message)
		print "Successfully sent email"
		return 0
	except Exception , e:
		print e
		print "Error: unable to send email"
		return 1