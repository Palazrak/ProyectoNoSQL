##Proyecto Final NoSQL Otoño 2023

Para la clase de Bases de Datos No Relacionales se nos pidió elaborar un proyecto que integrara los siguientes elementos:
- Realizar solicitudes a una API
- Insertar las solicitudes a un MongoDB, que servirá como un data lake
- A partir del data lake obtener consultas que insertar en otras dos bases de datos: una de Cassandra y otra de Neo4J
- Incorporar todos los elementos con un docker compose

En este documento explicaremos un poco sobre el funcionamiento del proyecto y algunas consultas prediseñadas para cada una de las bases de datos.

###API utilizada: The Coctail DB

[The Coctail DB](https://www.thecocktaildb.com/) es una base de datos que contiene información sobre 621 bebidas de todo el mundo. A pesar de tener algunos servicios gratuitos, para tener acceso a toda la base de datos es necesario pagar una suscripción en Patreon; una vez pagada la suscripción, obtuvimos una llave privada para hacer solicitudes a la API (por motivos de seguridad, la llave no está incluida en el proyecto).

Un servicio que sí es gratuito es obtener la informacion de una bebida obtenida aleatoriamente. Si nosotros hacemos esto, podemos ver que cada bebida viene con el siguiente formato:
