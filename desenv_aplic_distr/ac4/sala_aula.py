from flask import Flask, jsonify, request, render_template
from alunos_api import alunos_app
from professores_api import professores_app
import requests as Req
import infra.alunos_db as alunos_db
import infra.professores_db as professores_db

app = Flask(__name__)
app.register_blueprint(alunos_app)
app.register_blueprint(professores_app)

@app.route('/')
def all():
    alunos = Req.get("http://localhost:5000/alunos").json()
    professores = Req.get("http://localhost:5000/professores").json()
    return render_template("index.html", alunos=alunos, professores=professores)

alunos_db.init()
professores_db.init()

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
