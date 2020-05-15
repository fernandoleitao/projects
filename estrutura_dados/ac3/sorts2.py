'''
Turma: 3º ADS C - periodo noturno
Disciplina: Estrutura de Dados
Professor: Jorge Carlos Valverde Rebaza
aluno: Fernando Nunes José Leitão RA: 1901296
aluno: Allan Messias Cardoso RA: 1900309
aluno: Thais Bonifacio Alves RA: 1900092
Data do envio: 07/05/2020

Pergunta 1: Ranking de Algoritmos de Ordenação

'''

''' 
TAD para execução de sorts
'''

import random, time, openpyxl

class Sort:
    
    def bubble_sort(self, lista):
        n = len(lista)
        for i in range(n):
            ordenado = True 
            for j in range(n - i - 1):
                if lista[j] > lista[j + 1]:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
                    ordenado = False
            if ordenado:
                break
        return lista

    def merge_sort(self, lista):
        if len(lista) < 2:
            return lista
        centro = len(lista) // 2
        lista_L = self.merge_sort(lista[:centro])
        lista_R = self.merge_sort(lista[centro:])
        return self.merge(lista_L, lista_R)

    def merge(self, lista_L, lista_R):
        if len(lista_L) == 0:
            return lista_R
        if len(lista_R) == 0:
            return lista_L
        result = []
        index_L = index_R = 0
        while len(result) < len(lista_L) + len(lista_R):
            if lista_L[index_L] <= lista_R[index_R]:
                result.append(lista_L[index_L])
                index_L += 1
            else:
                result.append(lista_R[index_R])
                index_R += 1
            if index_R == len(lista_R):
                result += lista_L[index_L:]
                break
            if index_L == len(lista_L):
                result += lista_R[index_R:]
                break
        return result

    def insertion_sort(self, lista):
        for index in range(1,len(lista)):
            value = lista[index]
            i = index - 1
            while i >= 0:
                if value < lista[i]:
                    lista[i+1] = lista[i]
                    lista[i] = value
                    i -= 1
                else:
                    break
        return lista

    def quick_sort(self, lista):
        return self.quick_sort2(lista, 0, len(lista)-1)

    def quick_sort2(self, lista, first, last):
        if first < last:   
            pi = self.partition(lista,first,last) 
            self.quick_sort2(lista, first, pi-1) 
            self.quick_sort2(lista, pi+1, last)
        return lista

    def partition(self, lista, first, last): 
        i = ( first-1 )       
        pivot = lista[last]  
        for j in range(first , last): 
            if   lista[j] <= pivot: 
                i = i+1 
                lista[i],lista[j] = lista[j],lista[i] 
        lista[i+1],lista[last] = lista[last],lista[i+1] 
        return ( i+1 ) 

    def counting_sort(self, lista):
        return self.counting_sort2(lista, max(lista))

    def counting_sort2(self, lista, max_val):
        m = max_val + 1
        count = [0] * m                
    
        for a in lista:
            count[a] += 1             
        i = 0
        for a in range(m):            
            for c in range(count[a]):  
                lista[i] = a
                i += 1
        return lista

'''
Criando a Tabela conforme instruções ...
'''

wb= openpyxl.Workbook()
filepath="/home/fernando/Projects/estrutura_dados/ac3/algoritmos.xlsx"
sheet = wb.active
sheet.cell(row=1, column=2).value = "N=1000"
sheet.cell(row=1, column=3).value = "N=10000"
sheet.cell(row=1, column=4).value = "N=100000"
sheet.cell(row=1, column=5).value = "N=1000000"
sheet.cell(row=1, column=6).value = "N=10000000"
sheet.cell(row=2, column=1).value = "Bubble Sort"
sheet.cell(row=3, column=1).value = "Merge Sort"
sheet.cell(row=4, column=1).value = "Insertion Sort"
sheet.cell(row=5, column=1).value = "Quick Sort"
sheet.cell(row=6, column=1).value = "Counting Sort"

def rodar(fnc, N, c, r):
    while N <= 100000:
        somatempo = 0
        for i in range (1,11):
            ini = time.time()
            lista = [random.randint(0, N) for i in range(N+1)]
            lista_sorted = fnc(lista)
            print(f"Lista Ordenada com {sheet.cell(row=r, column=1).value}")
            print(lista_sorted)
            fim = time.time() 
            tempo = round(fim-ini, 2)
            somatempo += tempo 
            print(f'time: {tempo} round: {i}')
            if i == 10:
                media = somatempo/i
                sheet.cell(row=r, column=c).value = media
                c += 1
                wb.save(filepath) 
        N *= 10
'''
Rodando as funções ...
'''
N = 1000 # numero inicial
c = 2 # coluna inicial
sort = Sort()
rodar(sort.bubble_sort, N, c, 2)
#rodar(sort.merge_sort, N, c, 3)
rodar(sort.insertion_sort, N, c, 4)
#rodar(sort.quick_sort, N, c, 5)
#rodar(sort.counting_sort, N, c, 6)

wb.save(filepath)