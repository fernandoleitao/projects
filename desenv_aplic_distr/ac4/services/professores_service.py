from infra.professores_dao import \
    listar as dao_listar, \
    consultar as dao_consultar, \
    cadastrar as dao_cadastrar, \
    alterar as dao_alterar, \
    remover as dao_remover

from model.professor import Professor

def listar():
    return [professor.__dict__() for professor in dao_listar()]

def localizar(id):
    professor = dao_consultar(id)
    if professor == None:
        return None
    return professor.__dict__()

def criar(professor_data):
    if localizar(professor_data['id']) == None:
        professor = Professor.criar(professor_data)
        return dao_cadastrar(professor)
    return None
    
def remover(id):
    dados_professor = localizar(id)
    if dados_professor == None:
        return 0
    dao_remover(Professor.criar(dados_professor))
    return 1

    if localizar(id) == None:
        return 0
    dao_remover(id)
    return 1

def atualizar(id, nome):
    professor = Professor.criar({"id": id, "nome":nome})
    dao_alterar(professor)
    return localizar(id)