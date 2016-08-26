#!/usr/bin/env python
import os
import re
try:
    from .Parse import myParse
except Exception: #ImportError
    from Parse import myParse

class myQueries:
    # q = Queries()
    # q.runqueries(file_name, container_name)

    def getqueries_impala(self,
                          file):
        #dans le fichier file, on poste toutes les données que l'on veut executer dans notre benchmark
        #je on les separe pour voir comment elles se comportent dans notre hdfs
        f = open(file, 'r')
        str = f.read()
        f.close()
        str = re.sub('\n', ' ', str) #les sauts de ligne pausent problème
        queries = re.findall(r"[^\n][^;]*;", str)
        print(queries)
        return queries

    def load_data_impala(self,
                         query_shell,
                         query_load,
                         container):
        #quand j'ai fais le tour avec mes requètes pour un certain volume de données,
        #je continue avec un nouveau volume de données plus important
        #ici je les charge dans le hdfs
        f = open('data_load', 'w+')
        query = query_shell + '\n' + query_load
        f.write(query)
        f.close()
        cmd = 'docker cp data_load ' + container + ':/data_load'
        os.system(cmd)
        os.system('docker exec ' + container + '  impala-shell -f data_load')


    def exec_query_impala(self,
                  query,
                  container,
                  id_query,
                  stats,
                  data_size):
        #ici on va executer le une requète precise, recuperer les statistiques et les parser
        #pour les mettres dans le tableau stats
        query2 = query + ';\n summary;'
        # après chaques requètes, avant de fermer la connection, je lance la commande summary
        # elle va me permettre de recuperer des statistiques sur la requètes précédante et
        # donc de les garder en mémoire.
        print(query)
        file_name = 'query#'+ str(id_query)
        f = open(file_name,'w+')
        f.write(query2)
        f.close()
        cmd = 'docker cp '+ file_name +' '+ container + ':/' + file_name
        print(cmd)
        os.system(cmd)
        os.system('docker exec '+ container +'  impala-shell -f ' + file_name + ' > ' + file_name)
        #je demande à impala d'executer toutes les commandes contenues dans file_name, et je redirige la sortie standard
        #dans un fichier pour pouvoir ensuite le parser.
        if re.match(r'[\n\s]*[^shell].*', query) and re.match(r'[\n\s]*[^load].*', query):
            print(query2 + ' sent')
            p = myParse(file_name)
            stats.append([data_size, query, p.parse_avg_time(), p.parse_max_time(), p.parse_Mem_Peak()])
        print('query done')

    def add_data_impala(self,
                        id):
        print("TODO")

    def create_table_impala(self,
                            file,
                            container):
        #permet d'initialiser no tables dans impala
        print("#####")
        cmd = 'docker cp create_tables ' + container + ':/' + file
        print(cmd)
        os.system(cmd)
        cmd = 'docker exec ' + container + '  impala-shell -f ' + file
        os.system(cmd)
        print("#####")

    def run_queries_impala(self,
                   file,
                   container,
                   stats,
                   data_size):
        queries = self.getqueries_impala(file)
        x = 0
        for query in queries:
            self.exec_query_impala(query, container, x, stats, data_size)
            x += 1
        for stat in stats:
            print(stat)

    def exec_query_hive(self,
                        file,
                        container):
        os.system('docker exec ' + container + ' rm hive_script')
        cmd = 'docker cp ' + file + ' ' + container + ':/hive_script'
        print(cmd)
        os.system(cmd)
        os.system('docker exec ' + container + ' hive -f hive_script')

    def getdata_impala(self,
                       pattern,
                       container,
                       address,
                       port):
        #/!\ CAUTION WET FLOOR
        cmd1 = 'python3 client.py \'' + address + '\' \'' + port + '\' ' + '\'' + pattern + '\''
        print(cmd1)
        os.system('docker exec ' + container + ' echo #!/bin/sh\n' + cmd1 + ' > tmp')
        os.system('docker exec ' + container + ' chmod 777 tmp')
        cmd = 'docker exec ' + container + ' ./tmp'
        os.system(cmd)



