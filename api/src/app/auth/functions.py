import datetime

import jwt

from app.configs import configs


def generate_token():
    return jwt.encode(
        {
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(weeks=2),
        },
        key=configs.JWT_SECRET_KEY,
        algorithm=configs.JWT_ALGORITHM,
    )
