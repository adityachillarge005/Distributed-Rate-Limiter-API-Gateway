import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def process_queue():

    while True:
        job = r.rpop("gateway:queue")

        if job is None:
            break
        print("processing :",job)