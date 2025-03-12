import os

ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")

HOST_NAME: str = os.getenv("HOST_NAME", "")

PASSWORD_HASH: str = os.getenv("PASSWORD_HASH", "")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")

PAGINATE_PER_PAGE = int(os.getenv("PAGINATE_PER_PAGE", 20))

DATABASE_HOST: str = os.getenv("DATABASE_HOST", "postgres")
DATABASE_USER: str = os.getenv("DATABASE_USER", "shopping")
DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "test123")
DATABASE_DATABASE: str = os.getenv("DATABASE_DATABASE", "shopping")
