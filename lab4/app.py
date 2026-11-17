"""Учебный стенд для ЛР4: контактная форма с серверной валидацией (Flask)."""
import re

from flask import Flask, render_template_string, request

app = Flask(__name__)

TOPICS = ["Вопрос по заказу", "Техническая поддержка", "Сотрудничество"]

HTML = """
<style>
 body{font-family:Arial,sans-serif;background:#f3f5f9;display:flex;justify-content:center;padding-top:30px}
 .card{background:#fff;padding:24px 30px;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,.12);width:420px}
 h1{font-size:22px;margin:0 0 14px;color:#2c3e50}
 label{display:block;font-size:14px;margin:10px 0 4px}
 input[type=text],input[type=email],select,textarea{width:100%;box-sizing:border-box;padding:8px;border:1px solid #bbb;border-radius:5px;font-size:14px}
 textarea{height:80px}
 .err{color:#c0392b;font-size:12px;min-height:14px}
 button{margin-top:14px;width:100%;padding:10px;background:#27ae60;color:#fff;border:none;border-radius:5px;font-size:15px}
 #success{background:#e8f8ef;border:1px solid #27ae60;color:#1e8449;padding:12px;border-radius:6px;margin-bottom:10px}
</style>
<div class="card">
  <h1>Связаться с нами</h1>
  {% if success %}<div id="success">Спасибо, {{ form.name }}! Ваше сообщение отправлено.</div>{% endif %}
  <form method="post" action="/contact" novalidate>
    <label for="name">Имя *</label>
    <input type="text" id="name" name="name" value="{{ form.name or '' }}">
    <div class="err" id="error-name">{{ errors.name or '' }}</div>
    <label for="email">E-mail *</label>
    <input type="email" id="email" name="email" value="{{ form.email or '' }}">
    <div class="err" id="error-email">{{ errors.email or '' }}</div>
    <label for="phone">Телефон</label>
    <input type="text" id="phone" name="phone" placeholder="+79991234567" value="{{ form.phone or '' }}">
    <div class="err" id="error-phone">{{ errors.phone or '' }}</div>
    <label for="topic">Тема обращения *</label>
    <select id="topic" name="topic">
      <option value="">— выберите —</option>
      {% for t in topics %}<option value="{{ t }}" {% if form.topic == t %}selected{% endif %}>{{ t }}</option>{% endfor %}
    </select>
    <div class="err" id="error-topic">{{ errors.topic or '' }}</div>
    <label for="message">Сообщение *</label>
    <textarea id="message" name="message">{{ form.message or '' }}</textarea>
    <div class="err" id="error-message">{{ errors.message or '' }}</div>
    <label><input type="checkbox" id="consent" name="consent" {% if form.consent %}checked{% endif %}> Согласен на обработку персональных данных *</label>
    <div class="err" id="error-consent">{{ errors.consent or '' }}</div>
    <button type="submit" id="submit">Отправить</button>
  </form>
</div>
"""

NAME_RE = re.compile(r"^[A-Za-zА-Яа-яЁё\- ]{2,50}$")
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
PHONE_RE = re.compile(r"^\+7\d{10}$")


def validate(f):
    errors = {}
    name = f.get("name", "").strip()
    if not name:
        errors["name"] = "Поле «Имя» обязательно для заполнения"
    elif not NAME_RE.match(name):
        errors["name"] = "Имя должно содержать от 2 до 50 букв"
    email = f.get("email", "").strip()
    if not email:
        errors["email"] = "Поле «E-mail» обязательно для заполнения"
    elif not EMAIL_RE.match(email):
        errors["email"] = "Введите корректный e-mail"
    phone = f.get("phone", "").strip()
    if phone and not PHONE_RE.match(phone):
        errors["phone"] = "Телефон в формате +7XXXXXXXXXX"
    if f.get("topic") not in TOPICS:
        errors["topic"] = "Выберите тему обращения"
    message = f.get("message", "").strip()
    if not message:
        errors["message"] = "Поле «Сообщение» обязательно для заполнения"
    elif len(message) < 10:
        errors["message"] = "Сообщение должно быть не короче 10 символов"
    if not f.get("consent"):
        errors["consent"] = "Необходимо согласие на обработку данных"
    return errors


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form, errors, success = {}, {}, False
    if request.method == "POST":
        form = request.form
        errors = validate(form)
        success = not errors
    return render_template_string(HTML, form=form, errors=errors, success=success, topics=TOPICS)


if __name__ == "__main__":
    app.run(port=5004)
