from cassandra.cluster import Cluster

# Configuración de la conexión a Cassandra
cluster = Cluster(['cassandra_db'])  # Cambia esto según tu configuración
session = cluster.connect()

# Crear keyspace
create_keyspace_query = """
    CREATE KEYSPACE IF NOT EXISTS cocktails
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
"""
session.execute(create_keyspace_query)

# Usar el keyspace
session.set_keyspace('cocktails')

# Crear tabla popular_drinks
create_popular_drinks_query = """
    CREATE TABLE IF NOT EXISTS popular_drinks (
        idDrink INT,
        strDrink VARCHAR,
        strCategory VARCHAR,
        strAlcoholic VARCHAR,
        strGlass VARCHAR,
        PRIMARY KEY (idDrink, strDrink)
    );
"""
session.execute(create_popular_drinks_query)

# Crear tabla drinks
create_drinks_query = """
    CREATE TABLE IF NOT EXISTS drinks (
        idDrink INT,
        strDrink VARCHAR,
        strCategory VARCHAR,
        strAlcoholic VARCHAR,
        strGlass VARCHAR,
        PRIMARY KEY (idDrink, strDrink)
    );
"""
session.execute(create_drinks_query)

# Poblar la tabla popular_drinks desde el archivo CSV
popular_drinks_csv_file = 'popular_drinks.csv'
with open(popular_drinks_csv_file, 'r') as file:
    for i, line in enumerate(file):
        if i != 0:
            idDrink, strDrink, strCategory, strAlcoholic, strGlass = line.strip().split(',')
            idDrink = int(idDrink)
            session.execute(
                """
                INSERT INTO popular_drinks (idDrink, strDrink, strCategory, strAlcoholic, strGlass) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (idDrink, strDrink, strCategory, strAlcoholic, strGlass)
            )  

# Poblar la tabla drinks desde el archivo CSV
drinks_csv_file = 'drinks.csv'
with open(drinks_csv_file, 'r') as file:
    for i,line in enumerate(file):
        if i != 0:
            idDrink, strDrink, strCategory, strAlcoholic, strGlass = line.strip().split(',')
            idDrink = int(idDrink)
            session.execute(
                """
                INSERT INTO drinks (idDrink, strDrink, strCategory, strAlcoholic, strGlass) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (idDrink, strDrink, strCategory, strAlcoholic, strGlass)
            ) 

# Cerrar la conexión
cluster.shutdown()
print("Cassandra created successfully")