# Aeroflot

To run postgres docker image:
```
$ docker pull postgres:16.2
$ docker run -itd -e POSTGRES_USER=aeroflot -e POSTGRES_PASSWORD=test -p 5432:5432 -v ./database/data:/var/lib/postgresql/data --name postgresql postgres:16.2
```

To run Kafka:
```
$ docker pull apache/kafka:3.7.0
$ docker run -p 9092:9092 apache/kafka:3.7.0
```

To connect to the shell and execute shell command:
```
$ docker container ps 
$ docker exec -it <container_id> /bin/sh
(shell) $ ./kafka-topics.sh --create --topic messages --bootstrap-server localhost:9092
```

### Start-up
```
$ docker-compose up
<!-- $ git clone https://github.com/Gelassen/Aeroflot.git
$ cd Aeroflot/pilot && docker-compose up -->
```

Endpoint of database server:
```
$ docker container ps
$ docker inspect <container id> | grep IPAddress
```

### Manual connection to docker postgres
```
$ docker container ps
$ docker exec -it <container_id> bash
```
\l to display all the schema

\dt to display all tables. 

To query postgres from console:
```
$ sudo apt-get install postgresql-client
$ PGPASSWORD=test psql -h localhost -p 5432 -U aeroflot
```

### Notes
1. .env files SHOULD NOT be checked-in in the repository. The only reason why they are here is demo purpose and test nature of this config. For Github CI special secrets section should be used.
2. ```KRaft``` is a preferable mechanism to use instead of ```Zookeeper```, although the current Kafka release (apache/kafka:3.7.0) still rely on ```Zookeeper```. We have to use ```Zookeeper``` right now, but in the next release ```Kafka 4.0``` it is going to be removed. 
3. Pure implementation of ```Kafka``` and ```Kafka Connect``` faced with unresolved yet issues between ```KRaft``` and ```Zookeeper``. For mre details, please refer https://stackoverflow.com/questions/78472810/how-to-run-pure-kafka-and-kafka-connect-over-docker-compose#78472810