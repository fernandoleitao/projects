

import random

def merge_sort(lista):
    # se a lista tem menos de 2 elementos, 
    # retorna a lista sem fazer nada
    if len(lista) < 2:
        return lista

    #caso contrario a lista é dividida em duas partes
    centro = len(lista) // 2

    #chamadas recursivas para listas da esquerda e direita
    lista_L = merge_sort(lista[:centro])
    lista_R = merge_sort(lista[centro:])
    
    #juntamos o resultado da partição das duas listas anteriores 
    return merge(lista_L, lista_R)



def merge(lista_L, lista_R):
    # se uma lista está vazia, então não faço nada
    # e devo retornar a outra lista
    if len(lista_L) == 0:
        return lista_R

    # se a segunda lista está vazia, então não faço nada
    # e retorno a primeira lista
    if len(lista_R) == 0:
        return lista_L

    result = []
    index_L = index_R = 0

    # iremos processar tanto a lista da esquerda quanto
    # a lista da direita, então a lista de resultado deverá
    # terminar com o mesmo numero de elementos do que ambas listas
    while len(result) < len(lista_L) + len(lista_R):
        # realizo a ordenação e vou salvando na nova lista de resultados
        if lista_L[index_L] <= lista_R[index_R]:
            result.append(lista_L[index_L])
            index_L += 1
        else:
            result.append(lista_R[index_R])
            index_R += 1

        # Se alguma das listas é "esvaziada" então
        # copio os elementos restantes da outra lista
        # na lista de resultados e fecho/interrumpo o loop 
        if index_R == len(lista_R):
            result += lista_L[index_L:]
            break

        if index_L == len(lista_L):
            result += lista_R[index_R:]
            break

    return result


N = 100
lista = [random.randint(0, N) for i in range(N+1)]
print(lista)
lista_sorted = merge_sort(lista)
print("Lista Ordenada com mergesort:")
print(lista_sorted)
