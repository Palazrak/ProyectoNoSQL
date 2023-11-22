import requests
import pymongo
from dotenv import load_dotenv 
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

url = f"https://www.thecocktaildb.com/api/json/v2/{API_KEY}/search.php?f="

client = pymongo.MongoClient("mongodb://mongo_lake:27017")
db = client["cocktails"]
collection_formatted = db["drinks"]
collection_raw = db["raw"]

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y', 'z']
for letter in letters:
    print(letter)
    
    # Hacer la solicitud a la API
    response = requests.get(url + str(letter)).json()
    
    # Iterar sobre las bebidas y crear listas para strInstructions, strIngredient y strMeasure
    for drink in response["drinks"]:
        
        # Primero voy a guardar las bebidas sin formato; esto para poder pasar a forma tabular con mayor facilidad

        collection_raw.insert_one(drink)
    
    # Ahora, le doy un mejor formato a las bebidas
        
        # Obtener siempre 'strInstructions' y eliminar su clave del diccionario original
        en_instructions = drink.get("strInstructions")
        if en_instructions is not None:
            del drink["strInstructions"]
        else:
            en_instructions = ""

        # Guarda las instrucciones de las bebidas dentro de un diccionario. Solo almacena los datos no nulos
        instructions = {"EN": en_instructions}
        for lang in ["ES", "DE", "FR", "IT", "ZH-HANS", "ZH-HANT"]:
            lang_instructions = drink.get(f"strInstructions{lang}")
            if lang_instructions is not None:
                instructions[lang] = lang_instructions
            del drink[f"strInstructions{lang}"]  

        ingredients = [drink[key] for key in drink if key.startswith("strIngredient") and drink[key] is not None]
        measures = [drink[key] for key in drink if key.startswith("strMeasure") and drink[key] is not None]
        
        # Crear un nuevo diccionario limpio sin las claves que ya se han procesado
        clean_drink = {key: value for key, value in drink.items() if key not in {"strIngredient", "strMeasure"}}
        
        # Eliminar las claves "strIngredient" y "strMeasure" del rango 1-15, ya que están dentro de un diccionario
        for num in range(1, 16):
            ingredient_key = f"strIngredient{num}"
            measure_key = f"strMeasure{num}"
            if ingredient_key in clean_drink:
                del clean_drink[ingredient_key]
            if measure_key in clean_drink:
                del clean_drink[measure_key]
        
        # Agregar las listas y el diccionario de instrucciones al nuevo diccionario
        clean_drink["instructions"] = instructions
        clean_drink["ingredients"] = ingredients
        clean_drink["measures"] = measures
        
        # Insertar cada bebida individual en MongoDB
        collection_formatted.insert_one(clean_drink)

# Ahora crearé una colección para guardar los ingredientes
collection_ingredients = db["ingredients"]
url_ingredients = f"https://www.thecocktaildb.com/api/json/v2/{API_KEY}/list.php?i=list"
response_ingredients = requests.get(url_ingredients).json()

for ingredient in response_ingredients["drinks"]:
    collection_ingredients.insert_one(ingredient)
    
# Por último, guardar una colección adicional de "most popular drinks". Esto servirá para el Cassandra

collection_popular_drinks = db["popular_drinks"]
url_popular_drinks = f"www.thecocktaildb.com/api/json/v2/{API_KEY}/popular.php"
response_popular_drinks = response_ingredients = requests.get(url_popular_drinks).json()

for drink in response_popular_drinks["drinks"]:
    collection_popular_drinks.insert_one(drink)