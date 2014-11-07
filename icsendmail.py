#!/usr/local/bin/python2.7

import smtplib

def ic_sendmail(sender_address = 'status-automation@ixlink.com',sender_name = '',reciever_addresses = [], subject='',body='')

	recievers_list = ''
	for name,address in reciever_addresses.items():
		recievers_list += " %(name)s <%(address)s>," % {'name': name,'address': address}

	reciever_list.rstrip(',')

	message = """From: %(s_name)s <%(s_address)s>
To: %(reciever_list)s
Subject: %(subject)s

%(body)s
""" % {'s_name':sender_address , 's_address':sender_name, 'reciever_list': reciever_list, 'subject': subject, 'body':body}

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender, receivers, message)
		print "Successfully sent email"
		return 0
	except SMTPException:
		print "Error: unable to send email"
		return 1