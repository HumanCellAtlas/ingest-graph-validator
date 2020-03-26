from time import sleep

from kombu import Connection
from kombu.pools import producers



connection_string = "amqp://guest:guest@localhost:5672"


def run_producer():
    print("Connecting ...")
    with Connection(connection_string) as conn:
        print("Connected.")
        print("Sending task ...")

        payload = {"submissionEnvelopeUuid": "668791ed-deec-4470-b23a-9b80fd133e1c"}

        with producers[conn].acquire(block=True) as producer:
            while True:
                producer.publish(payload, serializer="json", compression="bzip2", routing_key="ingest.graph.validation.queue")
                sleep(5)


if __name__ == "__main__":
    run_producer()
