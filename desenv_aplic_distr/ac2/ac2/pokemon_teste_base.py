from requests import api, exceptions
from subprocess import PIPE, Popen
from functools import wraps
from threading import Thread
from os import getpid
from time import sleep
import json

dados_config = None

meu_site_treinador = "http://127.0.0.1:9000"
meu_site_pokeapi = "http://127.0.0.1:8000"
debug = False

def print_debug(x):
    if debug:
        print(x)

def ler_configuracao():
    global dados_config
    if dados_config is None:
        try:
            with open('config.json', encoding = 'utf-8') as f:
                dados = json.load(f)
        except Exception as x:
            print_debug(x)
            raise Exception("Não foi possível ler o arquivo config.json.")
        if 'pokeapi' not in dados or 'treinador' not in dados or len(dados) != 2:
            raise Exception("O arquivo config.json está mal-formado.")
        dados_config = dados
    return dados_config

def verificar_erro(interno, tipo_erro, tests = None):
    if tests is None:
        try:
            interno()
        except Exception as x:
            assert type(x) is tipo_erro, f"Esperava-se que um erro do tipo {tipo_erro.__name__}, mas obteve-se uma do tipo {x.__class__.__name__}."
        else:
            assert False, f"Esperava-se que um erro do tipo {tipo_erro.__name__} fosse produzido, mas não foi."
    else:
        try:
            interno()
        except Exception as x:
            tests.assertIs(type(x), tipo_erro, f"Esperava-se que um erro do tipo {tipo_erro.__name__}, mas obteve-se uma do tipo {x.__class__.__name__}.")
        else:
            tests.fail(f"Esperava-se que um erro do tipo {tipo_erro.__name__} fosse produzido, mas não foi.")

def pokemon_nao_existe(interno, tests = None):
    verificar_erro(interno, PokemonNaoExisteException, tests)

def pokemon_nao_cadastrado(interno, tests = None):
    verificar_erro(interno, PokemonNaoCadastradoException, tests)

def treinador_nao_cadastrado(interno, tests = None):
    verificar_erro(interno, TreinadorNaoCadastradoException, tests)

def pokemon_ja_cadastrado(interno, tests = None):
    verificar_erro(interno, PokemonJaCadastradoException, tests)

def valor_errado(interno, tests = None):
    verificar_erro(interno, ValueError, tests)

def qualquer_erro(interno, tests = None):
    try:
        interno()
    except Exception as x:
        pass
    else:
        if tests is None:
            assert False, f"Esperava-se que um erro fosse produzido, mas não foi."
        else:
            tests.fail(f"Esperava-se que um erro fosse produzido, mas não foi.")

def assert_equals_unordered_list(esperada, obtida, tests = None):
    if tests is None:
        assert len(esperada) == len(obtida), f"Esperava-se que o resultado fosse {obtida}, mas foi {esperada}."
        for item in esperada:
            assert item in obtida, f"Esperava-se que o resultado fosse {obtida}, mas foi {esperada}."
    else:
        tests.assertEqual(len(esperada), len(obtida), f"Esperava-se que o resultado fosse {obtida}, mas foi {esperada}.")
        for item in esperada:
            tests.assertIn(item, obtida, f"Esperava-se que o resultado fosse {obtida}, mas foi {esperada}.")

class NoStdIO:
    def __init__(self):
        import sys
        self.__oout = sys.stdout
        self.__oin = sys.stdin
        self.__usou_print = False
        self.__usou_input = False
        self.__privilegio = False

    def __enter__(self):
        import sys
        self.__oout = sys.stdout
        self.__oin = sys.stdin
        sys.stdout = self
        sys.stdin = self

    def __exit__(self, a, b, c):
        import sys
        sys.stdout = self.__oout
        sys.stdin = self.__oin

    def write(self, t):
        if not self.__privilegio:
            self.__usou_print = True
        return self.__oout.write(t)

    def print_privilegiado(self, texto):
        self.__privilegio = True
        try:
            print(texto)
        finally:
            self.__privilegio = False

    def readline(self):
        self.__usou_input = True
        return self.__oin.readline()

    def flush(self):
        pass

    def __call__(self, delegate):
        @wraps(delegate)
        def sem_input(*args, **kwargs):
            with self:
                return delegate(*args, **kwargs)
        return sem_input

    def test_print(self):
        if self.__usou_print: raise Exception("Você não deveria utilizar a função print neste exercício.")

    def test_input(self):
        if self.__usou_input: raise Exception("Você não deveria utilizar a função input neste exercício.")

sem_io = NoStdIO()

class ContaPontos:
    def __init__(self):
        self.__total = 0
        self.__acumulado = 0
        self.__map = {}

    def prepare(self, grupo, qtd, penalidade, before, after_ok, after_fail):
        if grupo != 'Bônus': self.__total += qtd
        if grupo in self.__map:
            self.__map[grupo]['total'] += qtd
        else:
            self.__map[grupo] = {'total': qtd, 'executado': 0, 'penalidade': 0}

        def intermediaria(interna):
            @wraps(interna)
            def contando(*args, **kwargs):
                try:
                    before()
                    with sem_io:
                        x = interna(*args, **kwargs)
                    self.__acumulado += qtd
                    self.__map[grupo]['executado'] += qtd
                    after_ok(x)
                    return x
                except Exception as z:
                    self.__map[grupo]['penalidade'] -= penalidade
                    self.__acumulado -= penalidade
                    after_fail(z)
                    raise z
            return contando
        return intermediaria

    def mostrar_pontos(self):
        if self.__total == 0:
            print("Os testes não foram executados.")
            return
        pontos = max(0, min(10, self.__acumulado * 10 / self.__total))
        def arredondar(v):
            s = f"X{v:4.2f}Y".replace(".", ",")
            while s.find("0Y") != -1: s = s.replace("0Y", "Y")
            return s.replace(",Y", "Y").replace("XY", "X0Y")[1:-1]
        ps = arredondar(pontos)
        print(f"Sua pontuação é de {self.__acumulado} / {self.__total}. Logo, sua nota é {ps}.")
        for valor in sorted(self.__map.keys()):
            t = self.__map[valor]['total']
            e = self.__map[valor]['executado']
            p = self.__map[valor]['penalidade']
            if t == 0 and p == 0:
                print(f'- O quesito "{valor}" está ok.')
            elif t == 0:
                print(f'- No quesito "{valor}", houve uma PENALIDADE de {p}.')
            elif p == 0:
                print(f'- No quesito "{valor}", sua pontuação é de {e} / {t}.')
            else:
                print(f'- No quesito "{valor}", sua pontuação é de {e} / {t}, mas houve uma PENALIDADE de {p}, totalizando {(e - p)} / {t}.')

pontos_main = ContaPontos()

class ServidorNaoOnlineException(Exception):
    pass

def wait(t):
    sleep(t)
    return t

class SobeServidores:

    @staticmethod
    def apocalipse():
        return
        out = Popen('tasklist', shell = True, stdin = PIPE, stdout = PIPE, stderr = PIPE).communicate()[0]
        parts = out.decode("windows-1252").split('\r\n')

        try:
            i = parts[1].index('Identifi')
        except:
            i = parts[1].index('     PID')
        meu_pid = getpid()

        for line in parts:
            if 'python.exe' in line and str(meu_pid) not in line:
                alvo = line[i : i + 8]
                SobeServidores.matar(alvo)

    @staticmethod
    def matar(alvo):
        return
        if alvo == -1: return
        tout = Popen(f"taskkill /f /pid {alvo}", shell = True, stdin = PIPE, stdout = PIPE, stderr = PIPE).communicate()[0]
        print_debug(tout.decode("windows-1252"))

    @staticmethod
    def subir_servidor(ouvido, comando, verificador_online):
        return
        if verificador_online() == "online": return

        ouvido("")
        ouvido(comando)
        proc = Popen(comando, shell = True, stdin = PIPE, stdout = PIPE, stderr = PIPE)
        SobeServidores.spy(ouvido, proc)

        paciencia = 8
        while paciencia > 0:
            if verificador_online() == "online": return
            paciencia -= wait(0.5)
        raise ServidorNaoOnlineException()

    @staticmethod
    def spy(ouvido, proc):
        def enqueue_output(out):
            for line in iter(out.readline, b''):
                z = line.decode("windows-1252").replace('\r', '').replace('\n', '')
                ouvido(z)

        t1 = Thread(target = enqueue_output, args = (proc.stdout, ))
        t1.daemon = True
        t1.start()

        t2 = Thread(target = enqueue_output, args = (proc.stderr, ))
        t2.daemon = True
        t2.start()

    @staticmethod
    def subir_pokeapi(ouvido):
        pasta = ler_configuracao()["pokeapi"]
        SobeServidores.subir_servidor(ouvido, f'start "pokeapi" cmd /k python.exe "{pasta}\\manage.py" runserver --settings=config.local', SobeServidores.pokeapi_online)

    @staticmethod
    def subir_treinador(ouvido):
        pasta = ler_configuracao()["treinador"]
        SobeServidores.subir_servidor(ouvido, f'start "treinador" cmd /k python.exe "{pasta}\\treinador.py"', SobeServidores.treinador_online)

    @staticmethod
    def reset_treinador():
        resposta = api.post(f"{meu_site_treinador}/reset")
        if resposta.status_code != 200: raise Exception("Reset falhou")

    @staticmethod
    def api_online(url_get, crivo):
        try:
            resposta = api.get(url_get)
            print_debug(f"{resposta} - {resposta.text}")
            if resposta.status_code == 200 and crivo(resposta):
                return "online"
            return "zumbi"
        except exceptions.ConnectionError as x:
            print_debug(x)
            return "offline"
        except Exception as x:
            print_debug(x)
            return "zumbi"

    @staticmethod
    def pokeapi_online():
        def crivo(resposta):
            return resposta.json()['pokemon'] == f'{meu_site_pokeapi}/api/v2/pokemon/'
        return SobeServidores.api_online(f"{meu_site_pokeapi}/api/v2/", crivo)

    @staticmethod
    def treinador_online():
        def crivo(resposta):
            return resposta.text == 'Pikachu, eu escolho você!'
        return SobeServidores.api_online(f"{meu_site_treinador}/hello", crivo)

    @staticmethod
    def treinador_pid():
        try:
            resposta = api.get(f"{meu_site_treinador}/pid")
            if resposta.status_code == 200: return int(resposta.text)
            return -1
        except:
            return -1

    def __init__(self):
        self.para_offline()
        self.__pokeapi_falhou = False
        self.__treinador_falhou = False

    def para_offline(self):
        SobeServidores.apocalipse()
        self.__status = "offline"

    def apenas_pokeapi(self, ouvido, skipper):
        if self.__pokeapi_falhou:
            skipper("Não foi possível subir a PokeAPI anteriormente.")
            return
        try:
            if self.__status == "pokeapi": return
            if self.__status == "pokeapi+treinador": SobeServidores.matar(SobeServidores.treinador_pid())
            SobeServidores.subir_pokeapi(ouvido)
            self.__status = "pokeapi"
        except ServidorNaoOnlineException as e:
            self.__pokeapi_falhou = True
            self.para_offline()
            raise e

    def pokeapi_treinador(self, ouvido, skipper):
        if self.__treinador_falhou:
            skipper("Não foi possível subir a API do treinador anteriormente.")
            return
        try:
            if self.__status == "pokeapi+treinador":
                SobeServidores.reset_treinador()
                return
            self.apenas_pokeapi(ouvido, skipper)
            SobeServidores.subir_treinador(ouvido)
            self.__status = "pokeapi+treinador"
        except ServidorNaoOnlineException as e:
            self.__treinador_falhou = True
            self.para_offline()
            raise e

sobe = SobeServidores()

def teste_erro():
    raise Exception("Não rodou no teste anterior.")

bonus_check = teste_erro

def teste(grupo, qtd, tipo, penalidade = 0):
    def skipper(motivo):
        import unittest
        raise unittest.SkipTest(motivo)

    def nao_faz_nada():
        pass

    def nao_faz_nada_com_parametro(z):
        pass

    def pokeapi():
        sobe.apenas_pokeapi(sem_io.print_privilegiado, skipper)

    def treinador():
        sobe.pokeapi_treinador(sem_io.print_privilegiado, skipper)

    if tipo == "offline":
        before = sobe.para_offline
    elif tipo == "pokeapi":
        before = pokeapi
    elif tipo == "pokeapi+treinador":
        before = treinador
    elif tipo == "tanto faz":
        before = nao_faz_nada
    else:
        raise Exception(f"Tipo de teste {tipo} inválido.")

    return pontos_main.prepare(grupo, qtd, penalidade, before, nao_faz_nada_com_parametro, sem_io.print_privilegiado)

# Pokémons utilizados como massa de teste.
from pokemon import *
charizard = EspeciePokemon("charizard", "vermelho", "charmeleon", [])
pidgeotto = EspeciePokemon("pidgeotto", "marrom", "pidgey", ["pidgeot"])
pikachu = EspeciePokemon("pikachu", "amarelo", "pichu", ["raichu"])
raikou = EspeciePokemon("raikou", "amarelo", None, [])
gloom = EspeciePokemon("gloom", "azul", "oddish", ["vileplume", "bellossom"])
koffing = EspeciePokemon("koffing", "roxo", None, ["weezing"])
weezing = EspeciePokemon("weezing", "roxo", "koffing", [])
weepinbell = EspeciePokemon("weepinbell", "verde", "bellsprout", ["victreebel"])
victreebel = EspeciePokemon("victreebel", "verde", "weepinbell", [])
wobbuffet = EspeciePokemon("wobbuffet", "azul", "wynaut", [])
arbok = EspeciePokemon("arbok", "roxo", "ekans", [])
lickitung = EspeciePokemon("lickitung", "rosa", "lickilicky", [])
magikarp = EspeciePokemon("magikarp", "vermelho", None, ["gyarados"])
staryu = EspeciePokemon("staryu", "marrom", None, ["starmie"])
geodude = EspeciePokemon("geodude", "marrom", None, ["graveler"])
onix = EspeciePokemon("onix", "cinza", None, ["steelix"])