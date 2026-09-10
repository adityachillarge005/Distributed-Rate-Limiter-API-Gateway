import redis
from pathlib import Path
import time

r = redis.Redis(   # connecting this python file with redis with settintg host , standard redis port, with the response to come in strings not in byte
    host="localhost",
    port=6379,
    decode_responses=True
)

lua_path = Path(__file__).resolve().parent.parent / "rate_limiter.lua" # file path to rate_limiter.lua

with open(lua_path, "r") as f:#to open file of lua path in read mode("r") and store in lua_script also closes file after reading
    lua_script = f.read()

rate_limiter = r.register_script(lua_script) #gives us a Python callable object that represents our Lua script


def check_rate_limit(user_id,capacity=10,refill_rate = 1):
    key = f"rate:user:{user_id}"#creates diff bucket for diff user

    result = rate_limiter(
        keys=[key],
        args=[
            int(time.time()),
            capacity,  # capacity
            refill_rate,   # refill rate
        ],
    )

    return result == 1