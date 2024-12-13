# run this on the smartphone

import pika
import json
from datetime import datetime

class ChatReceiver:
    def __init__(self, host='', username='', password=''):
        # Connection parameters
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, credentials=credentials)
        )
        self.channel = self.connection.channel()
        
        # Declare the same queue
        self.channel.queue_declare(queue='chat_queue', durable=True)
    
    def callback(self, ch, method, properties, body):
        # Process received message
        message_data = json.loads(body)
        print(f"\nReceived at {message_data['timestamp']}:")
        print(f"From {message_data['sender']}: {message_data['message']}")
        
        # Acknowledge message receipt
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def start_receiving(self):
        # Set up consumer
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue='chat_queue',
            on_message_callback=self.callback
        )
        
        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()
    
    def close(self):
        self.connection.close()

# Example usage
if __name__ == "__main__":
    receiver = ChatReceiver()
    try:
        receiver.start_receiving()
    except KeyboardInterrupt:
        receiver.close()