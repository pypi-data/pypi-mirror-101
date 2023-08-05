import os
import dotenv

required = object()


def cast_bool(val):
    return val.lower() in {'1', 'yes', 'true', 'y', 'on'} if isinstance(val, str) else bool(val)


def cast_list(val):
    return [i.strip() for i in val.split(',')]


def cast_django_db(val):
    import dj_database_url
    return dj_database_url.parse(val)


def cast_django_email(val):
    import dj_email_url
    return dj_email_url.parse(val)


class Config:

    def __init__(self, filename='.env', **castings):
        self.filename = filename
        self.found_path = None

        self.castings = {
            bool: cast_bool,
            list: cast_list,
            'django_db': cast_django_db,
            'django_email': cast_django_email,
        }
        self.castings.update(**castings)

        if os.path.exists(self.filename):
            self.found_path = self.filename
        else:
            self.found_path = dotenv.find_dotenv(self.filename, usecwd=True)
        self.values = dotenv.dotenv_values(self.found_path, verbose=True)

    def add_castings(self, **kwargs):
        self.castings.update(kwargs)

    def __call__(self, key, *, default=required, cast=str):
        value = os.getenv(key)
        if value is None:
            value = self.values.get(key, default)

        if value is required:
            raise EnvironmentError(f'{key} is required')

        return None if value is None else self.castings.get(cast, cast)(value)


def __getattr__(name):
    if name == 'config':
        return Config()
