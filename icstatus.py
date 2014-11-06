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
		self.type = ''
		self.values = {}
		self.size = 0

	def append_data(self,input_list=[]):
		index = int(input_list[0].lstrip('.')) 
		if not self.values.has_key(ident):
			self.values[ident] = ' '.join(input_list[3::]).rstrip()
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
			if names = None:
				if re.search(snmp_info[base_oid],line,re.I):
					names = False
				elif re.search(snmp_info[base_oid_name],line,re.I):
					names = True
			if names = True:
				base_oid = snmp_info[base_oid_name]
			elif names = False:
				base_oid = snmp_info[base_oid]
			for ident,value_name in snmp_info[colunms].items():
				pattern = base_oid + table_oid + '.' + str(ident)
				reg_search = re.compile(pattern)
				if reg_search.search(line):
					temp = re.sub(pattern,'',line).split(' ')
					if not result_dict.has_key(value_name):
						result_dict[value_name] = snmp_get_response()
						result_dict[value_name].oid = snmp_info[oid]
						result_dict[value_name].base_oid = snmp_info[base_oid]
						result_dict[value_name].base_oid_name = snmp_info[base_oid_name]
						result_dict[value_name.].table_oid = snmp_info[table_oid]
					result_dict[value_name].append_data(input_list=temp)




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
		18: "device smarthealth",
		19: "storage device",
		20: "storage device",
		90: "storagedevice state",
		91: "storage device",
	}
}

import pdb ; pdb.set_trace()
result = do_get_from_shell("san01",oid,table='yes',columns=colunms_dict)

import pdb ; pdb.set_trace()