#!/usr/local/bin/python2.7

from hnmp import SNMP

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


oid='.1.3.6.1.4.1.9804.3.1.1.2.4.2.1'
table='yes'
colunms_dict = {
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

result = do_get("san01",oid,table='yes',columns=colunms_dict)

import pdb ; pdb.set_trace()