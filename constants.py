from enum import Enum

BASE_URL = 'https://auth.dev-cinescope.coconutqa.ru/'
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

LOGIN_ENDPOINT = '/login'
REGISTER_ENDPOINT = '/register'


class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"