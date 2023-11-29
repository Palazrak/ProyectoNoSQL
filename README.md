# Proyecto Final NoSQL Otoño 2023

Para la clase de Bases de Datos No Relacionales se nos pidió elaborar un proyecto que integrara los siguientes elementos:
- Realizar solicitudes a una API
- Insertar las solicitudes a un MongoDB, que servirá como un data lake
- A partir del data lake obtener consultas que insertar en otras dos bases de datos: una en Cassandra y otra en Neo4j
- Incorporar todos los elementos dentro de un docker compose

En este documento explicaremos un poco sobre el funcionamiento del proyecto, los requisitos para su ejecución y algunas consultas prediseñadas para cada una de las bases de datos.

### Sobre la API utilizada: The Cocktail DB

[The Coctail DB](https://www.thecocktaildb.com/) es una base de datos que contiene información sobre 621 bebidas de todo el mundo. A partir de su API obtuvimos la información sobre las 621 bebidas disponibles, cuáles de éstas son las más populares y una lista con todos los ingredientes disponibles. Estas consultas nos sirvieron para crear las tres bases de datos.

A pesar de tener algunos servicios gratuitos, para tener acceso a toda la base de datos es necesario pagar una suscripción en Patreon; una vez pagada la suscripción, obtuvimos una llave privada para hacer solicitudes a la API, que manejamos como una variable de entorno en un archivo .env (por motivos de seguridad, no está contenido en este repositorio).

## Antes de comenzar: cómo inicializar el proyecto


## MongoDB

Una vez hechas las consultas a la API de The Cocktail DB, insertamos los datos en Mongo utilizando un script de Python. Al momento de guardar la información, creamos 4 colecciones:
- Una llamada "raw", en la cual se guardaron los datos sin formato para facilitar la creacion de la base de datos en Cassandra
- Una llamada "popular_drinks", en la cual se guardó la consulta de las bebidas más populares según la API. Los datos de esta colección tamibién se guardaron sin formato, por el mismo motivo que la coleccion "raw"
- Una llamada "ingredients", que contiene todos los ingredientes disponibles en la API
- Una llamada "drinks", en la cual se guardaron los elementos con un formato que facilitara la lectura en Mongo

Tomando esto en cuenta, la colección que tenemos planeado que sea utilizada es la colección "drinks", ya que las otras solo fueron utilizadas para la creación de las demás (no las eliminamos para demostrar que fue parte del proceso de creación).

### Acceder al contenedor de Mongo

Para acceder al contenedor de mongo del Docker compose se necesita correr el siguiente comando:
```bash
docker exec -it mongo_lake mongosh
```
Una vez hecho esto, es necesario activar la base de datos "cocktails"
```
use cocktails
```
Ahora sí, podemos empezar a usar el Mongo

### Consultas al Mongo

Para probar la base de datos de Mongo, diseñamos las siguientes consultas:

## Cassandra

### Acceder al contenedor de Cassandra

Para acceder al contenedor de mongo del Docker compose se necesita correr el siguiente comando:
```bash
docker exec -it cassandra_db cqlsh
```
Una vez hecho esto, es necesario activar el keyspace "cocktails"
```
use cocktails;
```
Ahora sí, podemos empezar a usar el Cassandra

### Consultas al Cassandra 

## Neo4J

### Acceder al contenedor de Neo4j

A diferencia de las otras bases de datos usadas, para Neo4j aprovecharemos la increible visualización que tiene y la abriremos en nuestro local. Para esto, es necesario que escribamos en el buscador:
```
localhost:7474/browser/
```
Esto nos mostrará al Neo4j que tenemos corriendo en nuestro docker. Para terminar de entrar, no hace falta llenar ni username ni password. Basta con darle al botón de "Connect"

Una vez dentro, podemos empezar a hacer nuestras consultas

### Consultas al Neo4j

1. Encuentra todas las bebidas que contengan un ingrediente específico: 
```
MATCH (d:Drink)-[:CONTAINS]->(i:Ingredient {name: 'Gin'})
RETURN d.name AS Drink
```

2. Listar todos los ingredientes que contiene una bebida específica:
```
MATCH (d:Drink {name: 'A1'})-[:CONTAINS]->(i:Ingredient)
RETURN i.name AS Ingredient
```

3. Encuentra a todas las bebidas y sus ingredientes:
```
MATCH (d:Drink)-[:CONTAINS]->(i:Ingredient)
RETURN d.name AS Drink, collect(i.name) AS Ingredients
ORDER BY d.name
```

4. Encuentra a los ingredientes más usados al preparar bebidas
```
MATCH (:Drink)-[:CONTAINS]->(i:Ingredient)
RETURN i.name AS Ingredient, count(*) AS NumberOfDrinks
ORDER BY NumberOfDrinks DESC
LIMIT 10
```