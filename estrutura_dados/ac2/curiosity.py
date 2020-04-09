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


    def coletar_rocha(self, rocha):
        if rocha.get_peso() <= self.rocha_max_peso \
           and rocha.get_tamanho() <= self.rocha_max_tamanho:
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
            # Contar rochas tipo 1,2 e 3
            lista_tipo1 = []
            lista_tipo2 = []
            lista_tipo3 = []

            for rocha in self.compartimento_rochas:
                if rocha.get_tipo() == 1:
                    lista_tipo1.append(rocha)
                if rocha.get_tipo() == 2:
                    lista_tipo2.append(rocha)
                if rocha.get_tipo() == 3:
                    lista_tipo3.append(rocha)

            print(f'O compartimento do Curiosity possui atualmente:')
            print(f'- {len(lista_tipo1)} rochas do tipo 1')
            print(f'- {len(lista_tipo2)} rochas do tipo 2')
            print(f'- {len(lista_tipo3)} rochas do tipo 3')

            qtde_balanceada = min([len(lista_tipo1),
                                    len(lista_tipo2), 
                                    len(lista_tipo3)])
            
            print(f'A quantidade ideal é {qtde_balanceada} rochas de cada tipo')

            while len(lista_tipo1) > qtde_balanceada:
                lista_tipo1.pop()
            while len(lista_tipo2) > qtde_balanceada:
                lista_tipo2.pop()
            while len(lista_tipo3) > qtde_balanceada:
                lista_tipo3.pop()                
        
        self.compartimento_rochas = []
        self.compartimento_rochas = lista_tipo1 + lista_tipo2 + lista_tipo3
        print(f'Rochas do tipo 1: {len(lista_tipo1)}')
        print(f'Rochas do tipo 2: {len(lista_tipo2)}')
        print(f'Rochas do tipo 3: {len(lista_tipo3)}')
        print(f'Compartimento atual: {self.compartimento_rochas}')

    def coletar_lixo(self, lixo):
        if self.get_peso() <= self.total_max_peso:
            if lixo.get_peso() <= self.lixo_max_peso \
            and lixo.get_tamanho() <= self.lixo_max_tamanho:

                while lixo.get_tipo() == self.get_topo_compartimento_lixo().get_tipo()\
                    and len(self.compartimento_lixo) > 0:
                    print('Coletando lixo...\nEncontrado mesmo tipo do topo da lista.')
                    self.descartar_lixo()
                else:
                    self.compartimento_lixo.append(lixo)
                    print('Coletando lixo... ', end='')
                    print('{:<8s}{:<6.2f}{:<9s}{:<6.2f}{:<6s}{:<8s}{:<1s}'
                        .format('[ Peso:', lixo.peso, 'Tamanho:', lixo.tamanho,
                                'Tipo:', lixo.tipo, ' ]'))

    def get_topo_compartimento_lixo(self):
        try:
            return self.compartimento_lixo[len(self.compartimento_lixo) - 1]
        except BaseException:
            return LixoEspacial(0, 0, 0)

    def descartar_lixo(self):
        print('Descartando lixo...')
        self.compartimento_lixo.pop()

    def get_peso(self):
        return self.get_peso_lixo() + self.get_peso_rochas()
    def get_peso_lixo(self):
            peso = 0
            for item in self.compartimento_lixo:
                peso += item.peso
            return peso
    def get_peso_rochas(self):
        peso = 0
        for item in self.compartimento_rochas:
            peso += item.peso
        return peso





def gerar_expedicao():
    rocha_min_peso = 0.5
    rocha_max_peso = 14.2
    rocha_min_tamanho = 0.2
    rocha_max_tamanho = 1.0
    rocha_tipos = [1, 2, 3]
    rochas = []
    lixo_min_peso = 1.12
    lixo_max_peso = 8.55
    lixo_min_tamanho = 0.1
    lixo_max_tamanho = 0.5
    lixo_tipos = ['metalico', 'não metalico']
    lixos = []
    tamanho_listas = randint(1000, 1000)
    for i in range(tamanho_listas):
        rocha = Rocha(round(uniform(rocha_min_peso, rocha_max_peso), 2),
                      round(uniform(rocha_min_tamanho, rocha_max_tamanho), 2),
                      rocha_tipos[randint(0, len(rocha_tipos)-1)])
        rochas.append(rocha)
        lixo = LixoEspacial(round(uniform(lixo_min_peso, lixo_max_peso), 2),
                            round(uniform(lixo_min_tamanho,
                                          lixo_max_tamanho), 2),
                            lixo_tipos[randint(0, len(lixo_tipos)-1)])
        lixos.append(lixo)
    return rochas, lixos


expedicoes = 1

while expedicoes <= 1:
    rochas, lixos = gerar_expedicao()
    curiosity = Curiosity()
    rochas, lixos = gerar_expedicao()
    print('\n{:#^80}'.format(''))
    print('{:#>49s}{:1d}{:#<30s}'.format(' iniciando expedição '.upper(), expedicoes, ' '))
    print('{:#^80}\n'.format(''))
    for rocha, lixo in zip(rochas, lixos):
        curiosity.coletar_rocha(rocha)
        curiosity.coletar_lixo(lixo)
        if curiosity.get_peso() >= curiosity.total_max_peso:
            print(f'Peso do Curiosity atingiu {round(curiosity.get_peso(), 2)} com {round(curiosity.get_peso_rochas(), 2)} em rochas e {round(curiosity.get_peso_lixo(), 2)} em lixo')
            curiosity.balancear_rochas()
            


    expedicoes += 1
    if expedicoes > 1:
        print('\nCuriosity terminou exploração. Liberando espaço de armazenamento')
        print('\n{:#^80}'.format(''))
        print('{:#^80}'.format(' relatório de missão '.upper()))
        print('{:#^80}\n'.format(''))
        print(f'Peso Coletado: {round(curiosity.get_peso(), 2)}')

