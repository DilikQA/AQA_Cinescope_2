import pytest
from constants import BASE_URL


class TestBookings:
    def test_create_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"


    def test_update_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Полное обновление бронирование
        update_booking = auth_session.put(f'{BASE_URL}/booking/{booking_id}', json=booking_data)
        assert update_booking.status_code == 200,  "Ошибка при обновлении брони"

        booking_id = update_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert update_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert update_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование полностью обновилось
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь обновлен успешно"


    def test_update_booking_partly(self, auth_session, booking_data):
        create_booking = auth_session.post(f'{BASE_URL}/booking', json=booking_data)
        assert create_booking.status_code == 200, 'Ошибка создания брони'

        booking_id = create_booking.json().get('bookingid')
        booking_name = create_booking.json()['booking']['firstname']
        # booking_add_info = create_booking.json()['booking']['additionalneeds']

        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert booking_name == booking_data['firstname'], "Заданное имя не совпадает"


        # Обновляем данные частично
        patch_booking = auth_session.patch(f'{BASE_URL}/booking/{booking_id}', json={
                                                                        'firstname':'Dilovar',
                                                                        'additionalneeds':'TV Set'
                                                                        })
        booking_id = create_booking.json().get('bookingid')
        # booking_name = patch_booking.json().get('firstname')
        # booking_add_info = patch_booking.json().get('additionalneeds')

        assert booking_id is not None, 'Идентификатор не найден'
        assert patch_booking.json()['firstname'] == 'Dilovar', "Заданное имя не совпадает"
        assert patch_booking.json()['additionalneeds'] == 'TV Set', "Заданное info не совпадает"


    def test_negavtive_get_test_cases(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/bookings/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"
