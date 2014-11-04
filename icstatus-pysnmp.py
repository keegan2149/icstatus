#!/usr/local/bin/python2.7

from hnmp import SNMP

snmp = SNMP("10.220.220.11",community="public")

import pdb ; pdb.set_trace()
[root@rhel-rancid icstatus]# cat icstatus.py 
#!/usr/local/bin/python2.7


from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('10.220.220.11', 161)),
    '.1.3.6.1.4.1.9804.3.1.1.2.4.2.1'
)

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

