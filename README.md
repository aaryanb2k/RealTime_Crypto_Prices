# RealTime_Crypto_Prices
This Project is about fetching the top trending CryptoCoins from CoinMarketCap using CoinMarket API along with the their prices,volume in 24hrs and other details and using apache kafka to ingest the data in real time and performing analysis and transformations on the data using Apache spark and storing the streaming data to MongoDb Atlas.

## Installation Steps
1.First we need to install Python(3.7) and java(jdk 8) On the machine for this projet to work appropriately.<br>
2.After the successful installation of above we need to download and <a href="https://kafka.apache.org/">Install Kafka</a> version 2.6.0 with scala version 2.12.<br>
3.Now we Need to Download Apache Spark <a href ="https://spark.apache.org/downloads.html">Apache Spark </a>version 3.3.0 with hadoop version 3.3. Download the <a href="https://github.com/cdarlint/winutils">winUtils file</a> for hadoop version 3.<br>
4.Now we need to setup the path in environment variables for spark and hadoop.<br>
5.Login to your mongo db atlas cluster and get the connection string to connect to the database.<br>

## Deployment Process
### starting up zookeeper server on local host 9092
@@ -25,4 +25,4 @@ Now your kafka Broker is up , you need to deploy the above code in any on the IDE
## Note
1.Since the kafka and mongo db connector are not part of the default spark package you need to define the connectors as the configuration while creating the spark session as mentioned in the code.<br>
2.While working with any IDE you need to import the spark and hadoop environment variable in the project structure under settings.
