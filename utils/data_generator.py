import random
import string
from faker import Faker
import datetime
from typing import Optional, List, Dict

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase+string.digits, k=8))
        return f'kek{random_string}@gmail.com'

    @staticmethod
    def generate_random_name():
        return f'{faker.first_name()} {faker.last_name()}'

    @staticmethod
    def generate_random_int():
        return range(1,1000000)

    @staticmethod
    def generate_random_password():
        """
         Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters) #одна буква
        digits = random.choice(string.digits) #одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = '?@#$%^&*|:'
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_movie_data_for_db() -> dict:
        return {
            "id":random.randint(1, 10000000),
            "name": DataGenerator.generate_random_name(),
            "price": random.randint(100, 1000),
            "description": faker.text(max_nb_chars=150),
            "image_url": faker.image_url(),
            "location": random.choice(["MSK", "SPB"]),
            "published": random.choice([True, False]),
            "genre_id": random.randint(1, 5),
            "rating": round(random.uniform(1.0, 10.0), 1),
            "created_at": datetime.datetime.now().isoformat()
        }

    @staticmethod
    def generate_random_movie_data_for_api() -> dict:
        return {
            "name": DataGenerator.generate_random_name(),
            "imageUrl": faker.image_url(),
            "price": random.randint(100, 1000),
            "description": faker.text(max_nb_chars=150),
            "location": random.choice(["MSK", "SPB"]),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 5),
        }


    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    def generate_movies_params(
            price_from: Optional[int] = None,
            price_to: Optional[int] = None,
            locations: Optional[List[str]] = None,
            genre_id: Optional[int] = None,
    ) -> Dict:
        params = {}

        if price_from is not None:
            params["priceFrom"] = price_from

        if price_to is not None:
            params["priceTo"] = price_to

        if locations:
            params["locations"] = locations

        if genre_id is not None:
            params["genreId"] = genre_id

        return params