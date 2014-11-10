#!/usr/local/bin/python2.7

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def ic_sendmail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= [], subject='',comments='',list_message=[],str_message='',layout='html_table'):

	receiver_list = ''
	receiver_addresses = ''
	for name,address in receiver_info.items():
		receiver_list += " %(name)s <%(address)s>," % {'name': name,'address': address}
	
	receiver_list.rstrip(',')
	receiver_addresses = ','.join(receiver_info.values())
	receiver_addresses.rstrip(', ')

	txt_body = MIMEText(''.join(str_message), 'plain')
	html_body = MIMEText(generate_html_message(message_lines=list_message,comments=comments), 'html')

	print html_body

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = sender_address
	msg['To'] = receiver_addresses
	msg.preamble = subject
	msg.attach(txt_body)
	msg.attach(html_body)

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender_address, receiver_addresses, msg.as_string())
		print "Successfully sent email"
		return 0
	except Exception , e:
		print e
		print "Error: unable to send email"
		return 1

def ic_mime_mail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= [], subject='',body='',comments='',pics=[]):

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


def generate_html_message(message_lines=[],comments='',layout='html_table'):
	def generate_cells(line = [],indent=0,line_type=''):
		cells = ''
		if line_type == 'header':
			for item in line:
				cells += '\t' * indent + '<th style="border: 1px solid black;background-color: #DCDCDC;text-align: center;"> ' + item + '</th>' + '\n'
		elif line_type == 'device': 
			for item in line:
				cells += '\t' * indent + '<td colspan="100"  style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 12px;color: #000;border: 1px solid black;background-color: #DCDCDC;font-weight: 900;text-align: center;" >' + item + '</td>' + '\n'
		else:
			for item in line:
				cells += '\t' * indent + '<td style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 9px;color: #000;border: 1px solid black;background-color: #DCDCDC;text-align: center;">' + item + '</td>' + '\n'
		return cells

	if layout == 'html_table':
		if comments:
			message = '<html>\n\t<head>\n\t\t<meta http-equiv=\'Content-Type\' content=\'text/html; charset=utf-8\'/>\n\t\t<meta http-equiv=\'X-UA-Compatible\' content=\'IE=edge,chrome=1\'/>\n\t</head>\n\t\t<body>\n\t\t\t<p>\n\t\t\t\t' + comments + '\n\t\t\t</p>\n\t\t\t<table style="border: 1px solid black;background-color: #DCDCDC">\n'
		else:
			message = '<html>\n\t<head>\n\t\t<meta http-equiv=\'Content-Type\' content=\'text/html; charset=utf-8\'/>\n\t\t<meta http-equiv=\'X-UA-Compatible\' content=\'IE=edge,chrome=1\'/>\n\t</head>\n\t\t<body>\n\t\t\t<table style="border: 1px solid black;background-color: #DCDCDC">\n'

		indent = 4
		tab = '\t'
		for line in message_lines:
			for line_type,list_line in line.items():
				message += '\t' * indent + '<tr>\n'
				indent += 1
				message += generate_cells(list_line,indent=indent,line_type=line_type)
				indent -= 1
				message += '\t' * indent + '</tr>'+ '\n'
		indent -= 1
		message += '\t' * indent + '</table>' + '\n'
		indent -= 1
		message += '\t' * indent + '</body>' + '\n'
		indent -= 1
		message += '\t' * indent + '</html>' + '\n'
	return message

