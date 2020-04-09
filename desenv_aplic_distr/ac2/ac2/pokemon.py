from requests import api
from dataclasses import dataclass
from enum import Enum, auto

"""
Instruções para TODOS os exercícios/funções abaixo:

1. Veja as instruções de como instalar e executar o PokéAPI, o treinador e os testes no documento entregue junto com este arquivo.

2. None e strings em branco são sempre consideradas inválidas quando utilizadas como parâmetros.

3. Não se preocupe com erros de tipo (como por exemplo, passar uma string para uma função que trabalha com números). Esse tipo de coisa não está nos testes.

4. Todos os nomes de pokémons nos testes estão em letras minúsculas.
   Entretanto, se você quiser aceitar MAIÚSCULAS ou até mesmo mIsTuRaDo, aplicando uma chamada à lower() ou coisa semelhante, isso fica a seu critério.
   Os testes não verificam diferenças de maiúsculas/minúsculas.

5. Desconsiderando-se os erros de tipo, se algum parâmetro puder ser determinado como inválido antes que alguma chamada a um servidor externo seja realizada, então ele deve ser detectado como tal sem que o servidor seja contactado, mesmo se ele estiver off-line.

6. Em todos os casos onde procura-se algum tipo de pokémon pelo nome ou pelo número e o mesmo não existir, uma exceção PokemonNaoExisteException deve ser lançada.

7. Em todos os casos onde procura-se algum treinador cadastrado e o mesmo não existir, uma exceção TreinadorNaoCadastradoException deve ser lançada.

8. Em todos os casos onde procura-se algum pokémon pertencente a algum treinador e o mesmo não existir, uma exceção PokemonNaoCadastradoException deve ser lançada.

9. Em todos os casos onde tenta-se cadastrar um pokémon e o mesmo já exista, uma exceção PokemonJaCadastradoException deve ser lançada.

10. Todos os nomes de pokémons, cores, jogos, movimentos, etc. recebidos e devolvidos pela PokéAPI estão em letras minúsculas e assim devem ser mantidas.

11. Não faça conexões com a URL externa pública da PokéAPI (https://pokeapi.co).
    O motivo disso é que eles irão bloquear IPs que fizerem um número muito grande de requisições em um intervalo de tempo muito curto.
    Veja nas instruções de instalação da PokéAPI como executá-la localmente (no localhost).

12. Os testes são sempre executados em ambiente local. A correção será feita com a internet desconectada.

13. Consulte a documentação em (https://pokeapi.co/docs/v2.html).

14. Infelizmente os desenvolvedores da PokéAPI ainda não disponibilizaram uma release com os pokémons da oitava geração (da região de Galar).

15. Não se esqueça de configurar o arquivo config.json para que o script dos testes possa encontrar os servidores locais da PokéAPI e também do treinador.

16. A API do treinador não tem documentação! Para entender como usá-la, olhe o código e tente deduzir.

17. Seguem alguns exemplos de URLs que podem servir para te ajudar:
    http://localhost:8000/api/v2/
    http://localhost:8000/api/v2/pokemon/39/
    http://localhost:8000/api/v2/pokemon/jigglypuff/
    http://localhost:8000/api/v2/pokemon-species/39/
    http://localhost:8000/api/v2/pokemon-species/jigglypuff/
    http://localhost:8000/api/v2/evolution-chain/11/
    http://localhost:8000/api/v2/growth-rate/1/
    http://localhost:8000/api/v2/pokemon-color/2/
"""

"""
Não altere estas URLs. Elas são utilizadas para conectar no treinador e no PokéAPI, respectivamente.
"""
site_treinador = "http://127.0.0.1:9000"
site_pokeapi = "http://127.0.0.1:8000"

"""
Use isso como parâmetro "timeout" em todas as chamadas ao requests.
Por exemplo:
    api.get(f"{site_pokeapi}/api/v2/", timeout = limite)
"""
limite = (4, 10)

"""
Isso daqui serve para deixar o código mais rápido, fazendo cache dos resultados de chamadas. Não altere isso.
"""
def cached(what):
    from functools import wraps
    cache = {}
    @wraps(what)
    def caching(n):
        if n not in cache: cache[n] = what(n)
        return cache[n]
    return caching

"""
Vamos precisar destas quatro exceções. Não altere o código delas.
"""
class PokemonNaoExisteException(Exception):
    pass

class PokemonNaoCadastradoException(Exception):
    pass

class TreinadorNaoCadastradoException(Exception):
    pass

class PokemonJaCadastradoException(Exception):
    pass

"""
1. Dado o número de um pokémon, qual é o nome dele?

Observações:
- Presuma que nunca irá existir mais do que 5000 pokémons diferentes.
- Também não existe pokémon de número zero ou negativo.
- Assim sendo, nem precisa fazer a requisição nesses casos.
- Se o pokémon não existir, lance uma PokemonNaoExisteException.
"""
@cached
def nome_do_pokemon(numero):
    if (numero <= 0) or (numero > 5000):
        raise PokemonNaoExisteException
    pokemon = api.get(f"{site_pokeapi}/api/v2/pokemon/{numero}", timeout = limite)
    if pokemon.status_code == 404 and 'Not found.' in pokemon.json().values():
        raise PokemonNaoExisteException
    return pokemon.json()['name']

"""
2. Dado o nome de um pokémon, qual é o número dele?

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista (PokemonNaoExisteException).
"""
@cached
def numero_do_pokemon(nome):
    if not nome:
        raise PokemonNaoExisteException
    pokemon = api.get(f"{site_pokeapi}/api/v2/pokemon/{nome}", timeout = limite)
    if pokemon.status_code == 404 and 'Not found.' in pokemon.json().values():
        raise PokemonNaoExisteException
    return pokemon.json()['id']

"""
3. Dado o nome de um pokémon, qual é o nome da cor (em inglês) predominante dele?

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.
"""
@cached
def color_of_pokemon(nome):
    if not nome:
        raise PokemonNaoExisteException
    pokemon_id = numero_do_pokemon(nome)
    pokemon_color = api.get(f"{site_pokeapi}/api/v2/pokemon-species/{pokemon_id}", timeout = limite)
    if pokemon_color.status_code == 404 and 'Not found.' in pokemon_color.json().values():
        raise PokemonNaoExisteException
    return pokemon_color.json()['color']['name']

"""
4. Dado o nome de um pokémon, qual é o nome da cor (em português) predominante dele?

Observações:
- Os nomes de cores possíveis de pokémons em português são APENAS as "marrom", "amarelo", "azul", "rosa", "cinza", "roxo", "vermelho", "branco", "verde" e "preto".
- No entanto, a pokeapi ainda não foi traduzida para o português! Como você pode dar um jeito nisso?

Dicas:
- O que os dicionários do python e os dicionários que você compra em livrarias têm em comum além do nome?
- Faça uma invocação à função color_of_pokemon acima.
"""
@cached
def cor_do_pokemon(nome):
    if not nome:
        raise PokemonNaoExisteException
    cores_pokemon = {
        'brown':'marrom',
        'yellow':'amarelo',
        'blue':'azul',
        'pink':'rosa',
        'gray':'cinza',
        'purple':'roxo',
        'red':'vermelho',
        'white':'branco',
        'green':'verde',
        'black':'preto'
    }
    return cores_pokemon[color_of_pokemon(nome)]

"""
5. Dado o nome de um pokémon, quais são os tipos no qual ele se enquadra?
Os nomes dos tipos de pokémons em português são "normal", "lutador", "voador", "veneno", "terra", "pedra", "inseto", "fantasma", "aço", "fogo", "água", "grama", "elétrico", "psíquico", "gelo", "dragão", "noturno" e "fada".
Todo pokémon pode pertencer a um ou a dois tipos diferentes. Retorne uma lista (ou um set ou uma tupla ou coisa similar, se preferir) contendo os tipos, mesmo que haja somente um.
Se houver dois tipos, a ordem não é importante.

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.
"""
@cached
def tipos_do_pokemon(nome):
    if not nome:
        raise PokemonNaoExisteException
    tipos_pokemon = {
        'normal':'normal', 
        'fighting':'lutador', 
        'flying':'voador', 
        'poison':'veneno', 
        'ground':'terra', 
        'rock':'pedra', 
        'bug':'inseto', 
        'ghost':'fantasma', 
        'steel':'aço', 
        'fire':'fogo', 
        'water':'água', 
        'grass':'grama', 
        'electric':'elétrico', 
        'psychic':'psíquico', 
        'ice':'gelo', 
        'dragon':'dragão', 
        'dark':'noturno',
        'fairy':'fada',
    }
    pokemon = api.get(f"{site_pokeapi}/api/v2/pokemon/{nome}", timeout = limite).json()
    if 'Not found.' in pokemon.values():
        raise PokemonNaoExisteException
    types = []
    for pokemon_type in pokemon['types']:
        types.append(tipos_pokemon[pokemon_type['type']['name']])
    return types

"""
6. Dado o nome de um pokémon, liste de qual pokémon ele evoluiu.
Por exemplo, evolucao_anterior('venusaur') == 'ivysaur'
Retorne None se o pokémon não tem evolução anterior. Por exemplo, evolucao_anterior('bulbasaur') == None

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.
"""
@cached
def evolucao_anterior(nome):
    if not nome:
        raise PokemonNaoExisteException
    pokemon = api.get(f"{site_pokeapi}/api/v2/pokemon-species/{nome}", timeout = limite)
    if pokemon.status_code == 404 and 'Not found.' in pokemon.json().values():
        raise PokemonNaoExisteException
    if pokemon.json()['evolves_from_species'] is not None:
        return pokemon.json()['evolves_from_species']['name']
    return

"""
7. Dado o nome de um pokémon, liste para quais pokémons ele pode evoluiur.
Por exemplo, evolucoes_proximas('ivysaur') == ['venusaur'].
A maioria dos pokémons que podem evoluir, só podem evoluir para um único tipo de pokémon próximo. No entanto, há alguns que podem evoluir para dois ou mais tipos diferentes de pokémons.
Se houver múltiplas possibilidades de evoluções, a ordem delas não importa. Por exemplo:
evolucoes_proximas('poliwhirl') == ['poliwrath', 'politoed']
Note que esta função dá como resultado somente o próximo passo evoluitivo. Assim sendo, evolucoes_proximas('poliwag') == ['poliwhirl']
Se o pokémon não evolui, retorne uma lista vazia. Por exemplo, evolucoes_proximas('celebi') == []

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.

Dicas:
- Este é um item bônus de desafio e deve ser um dos exercícios mais difíceis deste AC. Isso significa que mesmo que você não consiga, ainda dá para tirar 10.
- Se quiser desistir do bônus, basta colocar um "return []" como sendo o código disto.
- Possivelmente o JSON que a API irá te devolver será algo bem complicado de analisar.
- Possivelmente você terá que fazer 2 ou mais requisições aqui.
- Uma forma de resolver este exercício inclui utilizar recursão.
"""
@cached
def evolucoes_proximas(nome):
    pokemon_evolutions = []
    if not nome:
        raise PokemonNaoExisteException
    req_pokemon = api.get(f"{site_pokeapi}/api/v2/pokemon-species/{nome}", timeout = limite)
    if req_pokemon.status_code == 404:
        raise PokemonNaoExisteException
    url_chain = req_pokemon.json()['evolution_chain']['url']
    req_chain = api.get(url_chain, timeout = limite)
    chain = req_chain.json()#['chain']

    def encontra_evolucao(chain):  
        for item in chain:
            if chain[item] == nome: # Se o pokemon é o passado no parametro 'nome'
                chain = chain['evolves_to'] # Pula para 'evolves_to' para ver quais são as evoluções
                if len(chain) == 0: # Se 'evolves_to' retorna uma lista vazia é porque não tem evoluções
                    return pokemon_evolutions
                for item in chain: # para cada evolução do pokemon          
                    if chain[item]['species']['name'] == nome:                  
                        pokemon_evolutions.append(chain[item]['species']['name']) # grava na lista 'pokemon_evolutions' o nome do pokemon
        if len(pokemon_evolutions) > 0: # Se encontrou a(s) evolução(ões)            
            return pokemon_evolutions 
        chain = chain['evolves_to'] # Se chegou até aqui, não encontrou nada, então sobe um nível na cadeia
        for item in chain: # Para cada evolução nesse nível
            encontra_evolucao(item) # Roda de novo a função
        return pokemon_evolutions
    return encontra_evolucao(chain)

print(evolucoes_proximas('charmeleon'))

"""
8. A medida que ganham pontos de experiência, os pokémons sobem de nível.
É possível determinar o nível (1 a 100) em que um pokémon se encontra com base na quantidade de pontos de experiência que ele tem.
Entretanto, cada tipo de pokémon adota uma curva de level-up diferente (na verdade, existem apenas 6 curvas de level-up diferentes).
Assim sendo, dado um nome de pokémon e uma quantidade de pontos de experiência, retorne o nível em que este pokémon está.
Valores negativos de experiência devem ser considerados inválidos.

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.
- Lance uma exceção ValueError para os casos onde o valor da experiência é negativo.
- Não realize os cálculos diretamente nesta função implementando nela alguma fórmula matemática. Utilize a API para fazer os cálculos.
"""
def nivel_do_pokemon(nome, experiencia):
    if not nome:
        raise PokemonNaoExisteException
    if experiencia < 0:
        raise ValueError
    growth_rate_url = api.get(f"{site_pokeapi}/api/v2/pokemon-species/{nome}", timeout = limite)
    if growth_rate_url.status_code == 404:
        raise PokemonNaoExisteException
    pokemon_levels = api.get(growth_rate_url.json()['growth_rate']['url'], timeout = limite).json()['levels']
    for level in pokemon_levels:
        if level['experience'] <= experiencia: 
            final_level = level['level']
    return final_level
       
"""
Até agora, temos representado as espécies de pokemóns apenas como uma string, no entanto podemos representá-los com uma classe.
Esta classe representa uma espécie de pokémon, e cada instância carrega dentro de si o nome de uma espécie de pokémon, a cor e as informações da evolução.
"""
@dataclass(frozen = True)
class EspeciePokemon:
    nome: str
    cor: str
    evoluiu_de: str
    evolui_para: list

    """
    9. Com base nas funções acimas, implemente o método estático por_nome da classe EspeciePokemon.
    Esse método deve retornar uma instância de EspeciePokemon contendo o nome da espécie, a cor e as informações sobre a evolução.
    """
    @staticmethod
    @cached
    def por_nome(nome):
        if not nome:
            raise PokemonNaoExisteException
        return EspeciePokemon(nome,cor_do_pokemon(nome),evolucao_anterior(nome),evolucoes_proximas(nome))

"""
10. Dado um nome de treinador, cadastre-o na API de treinador.
Retorne True se um treinador com esse nome foi criado e False em caso contrário (já existia).
"""
def cadastrar_treinador(nome):
    res = api.put(f"{site_treinador}/treinador/{nome}", timeout = limite)
    if res.status_code == 303:
        return False
    elif res.status_code == 202:
        return True

"""
Vamos precisar desta classe logo abaixo.
"""
class Genero(Enum):
    FEMININO = auto()
    MASCULINO = auto()

    @staticmethod
    def decodificar(valor):
        for g in Genero:
            if g.name.lower() == valor:
                return g
        raise ValueError()

    def __str__(self):
        return self.name.lower()

"""
Agora, nós implementaremos alguns métodos desta classe (Pokemon). Não deve-se confundí-la com EspeciePokemon.
Vamos supor que você tenha dois pokémons da espécie Ponyta. Para diferenciá-los, decida chamar um de "veloz" e o outro de "ligeirinho".
Seu amigo também tem uma Ponyta, que ele chama de "quentinha".
Nesse caso, "veloz", "ligeirinho" e "quentinha" são três Ponytas diferentes, pertencentes a dois treinadores diferentes.
Além disso, esses diferentes pokémons, embora da mesma espécie, também podem ser de sexos diferentes e com diferentes quantidades de pontos de experiência.
"""
class Pokemon:

    def __init__(self, nome_treinador, apelido, tipo, experiencia, genero):
        if experiencia < 0: raise ValueError()
        self.__nome_treinador = nome_treinador
        self.__apelido = apelido
        self.__tipo = tipo
        self.__experiencia = experiencia
        self.__genero = genero

    #Não mexa nisso.
    def __setattr__(self, attr, value):
        if attr.find("__") == -1: raise AttributeError(attr)
        super().__setattr__(attr, value)

    @property
    def nome_treinador(self):
        return self.__nome_treinador

    @property
    def apelido(self):
        return self.__apelido

    @property
    def tipo(self):
        return self.__tipo

    @property
    def experiencia(self):
        return self.__experiencia

    @property
    def genero(self):
        return self.__genero
            

    """
    11. Você consegue definir uma implementação para essa propriedade?
    Dica:
    - Você pode usar a função nivel_do_pokemon definida acima:
    """
    @property
    def nivel(self):
        self.__nivel = nivel_do_pokemon(self.tipo.nome ,self.experiencia) 
        return self.__nivel

    """
    12. Imagine que você capturou dois pokémons do mesmo tipo. Para diferenciá-los, você dá nomes diferentes (apelidos) para eles.
    Logo, um treinador pode ter mais do que um pokémon de um determinado tipo, mas não pode ter dois pokémons diferentes com o mesmo apelido.
    Assim sendo, dado um nome de treinador, um apelido de pokémon, um tipo de pokémon e uma quantidade de experiência, cadastre o pokémon com o tipo correspondente ao treinador dado na API do treinador.
    Certifique-se de que todos os dados são válidos.
    """
    def cadastrar(self):
        req_check_pokemon = api.get(f"{site_pokeapi}/api/v2/pokemon-species/{self.tipo.nome}", timeout = limite)
        if req_check_pokemon.status_code == 404:
            raise PokemonNaoExisteException
        payload = {'tipo': self.tipo.nome ,'experiencia': self.experiencia,'genero': self.genero.name.lower()}
        req_add_pokemon = api.put(f"{site_treinador}/treinador/{self.nome_treinador}/{self.apelido}", json=payload, timeout = limite)
        if req_add_pokemon.status_code == 404:
            raise TreinadorNaoCadastradoException
        if req_add_pokemon.status_code == 409:
            raise PokemonJaCadastradoException
        if req_add_pokemon.status_code == 202:
            return True


    """
    13. Dado um pokémon (o que é representado pelo self) acrescente-lhe a experiência ganha na API do treinador (e no própria instância também).
    
    Observação:
    - A experiêcia ganha não pode ser um número negativo. Lance um ValueError nesse caso.
    """
    def ganhar_experiencia(self, ganho):
        if ganho < 0:
            raise ValueError
        payload = {'experiencia' : ganho}
        req_raise_xp_pokemon = api.post(f"{site_treinador}/treinador/{self.nome_treinador}/{self.apelido}/exp",json=payload, timeout = limite)
        if req_raise_xp_pokemon.status_code == 404 and req_raise_xp_pokemon.text == "Treinador não existe.":
            raise TreinadorNaoCadastradoException
        if req_raise_xp_pokemon.status_code == 404 and req_raise_xp_pokemon.text == "Pokémon não existe.":
            raise PokemonNaoCadastradoException
        if req_raise_xp_pokemon.status_code == 204:
            self.__experiencia = self.experiencia + ganho
            return True

    """
    14. Dado um nome de treinador e um apelido de pokémon, localize esse pokémon na API do treinador.
        A API do treinador trará como resultado, a espécie do pokémon, a quantidade de experiência que ele tem e o seu gênero.
        Finalmente, este método deve retornar um objeto que seja uma instância da classe Pokemon.
    """
    @staticmethod
    def localizar_pokemon(nome_treinador, apelido_pokemon):
        req_find_pokemon = api.get(f"{site_treinador}/treinador/{nome_treinador}/{apelido_pokemon}", timeout = limite)
        if req_find_pokemon.status_code == 404 and req_find_pokemon.text == "Treinador não existe.":
            raise TreinadorNaoCadastradoException
        if req_find_pokemon.status_code == 404 and req_find_pokemon.text == "Pokémon não existe.":
            raise PokemonNaoCadastradoException
        if req_find_pokemon.status_code == 200:
            res_apelido = req_find_pokemon.json()["apelido"]
            res_xp = req_find_pokemon.json()["experiencia"]
            res_type = req_find_pokemon.json()["tipo"]
            res_gender = req_find_pokemon.json()["genero"]
            return Pokemon(nome_treinador, res_apelido, EspeciePokemon.por_nome(res_type), res_xp, Genero.decodificar(res_gender))

"""
15 Dado o nome de um treinador, localize-o na API do treinador e retorne um dicionário contendo como chaves, os apelidos de seus pokémons e como valores os nomes dos tipos deles.
"""
def detalhar_treinador(nome_treinador):
    req_detail_trainer = api.get(f"{site_treinador}/treinador/{nome_treinador}", timeout = limite)
    if req_detail_trainer.status_code == 404:
            raise TreinadorNaoCadastradoException
    pokemons = req_detail_trainer.json()["pokemons"]
    poke_dict = {}
    for item in pokemons:
        poke_dict[item] = pokemons[item]['tipo']
    return poke_dict

"""
16. Dado o nome de um treinador, localize-o na API do treinador e exclua-o, juntamente com todos os seus pokémons.
"""
def excluir_treinador(nome_treinador):
    req_delete_trainer = api.delete(f"{site_treinador}/treinador/{nome_treinador}", timeout = limite)
    if req_delete_trainer.status_code == 404:
        raise TreinadorNaoCadastradoException
    if req_delete_trainer.status_code == 204:
        return True
 
"""
17. Dado o nome de um treinador e o apelido de um de seus pokémons, localize o pokémon na API do treinador e exclua-o.
"""
def excluir_pokemon(nome_treinador, apelido_pokemon):
    req_delete_pokemon = api.delete(f"{site_treinador}/treinador/{nome_treinador}/{apelido_pokemon}", timeout = limite)
    if req_delete_pokemon.status_code == 404 and req_delete_pokemon.text == "Treinador não existe.":
        raise TreinadorNaoCadastradoException
    if req_delete_pokemon.status_code == 404 and req_delete_pokemon.text == "Pokémon não existe.":
        raise PokemonNaoCadastradoException
    if req_delete_pokemon.status_code == 204:
        return True
