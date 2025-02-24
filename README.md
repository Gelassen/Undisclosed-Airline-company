# Undisclosed-Airline-company

<a href="https://gelassen.github.io/blog/2024/11/02/case-study-developing-forecast-sales-system-for-a-major-airline.html">Case study: developing forecast sales system for a major airline</a>

### Start-up
```
$ git clone https://github.com/Gelassen/Aeroflot.git
$ cd Aeroflot/pilot && docker-compose up
```

Command to run to enable Kafka Connect:

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

Producers waits a bit till Kafka and Kafka Connect start up, you will see message from them in the console. 

Check exported from Kafka data in database either directly over ```psql``` or over ```REST```

### REST API

To get all inventories by page:
```
http://172.16.254.6:80/api/v1/inventories
```
Sample reply:
```
[
  {
    "time": 1715565917000,
    "flight": "(TYA) NORDSTAR 403",
    "departure": 1715860453000,
    "flight_booking_class": "S",
    "idle_seats_count": 1
  },
  ...
]
```
To get all inventories by next page:
```
http://172.16.254.6/api/v1/inventories/?page=2
```
Sample reply:
```
[
  {
    "time": 1715322257000,
    "flight": "(LY) EL AL 611",
    "departure": 1715768829000,
    "flight_booking_class": "F",
    "idle_seats_count": 38
  }
  ...
]
```
To search by field (possible fields are ```flight```, ```departure```, ```flight_booking_class```):
```
http://172.16.254.6/api/v1/inventories/search/?flight=(LY) EL AL 611
```
Sample reply:
```
[
  {
    "time": 1715331626000,
    "flight": "(LY) EL AL 611",
    "departure": 1715781020000,
    "flight_booking_class": "L",
    "idle_seats_count": 9
  },
  {
    "time": 1715447991000,
    "flight": "(LY) EL AL 611",
    "departure": 1715740686000,
    "flight_booking_class": "G",
    "idle_seats_count": 6
  }
  ...
]
```

### Dev commands

Verify Kafka config:
```
curl -X GET http://172.16.254.4:8083/connectors/postgres-sink-connector/config
```

To check plain Kafka consumer, run consumer.py:
```
$ python -m venv ./venv
$ pip install -r requirements.txt
$ source venv/bin/activate && python consumer.py
```

#### Manual connection to docker postgres
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

#### Docker hot commands
To remove ALL images:
```
$ docker system prune -a
```
To remove ALL volumes:
```
$ docker volume rm -f $(docker volume ls -q)
```

### Notes
1. .env files SHOULD NOT be checked-in in the repository. The only reason why they are here is demo purpose and test nature of this config. For Github CI special secrets section should be used.
2. ```KRaft``` is a preferable mechanism to use instead of ```Zookeeper```, although the current Kafka release (apache/kafka:3.7.0) still rely on ```Zookeeper```. We have to use ```Zookeeper``` right now, but in the next release ```Kafka 4.0``` it is going to be removed. 
3. Pure implementation of ```Kafka``` and ```Kafka Connect``` faced with unresolved yet issues between ```KRaft``` and ```Zookeeper```. For more details, please refer https://stackoverflow.com/questions/78472810/how-to-run-pure-kafka-and-kafka-connect-over-docker-compose#78472810
4. External to docker Kafka producers using docker hostnames instead of direct IP addresses. They are not resolved automatically and possible workarounds are to try to modify hosts file on the Host machine or replace hostnames by direct ip addresses in advertise listeners properties
5. Confluent still relies on CLASSPATH in some cases, despite on it is a legacy mechanism. For postgres sink connector I had to define it in the config
6. Use docker secrets in production environment https://docs.docker.com/engine/swarm/secrets/
7. Remove all sensitive data like credentials from the repo and replace them. For demo purpose they has been left in repo.
8. Such projects should be covered with integration tests. They has not been added because of demo purpose of this project and not specified requirements for them. 
