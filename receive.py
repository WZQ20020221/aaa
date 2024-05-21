import pika

# 连接 RabbitMQ 服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明一个队列名为 'hello'
channel.queue_declare(queue='hello')

# 定义接收消息的回调函数
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# 告诉 RabbitMQ 使用上面定义的回调函数来处理接收到的消息
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始监听队列，当有消息到达时调用回调函数处理消息
channel.start_consuming()