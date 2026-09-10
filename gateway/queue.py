import redis

r =redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def add_to_queue(job):
    r.lpush("gateway:queue",job)