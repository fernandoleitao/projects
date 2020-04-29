import sqlite3

db_name = "professores.db"
table_name = "professor"

sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY, nome text NOT NULL);"

def createTable(cursor, sql):
    cursor.execute(sql)

def popularDb(cursor, id, nome):
    sql = f"INSERT INTO {table_name} (id, nome) VALUES (?, ?)"
    cursor.execute(sql, (id, nome))
    
def init():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    createTable(cursor, sql_create_table)
    try:
        popularDb(cursor, 1, "Tiago Alexandre")
        popularDb(cursor, 2, "Lucas Mendes")
        popularDb(cursor, 3, "Victor Williams")
    except:
        pass
    cursor.close()
    connection.commit()
    connection.close()
    
init()