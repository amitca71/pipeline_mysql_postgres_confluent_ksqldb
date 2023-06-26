# pipeline_mysql_postgres_confluent_ksqldb
The ETL process is based on three major kafka components:

1. kafka broker (and other operational components such as zoo keeper, schema registry and control-center)

2. kafka connect (with source and sink)

3. ksql – kafka component for streams manipulations, that has data transformation capability


The following figure describes the main components of the deployment
![image](https://github.com/amitca71/pipeline_mysql_postgres_confluent_ksqldb/assets/5821916/c48cc112-9560-40dc-9cdd-94599332b1c7)


Kafka- kakfa confluent broker

kafka connect is customized image is built with the rellevant connector (under customized-kafka-connect folder)

Mysql- used as the source for the data (configuration can be seen on file: source.json)

Postgres – used as sink (configuration: jdbc-sink.json)

Minio –used as S3 sink (configuration s3-minio-sink.json)

ksql- confluent ksql (due to lack of time and memory issues, I couldn’t track why cant be seen of control center). 

transformation can be done by gui after system boot on : http://localhost:9021/clusters/c5ziYokZTuO1G9kb8CBZkA/ksql/ksqldb1/editor

other option for transformation can be views on databases or kafka streams implementations, that due to lack of time were not implemented.

consuming system can pull data from postgres, kafka topics (as consuments) or S3



the system is complemented with confluent control center that provides visibility on the clusters (http://localhost:9021/)



Execution instructions:

pre requisite:

- docker and docker-compose installed on the running machine

script execution: execute  ./boot.sh 

manual execution:

. ./.env

docker-compose up -d

# see kafka confluent control-center on http://localhost:9021/


# Start PostgreSQL connector

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d @jdbc-sink.json


# Start S3 minio connector

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d @s3-minio-sink.json


# Start MySQL connector

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d @source.json


```


Check contents of the MySQL database:


```shell

docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER -p$MYSQL_PASSWORD inventory -e "select * from customers"'

+------+------------+-----------+-----------------------+

| id | first_name | last_name | email |

+------+------------+-----------+-----------------------+

| 1001 | Sally | Thomas | sally.thomas@acme.com |

| 1002 | George | Bailey | gbailey@foobar.com |

| 1003 | Edward | Walker | ed@walker.com |

| 1004 | Anne | Kretchmar | annek@noanswer.org |

+------+------------+-----------+-----------------------+

```


Verify that the PostgreSQL database has the same content:


```shell

docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB -c "select * from customers"'

last_name | id | first_name | email

-----------+------+------------+-----------------------

Thomas | 1001 | Sally | sally.thomas@acme.com

Bailey | 1002 | George | gbailey@foobar.com

Walker | 1003 | Edward | ed@walker.com

Kretchmar | 1004 | Anne | annek@noanswer.org

(4 rows)

```





#### New record


Insert a new record into MySQL;

```shell

docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER -p$MYSQL_PASSWORD inventory'

mysql> insert into customers values(default, 'John', 'Doe', 'john.doe@example.com');

Query OK, 1 row affected (0.02 sec)

```


Verify that PostgreSQL contains the new record:


```shell

docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB -c "select * from customers"'

last_name | id | first_name | email

-----------+------+------------+-----------------------

...

Doe | 1005 | John | john.doe@example.com

(5 rows)

```


#### Record update


Update a record in MySQL:


```shell

mysql> update customers set first_name='Jane', last_name='changed' where last_name='Thomas';

Query OK, 1 row affected (0.02 sec)

Rows matched: 1 Changed: 1 Warnings: 0

```


Verify that record in PostgreSQL is updated:


```shell

docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB -c "select * from customers"'

last_name | id | first_name | email

-----------+------+------------+-----------------------

...

Roe | 1005 | Jane | john.doe@example.com

(5 rows)

```


#### Record delete


Delete a record in MySQL:


```shell

mysql> delete from customers where email='john.doe@example.com';

Query OK, 1 row affected (0.01 sec)

```


Verify that record in PostgreSQL is deleted:


```shell

docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB -c "select * from customers"'

last_name | id | first_name | email

-----------+------+------------+-----------------------

...

(4 rows)

```


As you can see there is no longer a 'Jane Doe' as a customer.


Records can also be seen under buckets/topics

This can be be used as a raw data to lakehouse (e.g. can add spark that reads the data and transform it to parquet/delta, etc...)

