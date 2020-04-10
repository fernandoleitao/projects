from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/jinja2")
def index_template():
    return render_template("index.html", hello="Olá Turma!!!!!")


@app.route("/get_teste")
def get_teste():
    primeiro = request.args.get('primeiro')
    segundo = request.args.get('segundo')
    return render_template("index.html", hello="Olá Turma!!!!!")

usuarios = [
{'login': 'aluno1', 'senha': 'azul'},
{'login': 'aluno2', 'senha': 'vermelho'}
]

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", mensagem = "Entre no sistema")

@app.route("/form_teste", methods=["PUT", "POST"])
def form_teste():
    login = request.form["login"]
    senha = request.form["password"]
    for user in usuarios:
        if user['login'] == login and user['senha'] == senha:
            return render_template("login_ok.html", login = login)
        return render_template("login.html", mensagem = "Login inválido.")
    
if __name__ == "__main__":
    app.run(port = 5000, debug = True)