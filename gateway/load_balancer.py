import redis 

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def get_next_backend():

    counter = r.incr("gateway:backend_counter")
    backend_number = ((counter-1)%3)+1
    return f"Backend {backend_number}"