import pika
import uuid
import time

def on_response(ch, method, props, body):
    if corr_id == props.correlation_id:
        print(" [.] 收到响应：%r" % body)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='', exclusive=True)
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

corr_id = str(uuid.uuid4())
channel.basic_consume(queue=callback_queue,
                      on_message_callback=on_response,
                      auto_ack=True)

channel.basic_publish(exchange='',
                      routing_key='rpc_queue',
                      properties=pika.BasicProperties(
                          reply_to=callback_queue,
                          correlation_id=corr_id,
                      ),
                      body=str(30))

print(" [x] 请求计算fib(30)")
while True:
    connection.process_data_events()
    time.sleep(0.5)