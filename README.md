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
```javascript
[{"drinks":
    [{
        _id: ObjectId("65579e8cfd989dddf62cf81f"),
        idDrink: '15427',
        strDrink: 'Grand Blue',
        strDrinkAlternate: null,
        strTags: null,
        strVideo: null,
        strCategory: 'Ordinary Drink',
        strIBA: null,
        strAlcoholic: 'Alcoholic',
        strGlass: 'Old-fashioned glass',
        strInstructions: 'Serve in an old fashioned glass.',
        strInstructionsES: null,
        strInstructionsDE: 'In einem old-fashioned Glas servieren.',
        strInstructionsFR: null,
        strInstructionsIT: 'Versare tutti gli ingredienti in un bicchiere, mescola bene.',
        'strInstructionsZH-HANS': null,
        'strInstructionsZH-HANT': null,
        strDrinkThumb: 'https://www.thecocktaildb.com/images/media/drink/vsrsqu1472761749.jpg',
        strIngredient1: 'Malibu rum',
        strIngredient2: 'Peach schnapps',
        strIngredient3: 'Blue Curacao',
        strIngredient4: 'Sweet and sour',
        strIngredient5: null,
        strIngredient6: null,
        strIngredient7: null,
        strIngredient8: null,
        strIngredient9: null,
        strIngredient10: null,
        strIngredient11: null,
        strIngredient12: null,
        strIngredient13: null,
        strIngredient14: null,
        strIngredient15: null,
        strMeasure1: '1 1/2 cl ',
        strMeasure2: '1 1/2 cl ',
        strMeasure3: '1 1/2 cl ',
        strMeasure4: '3 cl ',
        strMeasure5: null,
        strMeasure6: null,
        strMeasure7: null,
        strMeasure8: null,
        strMeasure9: null,
        strMeasure10: null,
        strMeasure11: null,
        strMeasure12: null,
        strMeasure13: null,
        strMeasure14: null,
        strMeasure15: null,
        strImageSource: null,
        strImageAttribution: null,
        strCreativeCommonsConfirmed: 'No',
        dateModified: '2016-09-01 21:29:09'
    }]
}]
```
Como podemos ver, este formato es bastante ineficiente. Con el mismo script de python con el que hicimos las solicitudes a la API, dimos el siguiente formato a los resultados de la API:
```javascript
[{
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
}]
```
Así, metimos a los ingredientes y sus medidas en listas, que es una forma un poco mas intuitiva. También creamos un diccionario de instrucciones con los diferentes idiomas en los que vienen las instrucciones (en total son 7 idiomas diferentes).