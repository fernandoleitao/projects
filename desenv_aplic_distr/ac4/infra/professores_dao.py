import sqlite3
from model.professor import Professor
from contextlib import closing

db_name = "professores.db"
model_name = "professor"

def con():
    return sqlite3.connect(db_name)

def listar():
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT * FROM {model_name}")
        rows = cursor.fetchall()
        registros = []
        for (id, nome) in rows:
            registros.append(Professor.criar({"id": id, "nome": nome}))
        return registros

def consultar(id):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT * FROM {model_name} WHERE id = ?", (int(id),))
        row = cursor.fetchone()
        if row == None:
            return None
        return Professor.criar({"id": row[0], "nome": row[1]})

def cadastrar(professor):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"INSERT INTO {model_name} (id, nome) VALUES (?, ?)"
        result = cursor.execute(sql, (professor.id, professor.nome))
        connection.commit()
        if cursor.lastrowid:
            return professor.__dict__()
        else:
            return None

def alterar(professor):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"UPDATE {model_name} SET nome = ? WHERE id = ?"
        cursor.execute(sql, (professor.nome, professor.id))
        connection.commit()

def remover(professor):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"DELETE FROM {model_name} WHERE id = ?"
        cursor.execute(sql, f"{professor.id}")
        connection.commit()