# Proyecto Final NoSQL Otoño 2023

Para la clase de Bases de Datos No Relacionales se nos pidió elaborar un proyecto que integrara los siguientes elementos:
- Realizar solicitudes a una API.
- Insertar las solicitudes a un MongoDB, que servirá como un data lake.
- A partir del data lake obtener consultas que insertar en otras dos bases de datos: una en Cassandra y otra en Neo4j.
- Incorporar todos los elementos dentro de un docker compose.

En este documento explicaremos un poco sobre el funcionamiento del proyecto, los requisitos para su ejecución y algunas consultas prediseñadas para cada una de las bases de datos.

## Sobre la API utilizada: The Cocktail DB

[The Cocktail DB](https://www.thecocktaildb.com/) es una base de datos que contiene información sobre 621 bebidas de todo el mundo. A partir de su API obtuvimos la información sobre las 621 bebidas disponibles, cuáles de éstas son las más populares y una lista con todos los ingredientes disponibles. Estas consultas nos sirvieron para crear las tres bases de datos.

A pesar de tener algunos servicios gratuitos, para tener acceso a toda la base de datos es necesario pagar una suscripción en Patreon; una vez pagada la suscripción, obtuvimos una llave privada para hacer solicitudes a la API, que manejamos como una variable de entorno en un archivo .env (por motivos de seguridad, no está contenido en este repositorio).

## Antes de comenzar: Cómo inicializar el proyecto

Para poder ejecutar el proyecto como es debido, es necesario seguir las siguientes instrucciones:
1. Hacer un clon de este repositorio. La carpeta del repositorio se llama "ProyectoNoSQL".
2. Dentro de la carpeta del repositorio, crear un archivo .env que contenga una llave para la API.
3. Descargar los 4 archivos .csv contenidos en el siguiente drive de google (Haz click [aquí](https://drive.google.com/drive/folders/1YGicWeAc83kDsr9gNXHlb2ak2bhZonGS?usp=sharing)) y **guardarlos en la carpeta "data" que viene en el repositorio**. Es importante guardar los .csv en esta carpeta porque si no están en esta ubicación, el proyecto no funcionará.
4. Asegurate de que el daemon de docker esté corriendo.
5. En la carpeta del repositorio, escribir el siguiente comando en la terminal:
    ```bash
    docker compose up -d
    ```
6. Esperar alrededor de 2 minutos para garantizar que todo se cree correctamente.
7. Comprobar que los contenedores estén corriendo con el siguiente comando:
    ```bash
    docker ps
    ```

Aquí podremos ver toda la información de los contenedores que están corriendo, principalmente los puertos que utilizan y los nombres de los contenedores.

### Sobre los .csv utilizados: Cómo los generamos

Los .csv que están en ese drive no aparecieron de la nada. Fueron creados en una etapa temprana del proyecto, en la que solo estaba implementada la funcionalidad del MongoDB.

Para obtener los archivos, ésto fue lo que hicimos:
1. Entramos al bash del contenedor de Mongo
    ```
    docker exec -it mongo_lake /bin/bash
    ```
2. Dentro del bash de Mongo, corrimos los siguientes 4 mongoexports:
    ```
    mongoexport --db cocktails --collection raw --type=csv --fields idDrink,strDrink,strCategory,strAlcoholic,strGlass --out /data/db/drinks.csv
    mongoexport --db cocktails --collection popular_drinks --type=csv --fields idDrink,strDrink,strCategory,strAlcoholic,strGlass --out /data/db/popular_drinks.csv
    mongoexport --db cocktails --collection ingredients --type=csv --fields strIngredient1 --out /data/db/ingredients.csv
    mongoexport --db cocktails --collection drinks --type csv --fields strDrink,strCategory,strAlcoholic,strGlass,ingredients --out /data/db/drinks_filtered.csv
    ```
3. Salimos del bash de Mongo:
    ```
    exit
    ```
4. Fuera del bash de Mongo, corrimos los siguientes comandos:
    ```
    docker cp mongo_lake:/data/db/drinks.csv ./data
    docker cp mongo_lake:/data/db/popular_drinks.csv ./data
    docker cp mongo_lake:/data/db/ingredients.csv ./data
    docker cp mongo_lake:/data/db/drinks_filtered.csv ./data
    ```
Esto guarda los csv en la carpeta "data" del repositorio, con los cuales, en la siguiente etapa del proyecto, construimos el Cassandra y el Neo4j. No incluímos los csv en el repositorio para que no fuera tan pesado (y por instrucción del profesor).

Es importante recalcar que este procedimiento puede replicarse para comprobar que en efecto son los mismos .csv que se descargaron, pero para que el proyecto ejecute es necesario primero descargarlos a la carpeta "data". Ya después se puede jugar con generar los .csv y verificar que sean los mismos.

Ahora sí, podemos entrar de lleno con el resto del proyecto.

## MongoDB

Una vez hechas las consultas a la API de The Cocktail DB, insertamos los datos en Mongo utilizando un script de Python. Al momento de guardar la información, creamos 4 colecciones:
- Una llamada "raw", en la cual se guardaron los datos sin formato para facilitar la creacion de la base de datos en Cassandra
- Una llamada "popular_drinks", en la cual se guardó la consulta de las bebidas más populares según la API. Los datos de esta colección tamibién se guardaron sin formato, por el mismo motivo que la coleccion "raw"
- Una llamada "ingredients", que contiene todos los ingredientes disponibles en la API
- Una llamada "drinks", en la cual se guardaron los elementos con un formato que facilitara la lectura en Mongo

Tomando esto en cuenta, la colección que tenemos planeado que sea utilizada es la colección "drinks", ya que las otras solo fueron utilizadas para la creación de las demás (no las eliminamos para demostrar que fue parte del proceso de creación).

Aquí hay un ejemplo de cómo se guardan los elementos en la colección "drinks":
```
{
    _id: ObjectId("65584cb1247634a5a840c451"),
    idDrink: '17222',
    strDrink: 'A1',
    strDrinkAlternate: null,
    strTags: null,
    strVideo: null,
    strCategory: 'Cocktail',
    strIBA: null,
    strAlcoholic: 'Alcoholic',
    strGlass: 'Cocktail glass',
    strDrinkThumb: 'https://www.thecocktaildb.com/images/media/drink/2x8thr1504816928.jpg',
    strImageSource: null,
    strImageAttribution: null,
    strCreativeCommonsConfirmed: 'No',
    dateModified: '2017-09-07 21:42:09',
    instructions: {
        EN: 'Pour all ingredients into a cocktail shaker, mix and serve over ice into a chilled glass.',
        ES: 'Vierta todos los ingredientes en una coctelera, mezcle y sirva con hielo en un vaso frío.',
        DE: 'Alle Zutaten in einen Cocktailshaker geben, mischen und über Eis in ein gekühltes Glas servieren.',
        IT: 'Versare tutti gli ingredienti in uno shaker, mescolare e servire con ghiaccio in un bicchiere freddo.'
    },
    ingredients: [ 'Gin', 'Grand Marnier', 'Lemon Juice', 'Grenadine' ],
    measures: [ '1 3/4 shot ', '1 Shot ', '1/4 Shot', '1/8 Shot' ]
}
```
Para cada elemento puede variar el contenido de "instructions", ya que no todas las bebidas contienen las instrucciones en todos los idiomas disponibles, los cuales pueden ser:
- EN para Inglés
- ES para Español
- DE para Alemán
- IT para Italiano
- FR para Francés
- ZH-HANS para Chino simplificado
- ZH-HANT para Chino tradicional

Además, "ingredients" y "measures" están relacionados entre sí: cada posicion de "ingredients" corresponde a la misma posicion en "measures".

Es importante notar que contiene varios nulos. Estos podrían ser importantes por temas de derechos de autr o por otro tipo de análisis, y no queremos perder esa información.

### Accedediendo al contenedor de Mongo

Para acceder al contenedor de mongo del Docker compose se necesita correr el siguiente comando:
```bash
docker exec -it mongo_lake mongosh
```
Una vez hecho esto, es necesario activar la base de datos "cocktails".
```
use cocktails
```

### Consultas al Mongo

1. Obtener las instrucciones de como preparar las 20 bebidas más importantes
    ```javascript
    db.popular_drinks.find({},{'_id':0, 'idDrink':1, 'strDrink':1, 'strInstructions':1})
    ```
2. ¿Cuáles son las bebidas que contienen mayor número de ingredientes distintos?
    ```javascript
    db.drinks.aggregate([
        {$project: {_id: 1, strDrink: 1, ingredientCount: { $size: "$ingredients" }}},
        {$sort: {ingredientCount: -1}},
        {$limit: 10}
    ])
    ```
3. ¿Cuáles son los diferentes tipos de Mojitos que hay en la base de datos?
    ```javascript
    db.drinks.find({'strDrink':/^Mojito/})
    ```
4. Obtener la informacion de las bebidas que comiencen con una letra dada
    ```javascript
    db.drinks.find({'strDrink':/^D/})
    ```

## Cassandra

Dentro del cassandra creamos dos tablas en el mismo keyspace:
- Una llamada "drinks", en el que viene la información de todas las bebidas.
- Otra llamada "popular_drinks", en el que viene la informacion de las bebidas mas populares según la API.

A la hora de crear el Cassandra, de todos los campos que contiene cada bebida solo elegimos utilizar los siguientes:
- El ID de la bebida en la API
- El nombre de cada bebida
- Su categoría (coctel, shot, shake, chocolate, café, té, etc)
- Si la bebida es alcohólica, no alcohólica o contiene alcohol opcional
- El tipo de copa o vaso en el que se sirve

Utilizamos unicamente estos campos ya que consideramos que estos son los campos normalmente más buscados al hacer una consulta sobre una bebida. Para obtener el resto de la información, conviene obtenerla haciendo consultas del Mongo.

### Accedediendo al contenedor de Cassandra

Para acceder al contenedor de mongo del Docker compose se necesita correr el siguiente comando:
```bash
docker exec -it cassandra_db cqlsh
```
Una vez hecho esto, es necesario activar el keyspace "cocktails".
```
use cocktails;
```

### Consultas al Cassandra 

1. Información de las 20 bebidas mas populares según la API
    ```
    SELECT * FROM popular_drinks;
    ```
2. ¿Cuántas bebidas hay que sean de categoría 'Cocktail'?
    ```
    SELECT COUNT(*) as count
    FROM drinks
    WHERE strcategory = 'Cocktail'
    ALLOW FILTERING;
    ```
3. ¿Cuántas bebidas hay que se sirvan en vaso de tipo 'Old-fashioned glass'?
    ```
    SELECT COUNT(*) as count
    FROM drinks
    WHERE strglass = 'Old-fashioned glass'
    ALLOW FILTERING;
    ```
4. ¿Cuántas bebidas son alcohólicas, no alcohólias o contienen alcohol opcional?
    ```
    SELECT COUNT(*) as count
    FROM drinks
    WHERE stralcoholic = 'Alcoholic'
    ALLOW FILTERING;
    ```
    ```
    SELECT COUNT(*) as count
    FROM drinks
    WHERE stralcoholic = 'Optional alcohol'
    ALLOW FILTERING;
    ```
    ```
    SELECT COUNT(*) as count
    FROM drinks
    WHERE stralcoholic = 'Optional alcohol'
    ALLOW FILTERING;
    ```
Las consultas anteriores podrían usarse con diferentes opciones de "strcategory" y "strglass". Para ver cuáles son todas las opciones, puede o hacerse una consulta gratuita a la API en la que se listen todas las opciones o se puede hacer un aggregate en el Mongo. 

## Neo4J

Por la propia naturaleza de la base de datos que utilizamos, consideramos que para el Neo4j sería una buena idea tener nodos para bebidas y para ingredientes. Así, la relación "contiene" nos ayudaría a hacer las consultas deseadas.

Para esto utilizamos 3 scripts de Python (pudo haber sido uno, pero preferimos separarlos por legibilidad): uno insertó a los ingredientes, otro insertó a las bebidas y el último creó la relación "contiene" para conectar los nodos entre sí.

### Accedediendo al contenedor de Neo4j

A diferencia de las otras bases de datos usadas, para Neo4j aprovecharemos la increible visualización que tiene y la abriremos en nuestro local. Para esto, es necesario que escribamos en el buscador:
```
localhost:7474/browser/
```
Para terminar de entrar, **no hace falta llenar los campos Username y Password**. Basta con darle al botón de "Connect", ya que no creamos el contenedor ni con usuario ni con contraseña.

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