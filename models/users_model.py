from typing import Optional
from pydantic import BaseModel, Field, field_validator, ValidationError,  EmailStr
from constants import Roles



# class RegisteredUser(BaseModel):  # Создается класс User с помощью BaseModel от pydantic и указывается
#     email: EmailStr      # почта должно быть строкой
#     fullName: str # имя должно быть строкой
#     password: str = Field(max_length=8) # пароль должен быть строкой
#     passwordRepeat:str  # поле должно быть строкой
#     roles: list[Roles]   #Роли должен быть списком
#     banned: Optional[bool] = None
#     verified: Optional[bool] = None
#
#
#
# user = RegisteredUser(
#     email="testmail.com",
#     fullName="Ivan Ivanov",
#     password="12345678111",
#     passwordRepeat="12345678",
#     roles=[]
# )


class Product(BaseModel):  # Создается класс User с помощью BaseModel от pydantic и указывается
    name: str
    price: float
    in_stock: bool


product1 = Product(name='Telefon', price=2000, in_stock='false')
data = product1.model_dump_json()
print(data)

# Десериализация (JSON → Python)
new_user = Product.model_validate_json(data)
print(new_user)  # Вывод: Alice
















# def test_registered_user_validation(test_user, creation_user_data):
#     user_1 = RegisteredUser(**test_user)
#     user_2 = RegisteredUser(**creation_user_data)
#
#     print("USER FROM test_user:")
#     print(user_1.model_dump(exclude_unset=True))
#
#     print("\nUSER FROM creation_user_data:")
#     print(user_2.model_dump())
#
# from pydantic import BaseModel, Field, model_validator
# from enum import Enum
#
# class CardType(str, Enum):
#     VISA = "Visa"
#     AMEX = "American Express"
#
# class Card(BaseModel):
#     pan: str = Field(..., min_length=16, max_length=16)
#     cvc: str = Field(..., min_length=3, max_length=4)
#     card_type: CardType
#
#     @model_validator(mode="before")
#     def check_cvc_for_card_type(cls, values):
#         """
#         Проверяем, что:
#         - У карт VISA cvc == 3 цифры
#         - У карт AMEX cvc == 4 цифры
#         """
#         if values["card_type"] == CardType.VISA and len(values["cvc"]) != 3:
#             raise ValueError("CVC для VISA должен быть 3 цифры")
#         if values["card_type"] == CardType.AMEX and len(values["cvc"]) != 4:
#             raise ValueError("CVC для AMEX должен быть 4 цифры")
#         return values
#
#
#
