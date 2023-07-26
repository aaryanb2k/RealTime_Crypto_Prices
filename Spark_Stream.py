
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField
from pyspark.sql.types import StringType,IntegerType
import json
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import col
from kafka import KafkaConsumer
from pyspark.streaming import StreamingContext
# from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import functions as F
import os
conn = os.environ.get('conn_string')
def write_row(batch_df,batch_id):
    batch_df.write.format("mongo").option('uri',mongo_ip).option("database","Mongo_DB_Demo")\
            .option("collection", "Crypto_DB").mode("append").save()

mongo_ip = conn

#Creating SparkSession with all dependent packages
spark =SparkSession.builder.appName('Spark_Kafka_Stream')\
                            .config("spark.jars.packages","org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1").getOrCreate()

#Defining Schema for our Streaming records
data_schema = StructType([StructField("id",IntegerType(),True),
                         StructField("name",StringType(),True),
                         StructField("symbol",StringType(),True),
                         StructField("date_added",StringType(),True),
                         StructField("price",FloatType(),True),
                         StructField("last_updated",StringType(),True),
                         StructField("volume_24h",FloatType(),True),
                         StructField("market_cap",FloatType(),True)])


df =spark.readStream.format("kafka").option("kafka.bootstrap.servers","localhost:9092").option("subscribe","Popular_Crypto").option("startingoffset","latest").load()

#Fetching Value passed through our Kafka Topic
new_df = df.select(col('value').cast('string'))
final_df=new_df.select(from_json(col('value'),data_schema).alias("Crypto")).select("Crypto.*")

#Writing Data to MongoDB
query = final_df.writeStream.foreachBatch(write_row).start().awaitTermination()

query.awaitTermination()
