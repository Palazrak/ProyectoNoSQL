import csv
from neo4j import GraphDatabase
import json

# Neo4j connection URI and credentials
uri = "bolt://neo4j_db:7687"

# Initialize Neo4j driver
driver = GraphDatabase.driver(uri)

def add_drink(tx, drink_name, category, alcoholic, glass, ingredients):
    query = (
        "CREATE (d:Drink {name: $name, category: $category, alcoholic: $alcoholic, glass: $glass, ingredients: $ingredients})"
    )
    tx.run(query, name=drink_name, category=category, alcoholic=alcoholic, glass=glass, ingredients=ingredients)


def import_drinks(file_path):
    with driver.session() as session:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                drink_name = row['strDrink']
                category = row['strCategory']
                alcoholic = row['strAlcoholic']
                glass = row['strGlass']
                ingredients_str = row['ingredients'].replace("''", '"').replace('""', '"')
                ingredients = json.loads(ingredients_str)
                # Replace write_transaction with execute_write
                session.execute_write(add_drink, drink_name, category, alcoholic, glass, ingredients)

if __name__ == "__main__":
    file_path = 'drinks_filtered.csv'
    import_drinks(file_path)

    print("Drinks imported successfully.")

driver.close()