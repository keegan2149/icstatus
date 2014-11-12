import sys
import os
import re
import datetime
import requests
import xml.etree.ElementTree as et
import codecs

def get_credentials(conf_dir = '/usr/apps/icstatus/',conf_file = 'prtg.conf'):
	fh = open(os.path.join(conf_dir,conf_file),'r')
	lines = fh.read().rstrip('\n').split(',')
	return {'server': lines[0],'username': lines[1],'password': lines[2] }


def get_prtg_results(ssl=False,**kwargs):
	if not kwargs:
		creds = get_credentials()
	else:
		creds = kwargs
	return requests.get('https://' + creds['server'] + '/api/table.xml?content=sensortree&openutput=xml&id=9445?id=sensorid&username=%(username)s&password=%(password)s' % { 'username': creds['username'],'password': creds['password'] }, verify = ssl).text


def e_process_prtg_results(api_response):
	def get_url(prtg_ip,node):
		return 'https://' + prtg_ip + node.find('url').text
	def get_probes(root,probes_list):
		probes = []
		for probe_id in probes_list:
			path = './/probenode' + "[@id='%s']" % str(probe_id)
			probes.append(root.find(path))
		return probes
	def summarize_device(dev):
		device_summary = dev.find('summary').text.split(',')
		device_summary = map(int,device_summary)
		device_active = dev.find('active').text
		device_summary_url = get_url(prtg_ip,current_probe.find('./device'))
		if device_summary[0] == 0:
			return {'prtg_probe_line':[str(device_summary[1]) + ' sensors OK',device_summary_url]}
		elif dev('active').text == 'false':
			return {'prtg_probe_line':[str(device_summary[1]) + ' sensors INACT',device_summary_url]}
		else:
			return {'prtg_probe_line':[str(device_summary[1]) + ' sensors DOWN',device_summary_url]}


	list_data = []
	str_data = ''
	prtg_ip = '10.0.223.171'
	api_response = api_response.encode('utf-8')
	root = et.fromstring(api_response)

	summarized_groups = {9457:1,9473:1}
	probe_ids = [9445]
	probes = get_probes(root,probe_ids)
	for current_probe in probes:
		probe_name = current_probe.find('name').text
		probe_url = get_url(prtg_ip,current_probe)
		probe_active = current_probe.find('active')
		probe_device = current_probe.find('device')
		list_data.append({'prtg_probe_device':[probe_name,probe_active.text,probe_url]})
		list_data.append(summarize_device(probe_device))

		groups = current_probe.findall('./group')
		for current_group in groups:
			group_name = current_group.find('name').text
			group_url = get_url(prtg_ip,current_group)
			group_active = current_group.find('active')
			list_data.append({'prtg_group':[group_name,group_active.text,group_url]})

			devices = current_group.findall('./device')
			for current_device in devices:
				sensors_list = []
				device_name = current_device.find('name').text
				device_url = get_url(prtg_ip,current_device)
				device_active = current_device.find('active')
				list_data.append({'prtg_device':[device_name,device_active.text,device_url]})

				sensors = current_device.findall('./sensor')
				for current_sensor in sensors:
					if current_sensor.attrib['id'] == 4814:
						import pdb ; pdb.set_trace()
					sensor_name = current_sensor.find('name').text
					sensor_url = get_url(prtg_ip,current_sensor)
					sensor_status = current_sensor.find('status')
					sensor_message = current_sensor.find('statusmessage')
					sensor_active = current_sensor.find('active')
					sensors_list.append({'name':sensor_name,'status':sensor_status.text,'message':sensor_message.text,'active':sensor_active.text,'url':sensor_url})
				list_data.append({'sensors':sensors_list})

	return list_data
