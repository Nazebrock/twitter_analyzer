#!/usr/bin/env python3
from pyspark.sql import SparkSession
import json
import pprint

class TwitterDB():
    def __init__(self, *args, **kwargs):
        self.spark = SparkSession.builder \
                        .appName("twitter_analyzer") \
                        .config("spark.ui.showConsoleProgress","false") \
                        .master("local").getOrCreate()

        self.spark.sparkContext.setLogLevel("ERROR")

    def test(self):
        df = self.spark.read.json("hdfs://172.17.0.2:9000/input/twitter/tweets.json")
        rdd = df.rdd
        rdd = rdd.filter(lambda x: "test" in x['text']).map(lambda x: x['text'])

        return rdd.first()

    def search(self, query):
        print('SEARCH QUERY : '+query)
        #Creation d'une DATAFRAME (une « table ») à partir du fichier JSON se trouvant dans HDFS
        #Il faut remplacer le chemin par le fichier sous hdfs
        #on pourra le remplacer au début par un simple fichier local

        df = self.spark.read.json("hdfs://172.17.0.2:9000/input/twitter/tweets.json")
        rdd = df.rdd
        res = {}
        #Filter twitter text message containing query string
        rdd = rdd.filter(lambda x: query in x['text'])

        # Remove empty hashtags
        hashtags = rdd.filter(lambda x: x['entities']['hashtags'] != [])
        # Get the list of hashtags
        hashtags = hashtags.flatMap(lambda x: x['entities']['hashatags'])
        hashtags = hashtags.map(lambda x: (x['text'], 1))
        # Reduce by key to count each hashtag
        hashtags = hashtags.reduceByKey(lambda x, y: x + y)

        #Remove unknown places
        places = rdd.filter(lambda x: x['place'] != None)
        #Get list of contry_code
        places = places.map(lambda x: (x['place']['country_code'],1))
        #Count number of tweet in each country_code
        places = places.reduceByKey(lambda x,y: x+y)

        res['count'] = rdd.count()
        res['hashtags'] = hashtags.collect()
        res['places'] = places.collect()

        return res

#Standelone Test
if __name__ == "__main__":
    t = TwitterDB()
    s = t.test()
    print(s)