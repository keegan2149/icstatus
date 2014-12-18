#!/usr/local/bin/python2.7
import sys
import os
import subprocess
import re
import icsendmail
from hnmp import SNMP
import datetime
import prtg_api as prtg
import datetime

class snmp_get_response(object):
	def __init__(self):
		self.oid = ''
		self.base_oid = ''
		self.base_oid_name = ''
		self.table_oid = ''
		self.table_oid_name = ''
		self.type = ''
		self.values = {}
		self.size = 0

	def append_data(self,input_list=[]):
		index = int(input_list[0].lstrip('.')) 
		if not self.values.has_key(index):
			self.values[index] = ' '.join(input_list[3::]).rstrip()
			self.type = input_list[2].rstrip(':')
			self.size = len(self.values.keys())
		else:
			print "duplicate key"

def get_args(args):
	def print_help_and_die():
		print """ icstatus.py [-h] [-b] [-c] [<comments file>]
			-h - print help
			-c <comments file> - attach comments to status email
			-b - bulleted comments in html version of email
"""
		sys.exit()

	args_dict = dict((arg,0) for arg in args)
	comments = ''
	bulleted = False
	if args_dict.has_key('-h'):
		print_help_and_die()
	elif args_dict.has_key('-c'):	
		if len(args) - args.index('-c') > 0:
			if not re.search(r'^-',args[args.index('-c') + 1]):
				try:
					fh = open(args[args.index('-c') + 1])
					comments = fh.read()
				except Exception, e:
					print e
					print "cannot open comments file running script without comments"
			else:
				print_help_and_die()

	if args_dict.has_key('-b'):
		bulleted = True
	return comments,bulleted,args_dict



def logger(message=[],logfile='/var/log/icstatus'):
	now = datetime.datetime.now()
	fh = open(logfile,'a')
	if isinstance(message,str):
		fh.write(message)
	elif isinstance(message,list):
		for line in message:
			fh.write(line)
	fh.close()

def do_get_from_shell(device,snmp_info = {},table='no'):
	command = "snmpwalk -v %(version)s -c %(community)s %(device)s  %(oid)s" % snmp_info 
	result = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT,stdout=subprocess.PIPE).stdout.readlines()

	if table != 'no':
		names = None
		result_dict = {}
		for line in result:
			line = line.rstrip()
			if names == None:
				if re.search(snmp_info['base_oid'],line,re.I):
					names = False
				elif re.search(snmp_info['base_oid_name'],line,re.I):
					names = True
			if names == True:
				base_oid = snmp_info['base_oid_name']
			elif names == False:
				base_oid = snmp_info['base_oid']
			table_oid = snmp_info['table_oid']
			for ident,value_name in snmp_info['colunms'].items():
				pattern = '^' + base_oid + table_oid + '\.' + str(ident) + '\.'
				substitution = base_oid + table_oid + '.' + str(ident) + '|' + '\"'
				reg_search = re.compile(pattern)
				if reg_search.search(line):
					temp = re.sub(substitution,'',line).split(' ')
					if not result_dict.has_key(value_name):
						result_dict[value_name] = snmp_get_response()
						result_dict[value_name].oid = snmp_info['oid']
						result_dict[value_name].base_oid = snmp_info['base_oid']
						result_dict[value_name].base_oid_name = snmp_info['base_oid_name']
						result_dict[value_name].table_oid = snmp_info['table_oid']
						result_dict[value_name].table_oid_name = value_name
					result_dict[value_name].append_data(input_list=temp)
	return result_dict

def convert_boolean(value):
	if value == '1':
		return "pass"
	else:
		return "fail"

def format_san_resutls(results_dict = {},current_device=''):
	str_data = []
	inner_object = []
	table_data = []

	drive_dict = {}
	drive_names = results_dict['device name'].values
	number_of_drives = len(drive_names.keys())
	if current_device == "san03":
		heading = '|%(heading1)s|%(heading2)s|%(heading3)s|%(heading4)s|%(heading6)s|%(heading8)s|%(heading9)s|' % { 'heading1':'  drive name   ', 'heading2':'   drive class   ', 'heading3':'  drive mode  ', 'heading4':'    drive serial    ', 'heading6':'         array         ' , 'heading8':'  smart health  ', 'heading9':'  capacity  '}
	else: 
		heading = '|%(heading1)s|%(heading2)s|%(heading3)s|%(heading4)s|%(heading6)s|%(heading8)s|%(heading9)s|' % { 'heading1':'  drive name   ', 'heading2':'   drive class   ', 'heading3':'  drive mode  ', 'heading4':'        drive serial        ' , 'heading6':'         array         ' , 'heading8':'  smart health  ', 'heading9':'  capacity  '}
	inner_object = {'header':['drive name' , 'drive class' , 'drive mode' , 'drive serial' , 'temp' , 'array' , 'smart health status' , 'smart health' , 'capacity' , 'device status']}
	horizontal_border = '=' * len(heading)
	formatted_device = '  ' + current_device + '  '
	if len(formatted_device) % 2:
		title = '=' * (len(heading)/2 - (len(formatted_device)/2)) + formatted_device  + '=' * (len(heading)/2 - (len(formatted_device)/2) - 1)
	else:
		title = '=' * (len(heading)/2 - (len(formatted_device)/2)) + formatted_device  + '=' * (len(heading)/2 - (len(formatted_device)/2))	
	high_value = 20
	#print title
	#print heading
	#print horizontal_border

	table_data.append(inner_object)
	inner_object = []
	table_data.append({'device':[current_device]})

	str_data.append(title + '\n')
	str_data.append(heading + '\n')
	str_data.append(horizontal_border + '\n')

	variable_fields = {}
	space_count = {}
	lwhitespace = {}
	rwhitespace = {}

	for index in sorted(drive_names):
		smart_health_status = convert_boolean(results_dict['device smarthealth status'].values[index])
		storage_device_status = convert_boolean(results_dict['storage device status'].values[index])
		if not variable_fields.has_key('drive name'):
			variable_fields['drive name'] = len(drive_names[index])
			space_count['drive name'] = 8
		if variable_fields['drive name'] > 0 and (len(drive_names[index]) - variable_fields['drive name'] == 1):
			space_count['drive name'] -= 1
		elif variable_fields['drive name'] > 0 and (variable_fields['drive name'] - len(drive_names[index]) == 1):
			space_count['drive name'] += 1

		if not space_count['drive name'] % 2:
			lwhitespace['drive name'] = " " * (space_count['drive name']/2)
			rwhitespace['drive name'] = " " * (space_count['drive name']/2)
		else:
			lwhitespace['drive name'] = " " * ((space_count['drive name']/2) + 1)
			rwhitespace['drive name'] = " " * (space_count['drive name']/2)
		variable_fields['drive name'] = len(drive_names[index])

		if current_device != "san03":
			if not variable_fields.has_key('drive serial'):
				variable_fields['drive serial'] = len(results_dict['serial number'].values[index])
				space_count['drive serial'] = 6
			#print "serial number length - variable field",len(results_dict['serial number'].values[index]) - variable_fields['drive serial']
			#import pdb ; pdb.set_trace()
			if variable_fields['drive serial'] > 0 and (len(results_dict['serial number'].values[index]) >= high_value):
				space_count['drive serial'] = 8
				#print "space count serial",space_count['drive serial']
			else:
				space_count['drive serial'] = 20
				#print "space count serial",space_count['drive serial']
			variable_fields['drive serial'] = len(results_dict['serial number'].values[index])
			
			if not space_count['drive serial'] % 2 and (len(results_dict['serial number'].values[index]) < high_value):
				lwhitespace['drive serial'] = " " * ((space_count['drive serial']/2) - 6)
				rwhitespace['drive serial'] = " " * ((space_count['drive serial']/2) + 6)
			elif (len(results_dict['serial number'].values[index]) < high_value):
				lwhitespace['drive serial'] = " " * ((space_count['drive serial']/2) - 5)
				rwhitespace['drive serial'] = " " * ((space_count['drive serial']/2) + 6)
			else:
				lwhitespace['drive serial'] = " " * (space_count['drive serial']/2)
				rwhitespace['drive serial'] = " " * (space_count['drive serial']/2)

		else:
			space_count['drive serial'] = 12
			lwhitespace['drive serial'] = " " * (space_count['drive serial']/2)
			rwhitespace['drive serial'] = " " * (space_count['drive serial']/2)

		line = '|%(value1)s|   %(value2)s   |    %(value3)s    |%(value4)s|   %(value6)s   |     %(value8)s     |   %(value9)s   |' % { 'value1': lwhitespace['drive name'] + drive_names[index] + rwhitespace['drive name'], 'value2':results_dict['device class'].values[index], 'value3':results_dict['devicemode'].values[index], 'value4': lwhitespace['drive serial'] + results_dict['serial number'].values[index] + rwhitespace['drive serial'],'value6':results_dict['device raid'].values[index] , 'value8':results_dict["device smarthealth"].values[index],'value9':results_dict['storage device capacity'].values[index]}
		inner_object = {'cmc_values':[drive_names[index],results_dict['device class'].values[index],results_dict['devicemode'].values[index],results_dict['serial number'].values[index], results_dict['temperature'].values[index] , results_dict['device raid'].values[index] , smart_health_status, results_dict["device smarthealth"].values[index],results_dict['storage device capacity'].values[index] , storage_device_status ]}
		#print  line
		str_data.append(line + '\n')
		table_data.append(inner_object)
		inner_object = []
	str_data.append('\n')
	#print horizontal_border
	#print
	str_data.append(horizontal_border + '\n')
	str_data.append('\n')
	return str_data,table_data




str_message = []
table_message = []
devices = ["san01","san02","san03"]
everyone  = {
	'Rama Iyer':'rama.iyer@telarix.com',
	'Keegan Holley':'kholley@icore.com>',
	'Mike Emerson':'m.emerson@telarix.com', 'Swapnil Gadkari':'sgadkari@telarix.com', 'Susan Wegmueller':'swegmueller@ixlink.com', 'Jason Alleman':'jalleman@icore.com', 'Matt Berkman':'mberkman@icore.com', 'Esteban Dolores': 'esteban.deleon@telarix.com'}
ixexec = {
	'Shahdy Ali-Hassan':'shahdy.ali-hassan@telarix.com',
	'Swapnil Gadkari':'swapnil.gadkari@telarix.com',
	'Mark Hatam':'mark.hatam@telarix.com',
	'Shoma Chakravarty':'shoma.chakravarty@telarix.com',
	'Susan Wegmueller':'susan.wegmueller@telarix.com'
}
status_list = { 
	'Chris Finn':'chris.finn@telarix.com',
	'Esteban Deleon':'esteban.deleon@telarix.com',
	'Jason Alleman':'jason.alleman@telarix.com',
	'Keegan Holley':'kholley@icore.com',
	'Lisa Tovar':'LTovar@telarix.com',
	'Mark Hatam':'mhatam@telarix.com',
	'Matthew Berkman':'matthew.berkman@telarix.com',
	'Shahdy Ali-Hassan':'sali-hassan@telarix.com',
	'Shoma Chakravarty':'shoma.chakravarty@telarix.com',
	'Susan Wegmueller':'swegmueller@ixlink.com',
	'Swapnil Gadkari':'sgadkari@telarix.com'
	}
me = {'keegan holley':'kholley@icore.com '}
gmail = {'keegan holley2':'keegan2149@gmail.com'}
me2 = me
me2.update(gmail)
snmp_info = {
	"device": '',
	"version": '2c',
	"community": "public",
	"oid":'.1.3.6.1.4.1.9804.3.1.1.2.4.2.1',
	"base_oid":'.1.3.6.1.4.1.9804',
	"base_oid_name":'SNMPv2-SMI::enterprises.9804',
	"table_oid":'.3.1.1.2.4.2.1',
	"table":'yes',
	"colunms": {
		2: "device model",
		3: "device class",
		4: "unavailable",
		5: "devicemode",
		6: "unavailable",
		7: "serial number",
		9: "temperature",
		10: "temp threshold",
		11: "temp limit",
		12: "temp ok",
		13: "device label",
		14: "device name",
		15: "device raid",
		16: "device firmware",
		17: "device smarthealth",
		18: "device smarthealth status",
		19: "storage device capacity",
		20: "hot removable",
		90: "storage device state",
		91: "storage device status",
	}
}
comments,bulleted,args_dict = get_args(sys.argv)
#prtg_response = prtg.get_prtg_results()
#prtg_structure = prtg.e_process_prtg_results(prtg_response)
#table_message = prtg_structure
#subject = 'PRTG status ' + datetime.datetime.now().__str__()
#icsendmail.ic_sendmail(receiver_info = me, cc_info = gmail, subject=subject,comments=comments,list_message=table_message)

table_message = []
subject = 'HP SAN drive status ' + datetime.datetime.now().__str__()
for current_device in devices:
	snmp_info['device'] = current_device
	results_dict = do_get_from_shell(current_device,snmp_info=snmp_info,table='yes')
	str_result,list_result = format_san_resutls(results_dict = results_dict,current_device=current_device)
	str_message += str_result
	table_message += list_result
logger(message=str_message)
icsendmail.ic_sendmail(receiver_info = status_list, subject=subject,comments=comments,list_message=table_message)
