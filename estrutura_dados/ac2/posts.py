from random import seed, randint

seed(1)


class Posts:

    def __init__(self):
        self.posts = []

    def __str__(self):
        return str(self.posts)

    def sizeof_posts(self):
        return len(self.posts)

    def get_posts(self):
        return self.posts

    def create_post(self):
        self.posts.append(0)

    def give_likes(self, post, likes):
        index = post - 1
        first = 0
        last = len(self.posts) - 1

        if index < first or index > last:
            self.posts[randint(first, last)] += likes
            print("\nPost não existe. Escolhendo aleatoriamente...\n")
        elif index == first:
            if 1 <= likes <= 10:
                self.posts[index] += likes
                self.posts[index+1] += 1
            else:
                self.posts[index] += likes
                self.posts[index+1] += likes//2
        elif index == last:
            if 1 <= likes <= 10:
                self.posts[index] += likes
                self.posts[index-1] += 1
            else:
                self.posts[index] += likes
                self.posts[index-1] += likes//2
        else:
            if 1 <= likes <= 10:
                self.posts[index] += likes
                self.posts[index-1] += 1
                self.posts[index+1] += 1
            else:
                self.posts[index] += likes
                self.posts[index-1] += likes//2
                self.posts[index+1] += likes//2

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

    def menu_give_likes(self):
        nro_post = int(input('\nIngresse o número do post ao qual \
                             você quer dar likes: '))
        nro_likes = int(input('\nIngresse o número de likes que \
                              você quer atribuir: '))

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


socialmedia = Posts()
socialmedia.menu_principal()
