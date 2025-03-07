import os
import django
import pika
import json
import ssl

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontend.settings')
django.setup()

from api.models import Book

def get_rabbitmq_connection():
    """
    Establish a connection to Amazon MQ RabbitMQ.
    """
    # Amazon MQ endpoint
    endpoint = 'b-0af8867b-97dd-47cc-aad8-b579ba6bc935.mq.us-east-1.amazonaws.com'
    port = 5671  

    # Amazon MQ credentials (replace with your actual username and password)
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')

    # SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

    # Connection parameters
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(
        host=endpoint,
        port=port,
        credentials=credentials,
        ssl_options=pika.SSLOptions(context=ssl_context),
        virtual_host='/'
    )

    return pika.BlockingConnection(parameters)

def consume_book_events():
    """
    Consume 'book_created' and 'book_deleted' events from the 'book_queue'.
    """
    try:
        # Establish a connection to Amazon MQ RabbitMQ
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Declare the queue (if it doesn't exist)
        channel.queue_declare(queue='book_queue', durable=True)

        print(" [*] Waiting for book events. To exit, press CTRL+C")

        def callback(ch, method, properties, body):
            print(f"Received message: {body}")
            try:
                # Parse the message
                event = json.loads(body)
                event_type = event.get('event_type')  # 'book_created' or 'book_deleted'
                book_data = event.get('book_data')  # Book data for creation/update/deletion
               
                if event_type == 'book_created':
                    # Update or create the book in the Frontend API's database
                    Book.objects.update_or_create(
                        id=book_data['id'],
                        defaults={
                            'title': book_data['title'],
                            'author': book_data['author'],
                            'publisher': book_data['publisher'],
                            'category': book_data['category'],                         
                        }
                    )
                    print(f" [x] Updated/Created book: {book_data['title']}")

                elif event_type == 'book_deleted':
                    # Delete the book from the Frontend API's database
                    Book.objects.filter(id=book_data['id']).delete()
                    print(f" [x] Deleted book: {book_data['title']}")

                else:
                    print(f" [x] Unknown event type: {event_type}")

                # Acknowledge the message
                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                print(f"Failed to process event: {e}")
                # Reject the message and requeue it
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

        # Start consuming messages
        channel.basic_consume(queue='book_queue', on_message_callback=callback, auto_ack=False)
        channel.start_consuming()
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {e}")

if __name__ == "__main__":
    consume_book_events()