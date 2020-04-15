'''
Curso: Analise e Desenvolvimento de Sistemas 
Disciplina: Estrutura de Dados
Professor: Jorge Carlos Valverde Rebaza 
Aluno:Fernando Nunes José Leitão RA: 1901296
Aluno: Thais Bonifacio Alves RA: 1900092
Turma: 3ºC - periodo noturno
Data do envio: 10/04/2020


Pergunta 1: Likes de Postagens em Redes Sociais (4 pontos)

'''



from random import seed, randint

seed(1)


'''
TAD Posts criado para gerenciar os posts
'''
class Posts:
    '''
    Único atributo é a lista de posts
    '''
    def __init__(self):
        self.posts = []

    def __str__(self):
        return str(self.posts)
    '''
    Este método retorna o tamanho de self.posts
    '''
    def sizeof_posts(self):
        return len(self.posts)
    '''
    Este método retorna self.posts
    '''
    def get_posts(self):
        return self.posts
    '''
    Este método cria um post
    '''
    def create_post(self):
        self.posts.append(0)
    '''
    Este método adiciona likes em um post
    '''
    def give_likes(self, post, likes):
        index = post - 1
        first = 0 #primeiro da lista
        last = len(self.posts) - 1 #último da lista

        if index < first or index > last: #Caso o índice esteja fora do range da lista de posts, da um like aleatório...
            self.posts[randint(first, last)] += likes
            print("\nPost não existe. Escolhendo aleatoriamente...\n")
        elif index == first: #Caso seja o primeiro ...
            if 1 <= likes <= 10:
                self.posts[index] += likes
                self.posts[index+1] += 1
            else:
                self.posts[index] += likes
                self.posts[index+1] += likes//2
        elif index == last: # Caso seja o último
            if 1 <= likes <= 10:
                self.posts[index] += likes
                self.posts[index-1] += 1
            else:
                self.posts[index] += likes
                self.posts[index-1] += likes//2
        else: # Se não for nem o primeiro nem o último ...
            if 1 <= likes <= 10:
                self.posts[index] += likes
                self.posts[index-1] += 1
                self.posts[index+1] += 1
            else:
                self.posts[index] += likes
                self.posts[index-1] += likes//2
                self.posts[index+1] += likes//2
    '''
    Esté método encontra os top 3 posts
    '''
    def show_top3(self):
        first = (0, 0)
        second = (0, 0)
        third = (0, 0)
        for idx, likes in enumerate(self.posts):
            if likes > first[1]:
                third = second
                second = first
                first = (idx, likes)
            elif likes > second[1]:
                third = second
                second = (idx, likes)
            elif likes > third[1]:
                third = (idx, likes)
        return [first, second, third]

    '''
    Menu principal
    '''
    def menu_principal(self):
        print('{:-^46s}'.format('Menu Sistema Gestor de Postagens'))
        print('\n1) Criar um post\n2) Dar likes em um post \
               \n3) Top 3 posts\n0) Sair\n')
        try:
            option = int(input('Entre com uma opção: '))
        except ValueError:
            print('Valor inválido')
            self.menu_principal()
        if option == 1:
            self.menu_create_post()
        if option == 2:
            self.menu_give_likes()
        if option == 3:
            self.menu_show_top3()
        if option == 0:
            print('\nAté Logo!')
    '''
    Menu Criar um post
    '''
    def menu_create_post(self):
        self.create_post()
        print('')
        print(f'O Post nro {self.sizeof_posts()} foi criado.\n')
        print('A lista de postagens é a seguinte\n')
        print('Índice:', end='\t')
        for idx, post in enumerate(self.get_posts()):
            print(idx, end=' \t')
        print('')
        print('Likes:', end='\t')
        for item in self.get_posts():
            print(item, end='\t')
        print('')
        while input('\nDigite R para voltar: ') != 'R':
            print('\nErro!')
        self.menu_principal()
    '''
    Menu dar likes
    '''
    def menu_give_likes(self):
        nro_post = int(input('\nIngresse o número do post ao qual você quer dar likes: '))
        nro_likes = int(input('\nIngresse o número de likes que você quer atribuir: '))

        self.give_likes(nro_post, nro_likes)
        print('')
        print('Índice:', end='\t')
        for idx, post in enumerate(self.get_posts()):
            print(idx, end='\t')
        print('')
        print('Likes:', end='\t')
        for item in self.get_posts():
            print(item, end='\t')
        print('')
        while input('\nDigite R para voltar: ') != 'R':
            print('\nErro!')
        self.menu_principal()
    '''
    Menu Mostrar Top 3
    '''
    def menu_show_top3(self):
        print('\nO top 3 posts com mais likes são:')
        print('')
        print('{:<8s}{:<8d}{:<8d}{:<8d}'.format('TOP', 1, 2, 3))
        print('Índice:', end='\t')
        for idx, likes in self.show_top3():
            print(idx, end='\t')
        print('')
        print('Likes:', end='\t')
        for idx, likes in self.show_top3():
            print(likes, end='\t')
        print('')
        while input('\nDigite R para voltar: ') != 'R':
            print('\nErro!')
        self.menu_principal()

'''
Cria um objeto 'Posts' e chama o método 'Menu Principal'
'''
socialmedia = Posts()
socialmedia.menu_principal()
