import os
import logging
try:
    from .Queries import myQueries
except:
    from Queries import myQueries

try:
    from .Parse import myParse
except:
    from Parse import myParse

logger = logging.getLogger('benchlogs')

format = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(format=format, level=logging.WARNING)

# this benchmark will sent many request to a Cloudera container
# in each loop we add more data to the cluster and estimate the execution time of each query

class myBenchmark(object):
    def __init__(self):
        self.Q = myQueries()

    def reset_benchmark_impala(self,
                               file,
                               container):
        self.Q.create_table_impala(file, container)

    def run_benchmark_impala(self,
                             file,
                             container):
        stats = []
        stack = self.Q.getqueries_impala('load_data')
        loop = 1
        while True:
            print("size:")
            os.system('docker exec ' + container + ' impala-shell -q "select count(*) from source" > data_size')
            #cette commande va nous permettre de regarder les temps d'execution en fonction du nombre de données dans le hdfs
            p = myParse('data_size')
            data_size = p.parse_nb_lines()
            if data_size == 0:
                logger.warn("No data load in the source table check if you have read write access to this hdfs")
            else:
                logger.warn("the Source table contains {} lines", data_size)
            self.Q.load_data_impala(stack.pop(0), stack.pop(0), container)
            self.Q.run_queries_impala(file, container, stats, data_size)
            if len(stack) == 0:
                break
            loop += 1
        os.system('rm query#*')

def launch(queries, create_tables, container):
    bench = myBenchmark()
    bench.reset_benchmark_impala(create_tables, container)
    bench.run_benchmark_impala(queries, container)

launch('queries', 'create_tables', 'eceeeb983e30')




