import sys
import re

dependencies = open(sys.argv[1], 'r').read()
dependencies = re.split(r'\n', dependencies) 

dependencies.remove('')
merge= ''
for file in dependencies:
    data = open(file, 'r').read()
    merge = merge + '\n' + data

for file in dependencies:
	merge = re.sub(r'from\s'+re.sub(r"\.py", r"", file)+'.*', r'', merge)

open('data_merge.py', 'w+').write(merge)


