import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from models.base_models import TestUser
from entities import User
from constants import Roles
from faker import Faker

faker = Faker()



@pytest.fixture(scope="function")
def test_user() -> TestUser:
    """
       Генерация случайного пользователя для тестов.
    """
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.model_copy(update={
        "id": 'id',
        "verified": True,
        "banned": False
    })
    return updated_data


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)


    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=200
    )
    # response_data = response.json()
    registered_user = test_user.model_copy()
    return registered_user


@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture
def user_session():
    """
        Фикстура для создания пула сессий экземпляра ApiManager.
    """
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()



@pytest.fixture
def pre_filtered_movie(api_manager):
    """
    Создаёт фильм с фиксированными значениями для фильтрации.
    """
    movie = {
        "name": faker.sentence(nb_words=3).rstrip('.'),
        "imageUrl": "https://example.com/image.png",
        "description": faker.text(max_nb_chars=150),
        "genreId": 4,
        "price": 1001,
        "location": "MSK",
        "published": True
    }
    response = api_manager.movies_api.create_movie(data=movie)
    assert response.status_code == 201 or 200
    return response.json()


