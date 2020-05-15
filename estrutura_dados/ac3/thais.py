'''
Turma: 3º ADS C - periodo noturno
Disciplina: Estrutura de Dados
Professor: Jorge Carlos Valverde Rebaza
aluno: Thais Bonifacio Alves RA: 1900092
Data do envio: 07/05/2020

Pergunta 1: Ranking de Algoritmos de Ordenação

'''

import random, time, openpyxl

def bubble_sort(lista):
   
    n = len(lista)
    for i in range(n):
        ordenado = True #usamos uma flag para saber 
                            #se a lista já foi totalmente ordenada
        for j in range(n - i - 1):
            if lista[j] > lista[j + 1]:
                # fazemos a troca
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

                # o simples fato de eu ter feito a troca
                #já é um indicador de que a lista ainda não 
                #está totalmente ordenada
                ordenado = False

        # se não há mais trocas, então a lista está ordenada
        if ordenado:
            break
    return lista

'''

N = 1000
no_algor = 1
somatempo = 0
while N < 10000001:
    for i in range (1,11):
        ini = time.time()
        lista = [random.randint(0, N) for i in range(N+1)]
        #print("Lista inicial: ")
        #print(lista)
        lista_sorted = bubble_sort(lista)
        print(lista_sorted)
        fim = time.time() 
        tempo = round(fim-ini, 2)
        somatempo += tempo 
        print(tempo, N, i)
        i += 1
        ini -= ini
        if i == 10:
            
            media = somatempo/i
    no_algor += 1
    N *= 10 
'''


def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        ordenado = True #usamos uma flag para saber 
                            #se a lista já foi totalmente ordenada
        for j in range(n - i - 1):
            if lista[j] > lista[j + 1]:
                # fazemos a troca
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

                # o simples fato de eu ter feito a troca
                #já é um indicador de que a lista ainda não 
                #está totalmente ordenada
                ordenado = False

        # se não há mais trocas, então a lista está ordenada
        if ordenado:
            break

    return lista


N = 10
while N < 100:
    for i in range (1,11):
        somatempo = 0
        ini = time.time()
        lista = [random.randint(0, N) for i in range(N+1)]
        lista_sorted = bubble_sort(lista)
        for row in lista_sorted:
            wb= openpyxl.Workbook()
            filepath=f"/home/thais/algoritmo2_{N}_{i}.xlsx"
            sheet = wb.active
            sheet.append(lista_sorted)
            wb.save(filepath)
        print("Lista Ordenada com bubble-sort: ")
        print(lista_sorted)
        fim = time.time() 
        tempo = round(fim-ini, 2)
        somatempo += tempo 
        print(tempo, N, i)
        i += 1
        ini -= ini
        if i == 10:
            media = somatempo/i
            filepath = f"/home/thais/algoritmos.xlsx"
            sheet.cell(row=0, column=1).value = f"N= {N}"
            sheet.cell(row=0, column=2).value = f"N= {N}"
            sheet.cell(row=0, column=3).value = f"N= {N}"
            sheet.cell(row=0, column=4).value = f"N= {N}"
            sheet.cell(row=0, column=5).value = f"N= {N}"
            sheet.cell(row=1, column=0).value = f"Algoritmo 2"
            r, c = 1
            while sheet.cell(row=f"{r}", column=f"{c}").value != '':
                c += 1
                if sheet.cell(row=f"{r}", column=f"{c}").value == '':
                    sheet.cell(row=f"{r}", column=f"{c}").value == media
    N *= 10 