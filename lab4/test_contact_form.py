import pytest

from pages.contact_page import ContactPage

VALID = dict(
    name="Мария",
    email="maria@example.com",
    phone="+79991234567",
    topic="Техническая поддержка",
    message="Здравствуйте! Не приходит письмо с подтверждением заказа.",
    consent=True,
)


@pytest.fixture
def page(driver, server):
    return ContactPage(driver, server).open()


def test_positive_all_fields_valid(page):
    """Позитивный сценарий: все поля заполнены валидными данными."""
    page.fill_form(**VALID).submit()
    assert page.success_message() == "Спасибо, Мария! Ваше сообщение отправлено."
    assert page.all_errors() == {}


def test_negative_empty_required_name(page):
    """Негативный сценарий: обязательное поле «Имя» пустое."""
    data = {**VALID, "name": ""}
    page.fill_form(**data).submit()
    assert not page.is_visible(page.SUCCESS)
    assert page.error_for("name") == "Поле «Имя» обязательно для заполнения"


# Дополнительно: правила из матрицы принятия решений (R2–R8)
@pytest.mark.parametrize(
    "rule, overrides, field, expected_error",
    [
        ("R2", {"name": "М"}, "name", "Имя должно содержать от 2 до 50 букв"),
        ("R3", {"email": ""}, "email", "Поле «E-mail» обязательно для заполнения"),
        ("R4", {"email": "maria.example.com"}, "email", "Введите корректный e-mail"),
        ("R5", {"phone": "89991234567"}, "phone", "Телефон в формате +7XXXXXXXXXX"),
        ("R6", {"topic": ""}, "topic", "Выберите тему обращения"),
        ("R7", {"message": "Коротко"}, "message", "Сообщение должно быть не короче 10 символов"),
        ("R8", {"consent": False}, "consent", "Необходимо согласие на обработку данных"),
    ],
    ids=["R2", "R3", "R4", "R5", "R6", "R7", "R8"],
)
def test_negative_decision_table(page, rule, overrides, field, expected_error):
    page.fill_form(**{**VALID, **overrides}).submit()
    assert page.error_for(field) == expected_error
    assert list(page.all_errors()) == [field]


def test_positive_without_optional_phone(page):
    """R9: необязательное поле «Телефон» пустое — форма отправляется."""
    page.fill_form(**{**VALID, "phone": ""}).submit()
    assert "Ваше сообщение отправлено" in page.success_message()
