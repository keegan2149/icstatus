#!/usr/local/bin/python2.7

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def ic_sendmail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= {},cc_info= {}, subject='',comments='',list_message=[],str_message='',layout='html_table'):

	receiver_list = ''
	cc_list = ''
	#receiver_addresses = ''
	msg = MIMEMultipart('alternative')

	for name,address in receiver_info.items():
		receiver_list += " %(name)s <%(address)s>," % {'name': name,'address': address}
	for name,address in cc_info.items():
		cc_list += " %(name)s <%(address)s>," % {'name': name,'address': address}
	for address in receiver_info.values():
		msg.add_header('to',address)
	for address in cc_info.values():
		msg.add_header('cc',address)
	txt_body = MIMEText(''.join(str_message), 'plain')
	html_body = MIMEText(generate_html_message(message_lines=list_message,comments=comments), 'html')

	fh = open('last_email','w')
	fh.write(html_body.as_string())

	msg['Subject'] = subject
	msg['From'] = sender_address
	#msg['to'] = receiver_addresses
	#msg['cc'] = receiver_addresses
	msg.preamble = subject
	msg.attach(txt_body)
	msg.attach(html_body)

	try:
		smtpObj = smtplib.SMTP('localhost')
		if cc_info:
			smtpObj.sendmail(sender_address, msg.get_all('to') + msg.get_all('cc'), msg.as_string())
		else:
			smtpObj.sendmail(sender_address, msg.get_all('to'), msg.as_string())			
		print "Successfully sent email"
		return 0
	except Exception , e:
		print e
		print "Error: unable to send email"
		return 1

def ic_mime_mail(sender_address = 'status-automation@ixlink.com',sender_name = 'rancid-centos',receiver_info= [], subject='',body='',comments='',pics=[],prtg_server='10.0.223.171'):

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


def generate_html_message(message_lines=[],comments='',layout='html_table',prtg_server='10.0.223.171'):
	def generate_cells(line = [],indent=0,line_type='',prtg_server='10.0.223.171'):
		def convert_active(status):
			if status == 'true':
				return 'Active'
			elif status == 'false':
				return 'Inactive'

		cells = ''
		try:
			if line_type == 'header':
				for item in line:
					cells += '\t' * indent + '<th style="border: 1px solid black;background-color: #DCDCDC;text-align: center;"> ' + item + '</th>' + '\n'
			elif line_type == 'device': 
				for item in line:
					cells += '\t' * indent + '<td colspan="10"  title="%s" style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 12px;color: #000;border: 1px solid black;background-color: #DCDCDC;font-weight: 900;text-align: center;" >' % line_type + item + '</td>' + '\n'
			elif line_type == 'prtg_header' or line_type == 'prtg_probe_device' or line_type == 'prtg_group':
				url = line[2]
				cells = '\t' * indent + '<td colspan="10"  title="%(title)s" style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 12px;color: #000;border: 1px solid black;background-color: #DCDCDC;font-weight: 900;text-align: center;"><a href="%(url)s">' % {'title': line_type, 'url':url}  + line[0] + '</a></td>' + '<td colspan="10"  style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 12px;color: #000;border: 1px solid black;background-color: #DCDCDC;font-weight: 900;text-align: center;">'  +  convert_active(line[1]) + '</td>' +'\n'
			elif line_type == 'prtg_probe_line':
				url = line[1]
				cells = '\t' * indent + '<td colspan="10"  title="%(title)s"  style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 12px;color: #000;border: 1px solid black;background-color: #DCDCDC;text-align: center;"><a href="%(url)s">' % {'title': line_type, 'url':url}  + line[0] + '</a></td>' +'\n'
			elif line_type == 'prtg_device':
				url = line[2]
				cells = '\t' * indent + '<td colspan="10"  title="%(title)s"  style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 10px;color: #000;border: 1px solid black;background-color: #DCDCDC;font-weight: 900;text-align: center;"><a href="%(url)s">' % {'title': line_type, 'url':url}  + line[0] + '<td colspan="10"  style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 12px;color: #000;border: 1px solid black;background-color: #DCDCDC;font-weight: 900;text-align: center;">'  +  convert_active(line[1]) + '</td>' +'\n'
			elif line_type == 'sensors':
				for sensor in line:
					url = sensor['url']
					cells += '\t' * indent + '<td title="%(title)s"  style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 8px;color: #000;border: 1px solid black;background-color: #DCDCDC;text-align: center;"><a href="%(url)s">' % {'title': line_type, 'url':url} + sensor['name'] + '</a><br>' + sensor['message'][:12] + '<br>' + sensor['status'] + '<br>' + convert_active(sensor['active']) + '</td>' 
				cells += '\n'
			elif line_type == 'cmc_values':
				for item in line:
					if (line.index(item) == 6 and item == 'pass') or (line.index(item) == 7 and item == 'Normal'):
						color = '6699FF'
					elif (line.index(item) == 6 and item != 'pass') or (line.index(item) == 7 and item != 'Normal'):
						color = 'FF3300'
					else:
						color = 'DCDCDC'
					cells += '\t' * indent + '<td title="%(title)s"  style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 12px;color: #000;border: 1px solid black;background-color: #%(color)s;text-align: center;" >' % {'title': line_type, 'color':color} + item + '</td>' + '\n'
			else:
				for item in line:
					cells += '\t' * indent + '<td  title="%s"  style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 9px;color: #000;border: 1px solid black;background-color: #DCDCDC;text-align: center;">' % line_type + item + '</td>' + '\n'
		except:
			cells = '\t' * indent + '<td  title="%s" colspan="10" style="font-family: Verdana, Georgia, Arial, sans-serif;font-size: 9px;color: #000;border: 1px solid black;background-color: #DCDCDC;text-align: center;"> Error </td>' % 'Error'+ '\n'

		return cells

	if layout == 'html_table':
		if comments:
			message = '<html>\n\t<head>\n\t\t<meta http-equiv=\'Content-Type\' content=\'text/html; charset=us-ascii\'/>\n\t\t<meta http-equiv=\'X-UA-Compatible\' content=\'IE=edge,chrome=1\'/>\n\t</head>\n\t\t<body>\n\t\t\t<p>\n\t\t\t\t' + comments + '\n\t\t\t</p>\n\t\t\t<table style="border: 1px solid black;background-color: #DCDCDC">\n'
		else:
			message = '<html>\n\t<head>\n\t\t<meta http-equiv=\'Content-Type\' content=\'text/html; charset=us-ascii\'/>\n\t\t<meta http-equiv=\'X-UA-Compatible\' content=\'IE=edge,chrome=1\'/>\n\t</head>\n\t\t<body>\n\t\t\t<table style="border: 1px solid black;background-color: #DCDCDC">\n'

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

