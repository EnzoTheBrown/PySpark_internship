import re
import sys
import copy
import os
import subprocess

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

proc = subprocess.Popen(["ls", ""], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
out = re.split(r'\n', out)


def extract_dependencies(f):
    contents = open(f, 'r').read()
    contents = re.findall(r'from.*import.*', contents)
    res = []
    for line in contents:
        res.append(re.findall(r'from\s\.?(.*)\simport.*', line)[0]+'.py')
    res = intersect(res, out)
    return res

new_files = [sys.argv[1]]
new_files += extract_dependencies(sys.argv[1])

for new_file in new_files:
    new_files += extract_dependencies(new_file)


files = []
for i in new_files:
    if i not in files:
        files.append(i)

merge = ''

files2 = copy.copy(files)
while len(files2) > 0:
    content = open(files2.pop(), 'r').read()
    merge += '\n' + content

for file in files:
    print(file)
    merge = re.sub(r'from\s\.?' + re.sub(r"\.py", r"", file) + '.*', '', merge)

open('data_merge.py', 'w+').write(merge)

#command = 'data_merge.py '
#for arg in sys.argv[2:]:
#    command += arg + ' '

#os.system(command)

