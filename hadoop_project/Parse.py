import re

class myParse:
    def __init__(self, file):
        self.file = file
    def parse_max_time(self):
        f = open(self.file, 'r')
        result = f.read()
        f.close()
        matches = re.findall(r'\s*\|[^\|\n]*\|[^\|\n]*\|[^\|\n]*\|\s*(\d+\.\d+[msnu]+).*', result)
        #je recupère ce type de ligne
        #| 00:SCAN HDFS | 1      | 380.00ms | 380.00ms | 100.00K | -1         | 32.05 MB | 176.00 MB     | default.source |
        # et j'en extrait le 2eme temps
        print('Max Time(s):')
        return self.make_seconds_from_muns(matches)

    def parse_nb_lines(self):
        f = open(self.file, 'r')
        result = f.read()
        f.close()
        matches = re.findall(r'\|\scount\(\*\)\s*\|\n\+-*\+\n\|\s*(\d*)', result)
        digit = 0
        for match in matches:
            digit += int(match)
        print('Nb Lines:')
        print(digit)
        return digit

    def parse_avg_time(self):
        f = open(self.file, 'r')
        result = f.read()
        f.close()
        matches = re.findall(r'\s*\|[^\|\n]*\|[^\|\n]*\|\s*(\d+\.\d+[msnu]+).*', result)
        # je recupère ce type de ligne
        # | 00:SCAN HDFS | 1      | 380.00ms | 380.00ms | 100.00K | -1         | 32.05 MB | 176.00 MB     | default.source |
        # et j'en extrait le premier temps
        print('AVG Time(s):')
        return self.make_seconds_from_muns(matches)

    def make_seconds_from_muns(self,
                               matches):
        #j'additionne tous les temps d'une meme colonne en prenant garde à l'ordre de grandeur
        #je retourne le temps total
        digit = 0
        for line in matches:
            if re.match(r'(\d+.\d+)s', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0])
            if re.match(r'(\d+.\d+)ms', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0]) / 1000
            if re.match(r'(\d+.\d+)us', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0]) / 1000000
            if re.match(r'(\d+.\d+)ns', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0]) / 1000000000
        print(digit)
        return digit

    def parse_Mem_Peak(self):
        f = open(self.file, 'r')
        result = f.read()
        f.close()
        matches = re.findall(r'\s*\|[^\|\n]*\|[^\|\n]*\|[^\|\n]*\|[^\|\n]*\|[^\|\n]*\|[^\|\n]*\|\s*(\d+\.\d+\s*[KMBG]+).*', result)
        print('Mem Peak(MB):')
        return self.make_MB_from_KMGB(matches)

    def make_MB_from_KMGB(self,
                          matches):
        digit = 0
        for line in matches:
            if re.match(r'(\d+.\d+)\s*B', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0]) / 1000000
            if re.match(r'(\d+.\d+)\s*MB', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0])
            if re.match(r'(\d+.\d+)\s*KB', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0]) / 1000
            if re.match(r'(\d+.\d+)\s*GB', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0]) * 1000
            if re.match(r'(\d+.\d+)\s*TB', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0]) * 1000000
            if re.match(r'(\d+.\d+)\s*PB', line):
                digit += float(re.findall(r'(\d+.\d+)\D', line)[0]) * 1000000000
        print(digit)
        return digit

#p = myParse('result')
#p.parse_avg_time()
#p.parse_max_time()
#p.parse_Mem_Peak()

