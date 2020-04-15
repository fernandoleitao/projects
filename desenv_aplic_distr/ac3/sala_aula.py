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
    if 'nome' not in novo_aluno.keys():
        return jsonify({'erro':'aluno sem nome'}), 400
    for aluno in database['ALUNO']:
        if aluno['id'] == novo_aluno['id']:
            return jsonify({'erro':'id ja utilizada'}), 400
    database['ALUNO'] += [novo_aluno]
    return jsonify(novo_aluno), 200

@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def alterar_alunos(id_aluno):
    novo_nome = request.json
    if 'nome' not in novo_nome.keys():
        return jsonify({'erro':'aluno sem nome'}), 400
    for aluno in database['ALUNO']:
        if aluno['id'] == id_aluno:
            aluno['nome'] = novo_nome['nome'] 
            return jsonify(aluno), 200
    return jsonify({'erro':'aluno nao encontrado'}), 400 

@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def localizar_aluno(id_aluno):
    for aluno in database['ALUNO']:
        if aluno['id'] == id_aluno:
            return jsonify(aluno), 200
    return jsonify({'erro':'aluno nao encontrado'}), 400 


@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def remover_aluno(id_aluno):
    for aluno in database['ALUNO']:
        if aluno['id'] == id_aluno:
            database['ALUNO'].remove(aluno)
            return jsonify(aluno), 200
    return jsonify({'erro':'aluno nao encontrado'}), 400 
   

#PROFESSORES

@app.route('/professores')
def listar_professores():
    return jsonify(database['PROFESSOR'])

@app.route('/professores', methods=['POST'])
def cadastrar_professores():
    novo_professor = request.json
    if 'nome' not in novo_professor.keys():
        return jsonify({'erro':'professor sem nome'}), 400
    for professor in database['PROFESSOR']:
        if professor['id'] == novo_professor['id']:
            return jsonify({'erro':'id ja utilizada'}), 400
    database['PROFESSOR'] += [novo_professor]
    return jsonify(novo_professor), 200

@app.route('/professores/<int:id_professor>', methods=['PUT'])
def alterar_professor(id_professor):
    professor_request = request.json
    if 'nome' not in professor_request.keys():
        return jsonify({'erro':'professor sem nome'}), 400
    for professor in database['PROFESSOR']:
        if professor['id'] == id_professor:
            professor['nome'] = professor_request['nome']
            return jsonify(professor), 200
    return jsonify({'erro':'professor nao encontrado'}), 400 

@app.route('/professores/<int:id_professor>', methods=['GET'])
def localizar_professor(id_professor):
    for professor in database['PROFESSOR']:
        if professor['id'] == id_professor:
            return jsonify(professor), 200
    return jsonify({'erro':'professor nao encontrado'}),  400 

@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def remover_professor(id_professor):
    for professor in database['PROFESSOR']:
        if professor['id'] == id_professor:
            database['PROFESSOR'].remove(professor)
            return jsonify(professor), 200
    return jsonify({'erro':'professor nao encontrado'}), 400 

#GERAL

@app.route('/reseta', methods=['POST'])
def resetar():
    database['ALUNO'] = []
    database['PROFESSOR'] = []
    return jsonify(database), 200

if __name__ == '__main__':
    app.run(host = 'localhost', port = 5002, debug = True)