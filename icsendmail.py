#!/usr/local/bin/python2.7

import smtplib

def ic_sendmail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= [], subject='',list_message=[],str_message='',layout='html_table'):

	receiver_list = ''
	receiver_addresses = ''
	for name,address in receiver_info.items():
		receiver_list += " %(name)s <%(address)s>," % {'name': name,'address': address}
		receiver_addresses += " %s," % address
	receiver_list.rstrip(',')

	if layout == 'text':
		if isinstance(str_message,list):
			str_message = ''.join(str_message)
			message = """From: %(s_name)s <%(s_address)s>
To: %(receiver_list)s
Subject: %(subject)s

%(str_message)s
""" % {'s_name':sender_address , 's_address':sender_name, 'receiver_list': receiver_list, 'subject': subject, 'body':inner_object}
	elif layout == 'html_table':
		message = generate_html_message(message_lines=list_message)

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender_address, receiver_addresses, message)
		print "Successfully sent email"
		return 0
	except Exception , e:
		print e
		print "Error: unable to send email"
		return 1

def generate_html_message(message_lines=[],layout='html_table'):
	css = """
table, th, td {
	border: 1px solid black;
}

	"""
	def generate_cells(line = [],indent=0,header=False):
		cells = ''
		if header:
			for item in line:
				cells += '\t' * indent + '<th> ' + item + r'<\th>\n'
		else:
			for item in line:
				cells += '\t' * indent + '<td>' + item + r'<\td>\n'
		return cells

	if layout == 'html_table':
		message = '<html>\n\t<head><\head>\n\t\t<body>\n\t\t\t<table>\n'
		indent = 4
		tab = '\t'
		for line in message_lines:
			for line_type,list_line in line.items():
				message += '\t' * indent + '<tr>\n'
				if line_type == 'device' or line_type == 'header':
					header=True
				else:
					header=False
				indent += 1
				message += generate_cells(list_line,indent=indent,header=header)
				indent -= 1
				message += '\t' * indent + r'<\tr>\n'
		indent -= 1
		message += '\t' * indent + r'<\table>'
		indent -= 1
		message += '\t' * indent + r'<\body>'
		indent -= 1
		message += '\t' * indent + r'<\html>'
	return message









