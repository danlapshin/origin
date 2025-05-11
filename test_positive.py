# Позитивная проверка:
# Заполняем форму валидными значениями, кликаем по кнопке [Request A Quote]
# ER: Форма засобмичена, formStatus = "Форма отправлена"

from playwright.sync_api import Page, expect


URL = 'https://qatest.datasub.com/index.html'
VALID = "form-control bg-light border-0 is-valid"
VALID2 = "form-select bg-light border-0 is-valid"


def test_form(page: Page):
    page.goto(URL)

    # Проскролили до формы для наглядности
    locator = page.get_by_label("Business")
    locator.scroll_into_view_if_needed()
    page.wait_for_timeout(3000)

    # Проверка поля name
    locator = page.get_by_placeholder("Your Name")
    locator.fill("Daniil")
    expect(locator).to_have_value("Daniil")
    expect(locator).to_have_class(VALID)

    # Проверка поля email
    locator = page.get_by_placeholder("Your Email").first
    locator.fill("asd@asd.com")
    expect(locator).to_have_value("asd@asd.com")
    expect(locator).to_have_class(VALID)

    # Проверка выбора значения из выпадающего списка
    # ----------------------------------------------
    # Реализация через селектор
    # ----------------------------------------------
    # new_selector = 'id=service'
    # page.wait_for_selector(new_selector)
    # handle = page.query_selector(new_selector)
    # handle.select_option(value="B Service")
    # ----------------------------------------------
    # Реализация через локатор
    # ----------------------------------------------
    locator = page.locator("select")
    locator.select_option(value="B Service")
    expect(locator).to_have_class(VALID2)

    # page.wait_for_timeout(3000)  # Задержка для отладки

    # Проверка состояния радиокнопок после того как выбрана "Business"
    locator = page.get_by_label("Business")
    locator.set_checked(True)
    expect(locator).to_be_checked()
    expect(page.get_by_label("Personal")).not_to_be_checked()

    # Проверка состояния чекбоксов после того как выбраны все
    locator = page.get_by_label("Cash")
    locator.set_checked(True)
    expect(locator).to_be_checked()

    locator = page.get_by_label("Card")
    locator.set_checked(True)
    expect(locator).to_be_checked()

    locator = page.get_by_label("Cryptocurrency")
    locator.set_checked(True)
    expect(locator).to_be_checked()

    # Проверка текстового блока
    locator = page.get_by_placeholder("Message")
    locator.fill("Test test test")
    expect(locator).to_have_value("Test test test")
    expect(locator).to_have_class(VALID)

    # Проверка нажатия на кнопку [Request A Quote]
    locator = page.get_by_role("button", name="Request A Quote").click()
    locator = page.locator("#formStatus")
    expect(locator).to_have_text("Форма отправлена.")
    expect(locator).to_be_visible()

    page.screenshot(path='./demo.png')

    page.wait_for_timeout(3000)  # Задержка для отладки
