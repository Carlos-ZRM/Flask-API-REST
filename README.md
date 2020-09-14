# Ejecutar contenedores sin Docker  compose 


# Mongo 
``` bash
docker run -d --name some-mongo -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    mongo
```

# Flask 
## Build imagen 
```
docker build -t flask-rest Flask/
``` 

```
docker run -dt --name some-flask -p 5000:5000 \
    -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    -e MONGODB_HOST=some-mongo \
    --link some-mongo:MONGODB_HOST \
    -v $(pwd):/python:z \
    --hostname  some-flask \
    flask-rest
```
# Kong 
``kong config -c /usr/local/kong/.kong_env parse /usr/local/kong/declarative/kong.yml``
# Uso de la API 

# Metodos GET 
``` bash 
 curl -i localhost:5000/
 curl -i localhost:5000/registro
```

# Metodo POST
```
curl --header "Content-Type: application/json"   --request POST   --data '{"Pokemon": "Squirtle","Carrera": "ISC", "Semestre":1   }' -i   http://localhost:5000/registro 
```

# Metodo delete 

```
curl --header "Content-Type: application/json"   --request DELETE   --data '{"database": "IshmeetDB","collection": "people","Filtro": {"Pokemon": "Squirtle"}}' -i   http://localhost:5000/registro
``` 

# Metodo PUT
```
curl --header "Content-Type: application/json"   --request PUT   --data '{"Filtro": {"Pokemon": "Squirtle"},"Datos": {"Carrera": "IIA","Semestre": 1}}' -i   http://localhost:5000/registro

```

https://github.com/ishmeet1995/PublicProjects

 
