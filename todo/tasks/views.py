from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
import pika

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        task = serializer.save()

        # Connexion à RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Déclaration de la queue
        channel.queue_declare(queue='tasks_create')

        # Envoi du message
        channel.basic_publish(exchange='',
                              routing_key='tasks_create',
                              body=f"New task created: {task.title}")

        connection.close()
