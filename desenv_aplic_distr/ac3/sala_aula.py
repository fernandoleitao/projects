from flask import Flask, jsonify, request

app = Flask(__name__)

database = {}
database['ALUNO'] = []
database['PROFESSOR'] = []

@app.route('/')
def all():
  return jsonify(database)

# ALUNOS

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    inicio_nome = request.args.get('nome_inicia_com')   
    return jsonify(database['ALUNO'])

@app.route('/alunos', methods=['POST'])
def cadastrar_alunos():
    novo_aluno = request.json
    return jsonify({'erro':'função nao implementada'}), 500

@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def alterar_alunos(id_aluno):
    return jsonify({'erro':'função nao implementada'}), 500

@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def localizar_aluno(id_aluno):
    return jsonify({'erro':'função nao implementada'}), 500

@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def remover_aluno(id_aluno):
    return jsonify({'erro':'função nao implementada'}), 500
   

#PROFESSORES

@app.route('/professores')
def listar_professores():
    return jsonify(database['PROFESSOR'])

@app.route('/professores', methods=['POST'])
def cadastrar_professores():
    novo_professor = request.json
    return jsonify({'erro':'função nao implementada'}), 500

@app.route('/professores/<int:id_professor>', methods=['PUT'])
def alterar_professor(id_professor):
    professor_request = request.json
    return jsonify({'erro':'função nao implementada'}), 500

@app.route('/professores/<int:id_professor>', methods=['GET'])
def localizar_professor(id_professor):
    return jsonify({'erro':'função nao implementada'}), 500

@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def remover_professor(id_professor):
    return jsonify({'erro':'função nao implementada'}), 500

#GERAL

@app.route('/reseta', methods=['POST'])
def resetar():
    database['ALUNO'] = []
    database['PROFESSOR'] = []
    return jsonify(database)

if __name__ == '__main__':
    app.run(host = 'localhost', port = 5002, debug = True)