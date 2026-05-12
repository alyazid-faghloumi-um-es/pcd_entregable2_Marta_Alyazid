from kafka import KafkaProducer
import json
import random
import time


class Producer:
    def __init__(self, topic, freq):
        self.topic = topic
        self.freq = int(freq)

        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

        # IDs de canciones (1 a 20)
        self.ids_canciones = list(range(1, 21))

    def start_write(self):
        i = 0
        while True:
            evento = {
                "usuario_id": 1,
                "cancion_id": random.choice(self.ids_canciones)
            }

            self.producer.send(self.topic, value=evento)
            print(f'Message {i}: {evento}')

            i += 1
            time.sleep(self.freq)


if __name__ == '__main__':
    producer = Producer("escuchas", 2)
    producer.start_write()
