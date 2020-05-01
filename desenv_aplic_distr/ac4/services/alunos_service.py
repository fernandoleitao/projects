from infra.alunos_dao import \
    listar as dao_listar, \
    consultar as dao_consultar, \
    cadastrar as dao_cadastrar, \
    alterar as dao_alterar, \
    remover as dao_remover

from model.aluno import Aluno

def listar():
    return [aluno.__dict__() for aluno in dao_listar()]

def localizar(id):
    aluno = dao_consultar(id)
    if aluno == None:
        return None
    return aluno.__dict__()

def criar(aluno_data):
    if localizar(aluno_data['id']) == None:
        aluno = Aluno.criar(aluno_data)
        return dao_cadastrar(aluno)
    return None

def remover(id):
    dados_aluno = localizar(id)
    if dados_aluno == None:
        return 0
    dao_remover(Aluno.criar(dados_aluno))
    return 1

def atualizar(id, nome, matricula):
    aluno = Aluno.criar({"id": id, "nome":nome, "matricula":matricula})
    dao_alterar(aluno)
    return localizar(id)
    
def resetar():
    alunos = listar()
    for aluno in alunos:
        remover(aluno["id"])