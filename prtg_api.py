import requests

def get_credentials(conf_dir = '/usr/apps/icstatus/',conf_file = 'prtg.conf'):
	fh = open(os.path.join(conf_dir,conf_file),'r')
	lines = fh.read().rstrip('\n').split(',')
	return {'server': lines[0],'username': lines[1],'password': lines[2] }


def get_prtg_results(prtg_ip,username,password,ssl=False):
	return requests.get('https://' + prtg_ip + '/api/table.xml?content=sensortree&openutput=xml&id=9445?id=sensorid&username=%(username)s&password=%(password)s', verify = ssl).text


