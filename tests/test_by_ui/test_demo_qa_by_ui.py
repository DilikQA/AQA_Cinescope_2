from playwright.sync_api import Page, expect
from datetime import datetime, date


def test2_text_box(page: Page):
    page.goto('https://demoqa.com/text-box')

    username_locator = '#userName'
    page.fill(username_locator, 'testQa')
    page.fill('#userEmail', 'test@qa.com')
    page.fill('#currentAddress', 'Phuket, Thalang 99')
    page.fill('#permanentAddress', 'Moscow, Mashkova 1')

    page.click('button#submit')

    expect(page.locator('#output #name')).to_have_text('Name:testQa')
    expect(page.locator('#output #email')).to_have_text('Email:test@qa.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :Phuket, Thalang 99')
    expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :Moscow, Mashkova 1')


from playwright.sync_api import Page
import time


def test_text_box(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    # вариант №1
    username_locator = '[placeholder="Имя Фамилия Отчество"]'
    page.fill(username_locator, 'Жмышенко Валерий Альбертович')

    # вариант №2
    page.locator('[placeholder="Имя Фамилия Отчество"]').fill('Жмышенко Валерий Альбертович')

    # вариант №3
    page.fill(selector='[placeholder="Имя Фамилия Отчество"]', value='Жмышенко Валерий Альбертович')

    time.sleep(10)


from playwright.sync_api import Page
from random import randint
import time


def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    # вариант №1
    username_locator = '[placeholder="Имя Фамилия Отчество"]'
    email_locator = '[placeholder="Email"]'
    password_locator = '[placeholder="Пароль"]'
    repeat_password_locator = '[placeholder="Повторите пароль"]'

    user_email = f'test_{randint(1, 9999)}@email.qa'

    page.fill(username_locator, 'Жмышенко Валерий Альбертович')
    page.fill(email_locator, user_email)
    page.fill(password_locator, 'qwerty123Q')
    page.fill(repeat_password_locator, 'qwerty123Q')

    page.click('[type="submit"]')

    time.sleep(10)

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)



import re
from playwright.sync_api import Page, expect


def test_practice_from(page: Page) -> None:
    page.goto("https://demoqa.com/")
    page.locator("div").filter(has_text="Forms").nth(5).click()
    page.get_by_text("Practice Form").click()

    page.get_by_role("textbox", name="First Name").fill("QA")
    page.get_by_role("textbox", name="Last Name").fill("Test")
    page.get_by_role("textbox", name="name@example.com").fill("dilik@mail.com")
    page.get_by_text("Male", exact=True).click()
    page.get_by_role("textbox", name="Mobile Number").fill("8905751770")

    page.get_attribute('#dateOfBirthInput', 'value')
    expect(page.locator('#dateOfBirthInput')).to_have_value(
        date.today().strftime("%d %b %Y")
    )

    page.locator("#dateOfBirthInput").click()
    page.get_by_role("option", name="Choose Monday, February 2nd,").click()
    page.get_by_text("Sports").click()
    page.locator("#subjectsInput").fill("M")
    page.get_by_text("Maths", exact=True).click()

    page.get_by_role("textbox", name="Current Address").fill("Phuket")
    page.locator("#state").click()
    page.get_by_text("NCR", exact=True).click()
    page.locator("#city").click()
    page.get_by_text("Delhi", exact=True).click()
    page.get_by_role("button", name="Submit").click()

    expect(page.locator("div").filter(has_text="Thanks for submitting the form").nth(3)).to_be_visible()

    expect(page.locator("tr", has_text="Student Email")
        .locator("td", has_text="dilik@mail.com")).to_be_visible()

    expect(page.locator("tr", has_text="Student Email")
        .locator("td", has_text="dilik@mail.com")).to_be_visible()




def test2_example(page: Page) -> None:
    page.goto("https://demoqa.com/")
    page.get_by_text("Elements").click()
    page.get_by_role("listitem").filter(has_text="Web Tables").click()
    page.get_by_role("button", name="Add").click()

    expect(page.get_by_text("Registration Form")).to_be_visible()

    page.get_by_placeholder('First Name').fill('AQA_DIL')
    page.locator("#lastName").type("Odinaev")
    page.locator("#userEmail").type("dilik56@mail.com")
    page.locator("#age").type('32')
    page.locator("#salary").type("4000")
    page.locator("#department").type("QA")

    page.wait_for_timeout(5000)

    page.locator("#submit").click()



def test_footer_text(page: Page) -> None:
    page.goto("https://demoqa.com/")
    page.locator('.footer').locator('span:has-text("© 2013-2020 TOOLSQA.COM | ALL")')



#Практическое задание / №1
# Написать тест на проверку активности элементов:
# 1. проверка активности 2 радиобаттонов и неактивности 3-го


def test_active_radio_buttons(page: Page) -> None:
    page.goto("https://demoqa.com/")
    page.get_by_text("Elements").click()
    page.get_by_role("listitem").filter(has_text="Radio Button").click()

    page.locator('#yesRadio').is_enabled()
    page.locator('#impressiveRadio').is_enabled()
    page.locator('#noRadio').is_disabled()


#Практическое задание / №2
# Написать тест на проверку видимости элементов:
#1. Написать проверку, что Home виден, а Desktop не виден
def test_checkboxes(page: Page) -> None:
    page.goto("https://demoqa.com/")
    page.get_by_text("Elements").click()
    page.get_by_role("listitem").filter(has_text="Check Box").click()

    expect(page.get_by_text("Home")).to_be_visible()
    expect(page.locator("span").filter(has_text="Desktop").first).not_to_be_visible()

    page.get_by_role("button", name="Toggle").click()
    expect(page.locator("span").filter(has_text="Desktop").first).to_be_visible()

#Практическое задание / №3
# Через 5 секунд после загрузки страницы появится элемент
def test_dynamic_elements(page: Page) -> None:
    page.goto("https://demoqa.com/")
    page.get_by_text("Elements").click()
    page.get_by_role("listitem").filter(has_text="Dynamic Properties").click()

    expect(page.get_by_role("button", name="Visible After 5 Seconds")).not_to_be_visible()
    page.wait_for_selector('#visibleAfter')
    expect(page.get_by_role("button", name="Visible After 5 Seconds")).to_be_visible()




