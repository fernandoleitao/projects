import pika
exchangeName = 'professor'
exchangeType = 'direct'
exchangeDurable = True

queueName = 'monitoramento_professor2'
routingKey = 'materia'

credentials = pika.PlainCredentials(username='guest', password='guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange=exchangeName, exchange_type=exchangeType, durable = exchangeDurable)
queue = channel.queue_declare(queue=queueName).method.queue
channel.queue_bind(exchange=exchangeName, queue=queue, routing_key=routingKey)
count = 1
def callback(ch, method, properties, body):
    print(f'Received: {body}')



channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
