import csv
import json
from neo4j import GraphDatabase

# Function to create relationships
def create_relationship(tx, drink_name, ingredients_list):
    query = (
        "MATCH (d:Drink {name: $drink_name}), (i:Ingredient) "
        "WHERE i.name IN $ingredients_list "
        "MERGE (d)-[:CONTAINS]->(i)"
    )
    tx.run(query, drink_name=drink_name, ingredients_list=ingredients_list)

# Connect to Neo4j
driver = GraphDatabase.driver("neo4j://neo4j_db:7687")

# Open the CSV file
with open('drinks_filtered.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    # For each line in the CSV...
    for row in reader:
        # Extract the drink name and the ingredients list
        drink_name = row['strDrink']
        # Ensure the ingredients JSON string is correctly formatted for JSON decoding
        ingredients_str = row['ingredients'].replace("''", '"').replace('""', '"')
        ingredients = json.loads(ingredients_str)  # Now ingredients is a Python list
        
        # Run the transaction for the entire list of ingredients
        with driver.session() as session:
            try:
                # Note: If the execute_write function is deprecated or renamed in your version of neo4j driver,
                # use the recommended function to execute a write transaction.
                session.execute_write(create_relationship, drink_name, ingredients)
            except Exception as e:
                print(f"Failed to create relationship for {drink_name} with ingredients {ingredients}: {str(e)}")

# Close the driver
driver.close()