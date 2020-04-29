import sqlite3
from model.aluno import Aluno
from contextlib import closing

db_name = "alunos.db"
model_name = "aluno"

def con():
    return sqlite3.connect(db_name)

def listar():
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT * FROM {model_name}")
        rows = cursor.fetchall()
        registros = []
        for (id, nome) in rows:
            registros.append(Aluno.criar({"id": id, "nome": nome}))
        return registros

def consultar(id):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT * FROM {model_name} WHERE id = ?", (int(id),))
        row = cursor.fetchone()
        if row == None:
            return None
        return Aluno.criar({"id": row[0], "nome": row[1]})

def cadastrar(aluno):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"INSERT INTO {model_name} (id, nome) VALUES (?, ?)"
        result = cursor.execute(sql, (aluno.id, aluno.nome))
        connection.commit()
        if cursor.lastrowid:
            return aluno.__dict__()
        else:
            return None

def alterar(aluno):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"UPDATE {model_name} SET nome = ? WHERE id = ?"
        cursor.execute(sql, (aluno.nome, aluno.id))
        connection.commit()

def remover(aluno):
    with closing(con()) as connection, closing(connection.cursor()) as cursor:
        sql = f"DELETE FROM {model_name} WHERE id = ?"
        cursor.execute(sql, f"{aluno.id}")
        connection.commit()