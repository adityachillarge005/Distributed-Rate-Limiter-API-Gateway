from django.conf import settings

from .rate_limiter import check_rate_limit
from .sliding_window import check_sliding_window


def check_request_rate_limit(user_id):
    if settings.RATE_LIMIT_ALGORITHM == "token_bucket":
        return check_rate_limit(user_id)

    elif settings.RATE_LIMIT_ALGORITHM == "sliding_window":
        return check_sliding_window(user_id)

    return False