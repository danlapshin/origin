# Негативная проверка:
# Не заполняя форму кликаем по кнопке [Request A Quote]
# ER: Форма не отправляется, все обязательные поля подсвечены

from playwright.sync_api import Page, expect


URL = 'https://qatest.datasub.com/index.html'
INVALID = "form-control bg-light border-0 is-invalid"
VALID2 = "form-select bg-light border-0 is-valid"
INVALID2 = "form-select bg-light border-0 is-invalid"


def test_form(page: Page):
    page.goto(URL)

    # Проскролили до формы для наглядности
    locator = page.get_by_label("Business")
    locator.scroll_into_view_if_needed()
    page.wait_for_timeout(3000)

    # Проверка нажатия на кнопку [Request A Quote]
    locator = page.get_by_role("button", name="Request A Quote").click()
    locator = page.locator("#formStatus")  # пример использования id
    expect(locator).not_to_be_visible()

    # Проверка поля name
    expect(page.get_by_placeholder("Your Name")).to_have_class(INVALID)

    # Проверка поля email
    expect(page.get_by_placeholder("Your Email").first).to_have_class(INVALID)

    # Проверка выпадающего списка
    locator = page.locator("select")
    # -------------------
    # Выпадающий список реализован с ошибкой, поэтому
    # использована проверка с классом INVALID2, после фикса ошибки
    # заменить на класс VALID2
    expect(locator).to_have_class(INVALID2)

    # page.wait_for_timeout(3000)  # Задержка для отладки

    # Проверка состояния радиокнопок
    expect(page.get_by_label("Business")).not_to_be_checked()
    expect(page.get_by_label("Personal")).not_to_be_checked()

    # Проверка состояния чекбоксов после того как выбраны все
    expect(page.get_by_label("Cash")).not_to_be_checked()
    expect(page.get_by_label("Card")).not_to_be_checked()
    expect(page.get_by_label("Cryptocurrency")).not_to_be_checked()

    # Проверка текстового блока
    locator = page.get_by_placeholder("Message")
    # expect(locator).to_have_value("Test test test")
    expect(locator).to_be_empty
    expect(locator).to_have_class(INVALID)

    page.screenshot(path='./demo_neg.png')

    page.wait_for_timeout(3000)  # Задержка для отладки
