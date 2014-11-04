#!/usr/local/bin/python2.7

from hnmp import SNMP

def $get_snmp(device,oid,community="public",table='no',columns={},column_mapping={}):
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
