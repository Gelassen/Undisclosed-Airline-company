# Aeroflot

### Start-up
```
$ git clone https://github.com/Gelassen/Aeroflot.git
$ cd Aeroflot/pilot && docker-compose up
$ docker-compose up
```

Command to run to enable Kafka connection:

It should be done automatically by mounting ```postgres-sink-config.json```, but it is not and this issue has not been figured out yet, REST API call as an alternative approach should be used instead:
```
curl -i -X PUT -H  "Content-Type:application/json" \
    172.16.254.4:8083/connectors/postgres-sink-connector/config \
    -d '{
      "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
      "tasks.max": "1",
      "topics": "Inventory",
      "connection.url": "jdbc:postgresql://postgres:5432/aeroflot",
      "connection.user": "aeroflot",
      "connection.password": "test",
      "auto.create": "true",
      "insert.mode": "upsert",
      "pk.mode": "record_value",
      "pk.fields": "flight,flight_booking_class",
	    "driver.class": "org.postgresql.Driver",
	    "plugin.path": "/usr/share/java,/usr/share/confluent-hub-components",
	    "errors.log.enable": "true",
      "errors.log.include.messages": "true"
    }'
```
Verify Kafka config:
```
curl -X GET http://172.16.254.4:8083/connectors/postgres-sink-connector/config
```

Till this moment Kafka queue should be established. To run Consumer and Producer, execute commands below in two separate terminals:
```
$ source venv/bin/activate && python consumer.py
$ source venv/bin/activate && python producer.py
```

Check exported from Kafka data in database either directly over ```psql``` or over ```REST```

### Manual connection to docker postgres
Endpoint of database server:
```
$ docker container ps
$ docker inspect <container id> | grep IPv4Address
$ docker exec -it <container_id> bash
```
\l to display all schemas

\dt to display all tables. 

Double commas should be placed around table names.

To query postgres from console:
```
$ sudo apt-get install postgresql-client
$ PGPASSWORD=test psql -h localhost -p 5432 -U aeroflot
```

### Docker hot commands
To remove ALL images:
```
$ docker system prune -a
```
To remove ALL volumes:
```
$ docker volume rm -f $(docker volume ls -q)
```

### Others
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

### Notes
1. .env files SHOULD NOT be checked-in in the repository. The only reason why they are here is demo purpose and test nature of this config. For Github CI special secrets section should be used.
2. ```KRaft``` is a preferable mechanism to use instead of ```Zookeeper```, although the current Kafka release (apache/kafka:3.7.0) still rely on ```Zookeeper```. We have to use ```Zookeeper``` right now, but in the next release ```Kafka 4.0``` it is going to be removed. 
3. Pure implementation of ```Kafka``` and ```Kafka Connect``` faced with unresolved yet issues between ```KRaft``` and ```Zookeeper``. For mre details, please refer https://stackoverflow.com/questions/78472810/how-to-run-pure-kafka-and-kafka-connect-over-docker-compose#78472810
4. External to docker Kafka producers using docker hostnames instead of direct IP addresses. They are not resolved automatically and possible workarounds are to try to modify hosts file on the Host machine or replace hostnames by direct ip addresses in advertise listeners properties
5. Confluent still relies on CLASSPATH in some cases, despite on it is a legacy mechanism. For postgres sink connector I had to define it in the config