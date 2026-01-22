from db_models.account_transactions import AccountTransactionTemplate
from utils.data_generator import DataGenerator
from sqlalchemy.orm import Session
import pytest
import allure


@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplate:

    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
    Этот тест проверяет корректность перевода денег между двумя счетами.
    Шаги:
    1. Создание двух счетов: Stan и Bob.
    2. Перевод 200 единиц от Stan к Bob.
    3. Проверка изменения балансов.
    4. Очистка тестовых данных.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ivan Petrovich")
    @allure.title("Тест перевода денег между счетами 200 рублей")
    def test_accounts_transaction_template(self, db_session: Session):
        # ====================================================================== Подготовка к тесту
        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan3 = AccountTransactionTemplate(user=f"Stan3_{DataGenerator.generate_random_int()}", balance=1000)
            bob3 = AccountTransactionTemplate(user=f"Bob3_{DataGenerator.generate_random_int()}", balance=500)
            db_session.add_all([stan3, bob3])
            db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        @allure.description("""
            функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
            и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """)
        def transfer_money(session, from_account, to_account, amount):
            with allure.step(" Получаем счета"):
                from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
                to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            with allure.step("Проверяем, что на счете достаточно средств"):
                if from_account.balance < amount:
                    raise ValueError("Недостаточно средств на счете")

            with allure.step("Выполняем перевод"):
                from_account.balance -= amount
                to_account.balance += amount

            with allure.step("Сохраняем изменения"):
                session.commit()

        # ====================================================================== Тест
        with allure.step("Проверяем начальные балансы"):
            assert stan3.balance == 1000
            assert bob3.balance == 500

        try:
            with allure.step("Выполняем перевод 200 единиц от stan3 к bob3"):
                transfer_money(db_session, from_account=stan3.user, to_account=bob3.user, amount=200)

            with allure.step("Проверяем, что балансы изменились"):
                assert stan3.balance == 800
                assert bob3.balance == 700

        except Exception as e:
            with allure.step("ОШИБКА откаты транзакции"):
                db_session.rollback()

            pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan3)
                db_session.delete(bob3)
                db_session.commit()


@pytest.mark.xfail(reason="Негативный тест. Недостатоная сумма баланса) ")
def test_negative_accounts_transaction_template(db_session: Session):
    # ====================================================================== Подготовка к тесту

    stan2 = AccountTransactionTemplate(user=f"Stan2_{DataGenerator.generate_random_int()}", balance=100)
    bob2= AccountTransactionTemplate(user=f"Bob2_{DataGenerator.generate_random_int()}", balance=500)

    # Добавляем записи в сессию
    db_session.add_all([stan2, bob2])
    # Фиксируем изменения в базе данных
    db_session.commit()

    def transfer_money(session, from_account, to_account, amount):
        """
        Переводит деньги с одного счета на другой.
        :param session: Сессия SQLAlchemy.
        :param from_account_id: ID счета, с которого списываются деньги.
        :param to_account_id: ID счета, на который зачисляются деньги.
        :param amount: Сумма перевода.
        """
        # Получаем счета
        from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
        to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

        # Проверяем, что на счете достаточно средств
        if from_account.balance < amount:
            # Удаляем данные для тестирования из базы
            db_session.delete(stan2)
            db_session.delete(bob2)
            # Фиксируем изменения в базе данных
            db_session.commit()
            raise ValueError("Недостаточно средств на счете")


        # Выполняем перевод
        from_account.balance -= amount
        to_account.balance += amount

        # Сохраняем изменения
        session.commit()

    # ====================================================================== Тест
    # Проверяем начальные балансы
    assert stan2.balance == 100
    assert bob2.balance == 500

    try:
        # Выполняем перевод 200 единиц от stan к bob2
        transfer_money(db_session, from_account=stan2.user, to_account=bob2.user, amount=200)

        # Проверяем, что балансы не изменились
        assert stan2.balance == 100
        assert bob2.balance == 500

    except Exception as e:
        # Если произошла ошибка, откатываем транзакцию
        db_session.rollback()  # откат всех введеных нами изменений
        pytest.fail(f"Ошибка при переводе денег: {e}")

    finally:
        # Удаляем данные для тестирования из базы
        db_session.delete(stan2)
        db_session.delete(bob2)
        # Фиксируем изменения в базе данных
        db_session.commit()