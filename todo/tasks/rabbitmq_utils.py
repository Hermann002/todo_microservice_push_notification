import pika
import json

def send_task_to_rabbitmq(task_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='tasks_create')
    message = {'task_id': task_id}
    channel.basic_publish(exchange='', routing_key='tasks', body=json.dumps(message), properties=pika.BasicProperties(delivery_mode=2))

    print(f"Task {task_id} sent to RabbitMQ")
    connection.close()
    