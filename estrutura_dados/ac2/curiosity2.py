from random import uniform, randint
from statistics import median, mean


class Rocha:

    def __init__(self, peso, tamanho, tipo):
        self.peso = peso
        self.tamanho = tamanho
        self.tipo = tipo

    def get_peso(self):
        return self.peso

    def get_tamanho(self):
        return self.tamanho

    def get_tipo(self):
        return self.tipo

    def __str__(self):
        return str([self.peso, self.tamanho, self.tipo])

    def __repr__(self):
        return self.__str__()

class LixoEspacial:

    def __init__(self, peso, tamanho, tipo):
        self.peso = peso
        self.tamanho = tamanho
        self.tipo = tipo

    def get_peso(self):
        return self.peso

    def get_tamanho(self):
        return self.tamanho

    def get_tipo(self):
        return self.tipo

    def __str__(self):
        return str([self.peso, self.tamanho, self.tipo])

    def __repr__(self):
        return self.__str__()

class Curiosity():

    def __init__(self):
        self.total_max_peso = 70
        self.rocha_max_peso = 2.5
        self.rocha_max_tamanho = 0.74
        self.rocha_tipo = [1, 2, 3]
        self.lixo_max_peso = 2.5
        self.lixo_max_tamanho = 0.3
        self.lixo_tipos = ['metalico', 'não metalico']
        self.compartimento_rochas = []
        self.compartimento_lixo = []

    def get_peso_compartimento(self, compartimento):
        peso = 0
        for item in compartimento:
            peso += item.peso
        return peso

    def get_peso(self):
        return self.get_peso_compartimento(self.compartimento_rochas) + \
               self.get_peso_compartimento(self.compartimento_lixo)

    def cheio(self):
        if self.get_peso() >= self.total_max_peso * 0.98:
            return True
        return False

    def coletar_rocha(self, rocha):
        if rocha.get_peso() <= self.rocha_max_peso and \
           rocha.get_tamanho() <= self.rocha_max_tamanho:
            self.compartimento_rochas.append(rocha)
            print('Coletando rocha...', end='')
            print('{:<8s}{:<6.2f}{:<9s}{:<6.2f}{:<6s}{:<1d}{:<1s}'
                .format('[ Peso:', rocha.peso, 'Tamanho:', rocha.tamanho,
                        'Tipo:', rocha.tipo, ' ]'))

    def descartar_rocha(self, rocha):
        self.compartimento_rochas.remove(rocha)
        print('Descartando rocha...')
    
    def balancear_rochas(self):
        if self.get_peso() >= self.total_max_peso:
            print('\n{:#^80}'.format(''))
            print('{:#^80}'.format(' modo balanceamento do compartimento de rochas '.upper()))
            print('{:#^80}\n'.format(''))
            
            rochas_tipo1 = []
            rochas_tipo2 = []
            rochas_tipo3 = []

            for rocha in self.compartimento_rochas:
                if rocha.get_tipo() == 1:
                    rochas_tipo1.append(rocha)
                if rocha.get_tipo() == 2:
                    rochas_tipo2.append(rocha)
                if rocha.get_tipo() == 3:
                    rochas_tipo3.append(rocha)

            print(f'O compartimento do Curiosity possui atualmente:\n')
            print(f'- {len(rochas_tipo1)} rochas do tipo 1 e pesa {self.get_peso_compartimento(rochas_tipo1)}')
            print(f'- {len(rochas_tipo2)} rochas do tipo 2 e pesa {self.get_peso_compartimento(rochas_tipo2)}')
            print(f'- {len(rochas_tipo3)} rochas do tipo 3 e pesa {self.get_peso_compartimento(rochas_tipo3)}')

            qtde_balanceada = round(mean([len(rochas_tipo1), len(rochas_tipo2), len(rochas_tipo3)]))

            print(f'\nA quantidade sugerida é {qtde_balanceada} de cada tipo...')
            print('Balanceando...')

            while len(rochas_tipo1) > qtde_balanceada:
                rochas_tipo1.pop()
            while len(rochas_tipo2) > qtde_balanceada:
                rochas_tipo2.pop()
            while len(rochas_tipo3) > qtde_balanceada:
                rochas_tipo3.pop()                
        
            self.compartimento_rochas = []
            self.compartimento_rochas = rochas_tipo1 + rochas_tipo2 + rochas_tipo3
            print('\nTotal de Rochas:')
            print(f'Rochas do tipo 1: {len(rochas_tipo1)}')
            print(f'Rochas do tipo 2: {len(rochas_tipo2)}')
            print(f'Rochas do tipo 3: {len(rochas_tipo3)}')

    def coletar_lixo(self, lixo):
        if lixo.get_peso() <= self.lixo_max_peso \
           and lixo.get_tamanho() <= self.lixo_max_tamanho:
            while lixo.get_tipo() == self.topo_lixo().get_tipo()\
                and len(self.compartimento_lixo) > 0:
                print('Coletando lixo...\nEncontrado mesmo tipo do topo da lista.')
                self.descartar_lixo()
            else:
                self.compartimento_lixo.append(lixo)
                print('Coletando lixo... ', end='')
                print('{:<8s}{:<6.2f}{:<9s}{:<6.2f}{:<6s}{:<8s}{:<1s}'
                    .format('[ Peso:', lixo.peso, 'Tamanho:', lixo.tamanho,
                            'Tipo:', lixo.tipo, ' ]'))

    def topo_lixo(self):
        try:
            return self.compartimento_lixo[len(self.compartimento_lixo) - 1]
        except BaseException:
            return LixoEspacial(0, 0, 0)

    def descartar_lixo(self):
        print('Descartando lixo...')
        self.compartimento_lixo.pop()

    def explorar(self, rochas, lixos, expedicoes):
        print('\n{:#^80}'.format(''))
        print('{:#>49s}{:1d}{:#<30s}'.format(' iniciando expedição '.upper(), expedicoes, ' '))
        print('{:#^80}\n'.format(''))

        for rocha, lixo in zip(rochas, lixos):
            self.coletar_rocha(rocha)
            self.coletar_lixo(lixo)
            if self.cheio():
                print(f'Peso do Curiosity atingiu {round(self.get_peso(), 2)} com {round(self.get_peso_compartimento(self.compartimento_rochas), 2)} em rochas e {round(self.get_peso_compartimento(self.compartimento_lixo), 2)} em lixo')
                self.balancear_rochas()
                if self.cheio(): break

        print('\nCuriosity terminou exploração. Liberando espaço de armazenamento')
        print('\n{:#^80}'.format(''))
        print('{:#^80}'.format(' relatório de missão '.upper()))
        print('{:#^80}\n'.format(''))
        print(f'Peso Coletado: {round(self.get_peso(), 2)}')
        print(f'Peso do compartimento de rochas: {round(self.get_peso_compartimento(self.compartimento_rochas), 2)}')
        print(f'Peso do compartimento de lixo: {round(self.get_peso_compartimento(self.compartimento_lixo), 2)}')


class Marte():

    def __init__(self, min_obj, max_obj):
        self.rocha_min_peso = 0.5
        self.rocha_max_peso = 14.2
        self.rocha_min_tamanho = 0.2
        self.rocha_max_tamanho = 1.0
        self.rocha_tipos = [1, 2, 3]
        self.rochas = []
        self.lixo_min_peso = 1.12
        self.lixo_max_peso = 8.55
        self.lixo_min_tamanho = 0.1
        self.lixo_max_tamanho = 0.5
        self.lixo_tipos = ['metalico', 'não metalico']
        self.lixos = []
        self.tamanho_listas = randint(min_obj, max_obj)

    def gerar_expedicao(self):
        rochas = []
        lixos = []
        for i in range(self.tamanho_listas):
            rocha = Rocha(round(uniform(self.rocha_min_peso, self.rocha_max_peso), 2),
                        round(uniform(self.rocha_min_tamanho, self.rocha_max_tamanho), 2),
                        self.rocha_tipos[randint(0, len(self.rocha_tipos)-1)])
            rochas.append(rocha)
            lixo = LixoEspacial(round(uniform(self.lixo_min_peso, self.lixo_max_peso), 2),
                                round(uniform(self.lixo_min_tamanho,
                                            self.lixo_max_tamanho), 2),
                                self.lixo_tipos[randint(0, len(self.lixo_tipos)-1)])
            lixos.append(lixo)
        return rochas, lixos


marte = Marte(1000, 1000)
expedicoes = 3

for i in range(expedicoes):
    curiosity = Curiosity()
    rochas, lixos = marte.gerar_expedicao()
    curiosity.explorar(rochas, lixos, i+1)

    


