import requests
import unittest

class SalaAulaUnitTests(unittest.TestCase):

    # Verificando se há apenas 3 alunos.
    def test_01_alunos_retorna_lista_inical(self):
        r1 = requests.delete('http://localhost:5000/alunos/resetar')
        self.assertEqual(r1.status_code,202)
        r2 = requests.post('http://localhost:5000/alunos',json={'nome':'Thomas Alexandre','id':1, "matricula": 1234})
        self.assertEqual(r2.status_code,200)
        r3 = requests.post('http://localhost:5000/alunos',json={'nome':'Lucio Mendes','id':2, "matricula": 1235})
        self.assertEqual(r3.status_code,200)
        r4 = requests.post('http://localhost:5000/alunos',json={'nome':'Vinicius Williams','id':3, "matricula": 1236})
        self.assertEqual(r4.status_code,200)
        r = requests.get('http://localhost:5000/alunos')
        self.assertEqual(type(r.json()),type([]))
        self.assertEqual(len(r.json()),3)

    def test_02_listar_alunos_pre_cadastrados(self):
        r = requests.get('http://localhost:5000/alunos')
        for aluno in r.json():
            self.assertEqual(aluno["matricula"] != None, True)
        
    def test_03_cadastrar_aluno_com_matricula(self):
        r = requests.post('http://localhost:5000/alunos',json={'nome':'Roberto Carlos de Souza','id':4, "matricula": 21234})
        self.assertEqual(r.status_code,200)
        aluno_cadastrado = r.json()
        self.assertEqual(aluno_cadastrado["matricula"], 21234)
             
    def test_04_cadastrar_aluno_sem_nome_e_matricula(self):
        r = requests.post('http://localhost:5000/alunos',json={'id':5})
        self.assertEqual(r.status_code == 200, False)
        
    def test_05_cadastrar_aluno_sem_nome(self):
        r = requests.post('http://localhost:5000/alunos',json={'id':5, "matricula": 21235})
        self.assertEqual(r.status_code == 200, False)

    def test_06_cadastrar_aluno_sem_matricula(self):
        r = requests.post('http://localhost:5000/alunos',json={'id':5, "nome": "Roberto Souza da Silva"})
        self.assertEqual(r.status_code == 200, False)

    def test_07_deletar_aluno(self):
        r = requests.delete('http://localhost:5000/alunos/4')
        self.assertEqual(r.status_code,202)
        self.assertEqual(r.json(), 1)

    def test_08_deletar_aluno_inexistente(self):
        r = requests.delete('http://localhost:5000/alunos/4')
        self.assertEqual(r.status_code, 400)
        
    def test_09_alterar_aluno(self):
        r = requests.post('http://localhost:5000/alunos',json={'nome':'Roberto Carlos de Souza','id':4, "matricula": 21234})
        self.assertEqual(r.status_code, 200)
        r = requests.put('http://localhost:5000/alunos/4', json = {"nome": "Roberto Souza da Silva", "matricula": 21235 })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["matricula"], 21235)
        
    def test_10_alterar_aluno_sem_matricula(self):
        r = requests.put('http://localhost:5000/alunos/4', json = {"nome": "Roberto Souza da Silva"})
        self.assertEqual(r.status_code, 400)

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(SalaAulaUnitTests)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)

if __name__ == '__main__':
    runTests()