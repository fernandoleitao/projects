import pika
count = 1
credentials = pika.PlainCredentials(username='guest', password='guest')
while True:
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()
    userinput = input('insira a msg : ')
    channel.basic_publish(exchange='aluno',
                          routing_key='matricula',
                          body=userinput)   
    print(f' [{count}] Sent : ', userinput)   
    count = count + 1



    
