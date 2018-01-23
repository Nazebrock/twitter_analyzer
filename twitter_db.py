#!/usr/bin/env python3


from pyspark.sql import SparkSession

#Creation d'une application spark


spark = SparkSession.builder \
                        .appName(config.SPARK_APP_NAME) \
                        .config("spark.ui.showConsoleProgress","false") \
                        .master("local").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

#Creation d'une DATAFRAME (une « table ») à partir du fichier JSON se trouvant dans HDFS
#Il faut remplacer le chemin par le fichier sous hdfs
#on pourra le remplacer au début par un simple fichier local

df = spark.read.json("hdfs://localhost:9000/input/twitter/20170129.json")

rdd = df.rdd

#On obtient un objet RDD de Row(…) qui fonctionnent comme des dictionnaires pythons.

rdd2 = rdd.map(lambda x: x['user_id'])
for i in rdd2.collect():
    print (i)
