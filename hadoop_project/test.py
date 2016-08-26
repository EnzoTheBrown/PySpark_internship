#import re

#str = "'abc' '''''''''''''''"
#str = re.sub('\'', '\\\'', str)
#print(str)

#from impala.dbapi import connect
#conn = connect(host='172.17.0.2', port=21050)
#cursor = conn.cursor()
#cursor.execute('SELECT count(*) FROM source')
#print(cursor.description)  # prints the result set's schema
#results = cursor.fetchall()

#import os

#os.system('docker ps -q > tmp_dockerId')

#f = open('tmp_dockerId', 'r')
#str = f.read()
#f.close()
#print(str)

#import re

#f = open('queries', 'r')
#result = f.read()
#f.close()
#matches = re.findall(r"[^#\n].*", result)
#print(matches)

#import  re
#f = open('result', 'r')
#result = f.read()
#f.close()
#matches = re.findall(r'\|\scount\(\*\)\s*\|\n\+-*\+\n\|\s*(\d*)', result)
#print('Nb Lines:')
#digit = 0
#for match in matches:
#    digit += int(match)

#print(digit)

import re
str = "bonjour monsieur le commissaire."
str = '\nbonjour l\'addition s\'il vous plait!'
str = str + ';\n summary;'

if re.match(r'\n*[^bonjour].*', str):
    print("rude")
else:
    print('polite')