# Aeroflot

To run postgres docker image:
```
$ docker pull postgres:16.2
$ docker run -itd -e POSTGRES_USER=aeroflot -e POSTGRES_PASSWORD=test -p 5432:5432 -v ./database/data:/var/lib/postgresql/data --name postgresql postgres:16.2
```

To query postgres from console:
```
$ sudo apt-get install postgresql-client
$ PGPASSWORD=test psql -h localhost -p 5432 -U aeroflot
```

### Start-up
```
$ git clone https://github.com/Gelassen/Aeroflot.git
$ cd Aeroflot/pilot && docker-compose up
```

Endpoint of database server:
```
$ docker container ps
$ docker inspect <container id> | grep IPAddress
```

### Notes
1. .env files SHOULD NOT be checked-in in the repository. The only reason why they are here is demo purpose and test nature of this config. For Github CI special secrets section should be used.