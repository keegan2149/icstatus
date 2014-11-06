#!/usr/local/bin/python2.7

import subprocess
import re
from hnmp import SNMP

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


def do_get(device,oid,community="public",table='no',columns={},column_mapping={}):
	snmp = SNMP(device,community)

	if table != 'no':
		snmp_table = snmp.table(
			oid,
			columns = columns,
			column_value_mapping=column_mapping,
		)
		fetch_all_columns=False
	else:
		response = snmp.get(oid)

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
				substitution = base_oid + table_oid + '.' + str(ident)
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




device = "10.220.220.12"
snmp_info = {
	"device": device,
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
		5: "devicemode ",
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



heading = '|%(heading1)s|%(heading2)s|%(heading3)s|%(heading4)s|%(heading5)s|%(heading6)s|%(heading7)s|%(heading8)s|%(heading9)s|%(heading10)s|' % { 'heading1':'  drive name  ', 'heading2':'  drive class  ', 'heading3':'  drive mode  ', 'heading4':'  drive serial  ' , 'heading5':'  temp  ' , 'heading6':'  array  ' , 'heading7':'  smart health  ' , 'heading8':'  capacity  ' , 'heading9':'  device state  ' , 'heading10':'  device status  ' }
horizontal_border = '=' * len(heading)
title = '=' * len(heading)/2 + '  ' + device + '  ' + '=' * len(heading)/2 
cell_size = 10
print horizontal_border
print title
for 



results_dict = do_get_from_shell("san01",snmp_info=snmp_info,table='yes')

drive_dict = {}
drive_names = results_dict['device name'].values
number_of_drives = len(drive_names.keys())
for index,current_drive in sorted(drive_names):
	print

pass

import pdb ; pdb.set_trace()