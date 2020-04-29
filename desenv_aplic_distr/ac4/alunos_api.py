from flask import Blueprint, jsonify, request
from services.alunos_service import \
    listar as service_listar, \
    localizar as service_localiza, \
    criar as service_criar, \
    remover as service_remover, \
    atualizar as service_atualiza, \
    resetar as service_resetar

alunos_app = Blueprint('alunos_app', __name__, template_folder='templates')

@alunos_app.route('/alunos')
def listar_alunos():
    lista = service_listar()
    return jsonify(lista)

@alunos_app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    novo_aluno = request.get_json()
    aluno = service_criar(novo_aluno)
    if aluno == None:
        return jsonify({'erro':'aluno ja existe'}), 400
    return jsonify(aluno)

@alunos_app.route('/alunos/<int:id>', methods=['PUT'])
def alterar_aluno(id):
    aluno_data = request.get_json()
    if ('nome' not in aluno_data):
        return jsonify({'erro':'aluno sem nome'}), 400
    atualizado = service_atualiza(id, aluno_data['nome'])
    if atualizado != None:
        return jsonify(atualizado), 200
    return jsonify({'erro':'aluno nao encontrado'}), 400
    
@alunos_app.route('/alunos/<int:id>', methods=['GET'])
def localizar_aluno(id):
    aluno = service_localiza(id)
    if aluno != None:
        return jsonify(aluno)
    return jsonify({'erro':'aluno nao encontrado'}), 400

@alunos_app.route('/alunos/<int:id>', methods=['DELETE'])
def remover_aluno(id):
    removido = service_remover(id)
    if removido == 1:
        return jsonify(removido), 202
    return jsonify({'erro':'aluno nao encontrado'}), 400

@alunos_app.route('/alunos/resetar', methods=['DELETE'])
def resetar():
    service_resetar()
    return jsonify("Base de alunos reiniciada"), 202