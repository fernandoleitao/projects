import random

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


N = 100
lista = [random.randint(0, N) for i in range(N+1)]
print("Lista inicial: ")
print(lista)
lista_sorted = bubble_sort(lista)
print("Lista Ordenada com bubble-sort: ")
print(lista_sorted)



