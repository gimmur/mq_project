# run this on the laptop

import pika
import json
from datetime import datetime

class ChatSender:
    def __init__(self, host='', username='', password=''):
        # Connection parameters
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, credentials=credentials)
        )
        self.channel = self.connection.channel()
        
        # Declare a queue for messages
        self.channel.queue_declare(queue='chat_queue', durable=True)
    
    def send_message(self, message):
        # Create message with timestamp
        payload = {
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sender': 'laptop'
        }
        
        # Send message to the queue
        self.channel.basic_publish(
            exchange='',
            routing_key='chat_queue',
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        print(f"Sent: {message}")
    
    def close(self):
        self.connection.close()

if __name__ == "__main__":
    sender = ChatSender()
    try:
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
            sender.send_message(message)
    finally:
        sender.close()