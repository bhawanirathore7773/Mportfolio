from .base import *  # noqa: F401,F403
from decouple import config

DEBUG = True
ALLOWED_HOSTS = ["*"]

# SQLite is fine for local development so contributors don't need Postgres
# running just to look at templates. Set DB_ENGINE in .env to override.
if config("USE_SQLITE", default=True, cast=bool):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
