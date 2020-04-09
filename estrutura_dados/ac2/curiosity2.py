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

    def cheio():
        if get_peso() >= self.total_max_peso:
            return True
        return False

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

    def coletar_lixo(self, lixo):
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