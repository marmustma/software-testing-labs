from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ContactPage(BasePage):
    """Page Object для страницы контактной формы /contact."""

    PATH = "/contact"
    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    TOPIC = (By.ID, "topic")
    MESSAGE = (By.ID, "message")
    CONSENT = (By.ID, "consent")
    SUBMIT = (By.ID, "submit")
    SUCCESS = (By.ID, "success")

    def open(self):
        return super().open(self.PATH)

    def fill_form(self, name="", email="", phone="", topic="", message="", consent=False):
        self.type(self.NAME, name)
        self.type(self.EMAIL, email)
        self.type(self.PHONE, phone)
        self.select(self.TOPIC, topic)
        self.type(self.MESSAGE, message)
        checkbox = self.find(self.CONSENT)
        if checkbox.is_selected() != consent:
            checkbox.click()
        return self

    def submit(self):
        self.click(self.SUBMIT)
        return self

    def success_message(self):
        return self.text_of(self.SUCCESS)

    def error_for(self, field):
        return self.text_of((By.ID, f"error-{field}"))

    def all_errors(self):
        fields = ["name", "email", "phone", "topic", "message", "consent"]
        return {f: self.error_for(f) for f in fields if self.error_for(f)}
