local tokens = tonumber(redis.call("HGET", KEYS[1], "tokens"))
local last_refill = tonumber(redis.call("HGET", KEYS[1], "last_refill_time"))

local current_time = tonumber(ARGV[1])
local capacity = tonumber(ARGV[2])
local refill_rate = tonumber(ARGV[3])

-- First request: create the bucket
if not tokens then
    tokens = capacity - 1

    redis.call("HSET", KEYS[1],
        "tokens", tokens,
        "last_refill_time", current_time
    )

    return 1
end

-- Calculate refill
local elapsed = current_time - last_refill
local refill = elapsed * refill_rate

tokens = math.min(capacity, tokens + refill)

-- Check whether request can proceed
if tokens >= 1 then
    tokens = tokens - 1

    redis.call("HSET", KEYS[1],
        "tokens", tokens,
        "last_refill_time", current_time
    )

    return 1
else
    redis.call("HSET", KEYS[1],
        "tokens", tokens,
        "last_refill_time", current_time
    )

    return 0
end