from get_activity import get_activity
import re


#str = open('mac_address_wifi', 'r').read()
#str = re.sub(r'\s', r'\n', str)
#addressesI = re.split(r'\n', str)
#for address in addresses:
#    re.sub(r'\s', r'', address)
A = get_activity()
print(A.get_listener())
#addresses = []
#for add in addressesI:
#    if add != '':
#        addresses.append(add)
#for address in addresses:
#    res = A.activity(address)
#    with open('mac_address_activity/'+address+'.pickle', 'wb') as f:
#        pickle.dump(res, f)
#os.system('ls -l mac_address_activity')


