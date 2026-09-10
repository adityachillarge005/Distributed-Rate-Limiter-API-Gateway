import redis
import time

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def check_sliding_window(user_id, limit=10, window=60):

    key = f"rate:sliding:user:{user_id}"

    current_time = time.time()

    oldest_allowed_time = current_time - window

    r.zremrangebyscore(key, "-inf", oldest_allowed_time)

    request_count = r.zcard(key)

    if request_count >= limit:
        return False
    else:
        r.zadd(key, {str(current_time): current_time})
        return True