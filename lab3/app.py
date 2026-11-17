"""Учебный стенд для ЛР3: страница логина и личный кабинет (Flask)."""
import random
import string

from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = "lab3-secret-key"

USERS = {"student": "Test123!"}

BASE_CSS = """
<style>
 body{font-family:Arial,sans-serif;background:#eef2f7;display:flex;justify-content:center;padding-top:50px}
 .card{background:#fff;padding:28px 32px;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,.12);width:320px}
 h1{font-size:22px;margin:0 0 18px;color:#2c3e50}
 label{display:block;font-size:14px;margin:10px 0 4px}
 input[type=text],input[type=password]{width:100%;box-sizing:border-box;padding:9px;border:1px solid #bbb;border-radius:5px}
 button{margin-top:16px;width:100%;padding:10px;background:#2980b9;color:#fff;border:none;border-radius:5px;font-size:15px}
 .flash{color:#c0392b;font-size:14px;margin-top:10px;min-height:18px}
 .row{display:flex;justify-content:space-between;align-items:center;margin-top:10px;font-size:13px}
 a{color:#2980b9}
</style>
"""

LOGIN_HTML = BASE_CSS + """
<div class="card">
  <h1 class="{{ rnd }}">Вход в систему</h1>
  <form method="post" action="/login">
    <label for="username">Логин</label>
    <input type="text" id="username" name="username" autocomplete="off">
    <label for="password">Пароль</label>
    <input type="password" id="password" name="password">
    <div class="row">
      <label><input type="checkbox" id="remember" name="remember"> Запомнить меня</label>
      <a href="#">Забыли пароль?</a>
    </div>
    <button type="submit" id="login-btn" class="btn-{{ rnd }}">Войти</button>
  </form>
  <div class="flash" id="flash">{{ error or "" }}</div>
</div>
"""

DASHBOARD_HTML = BASE_CSS + """
<div class="card">
  <h1 id="welcome">Добро пожаловать, {{ user }}!</h1>
  <p>Вы успешно вошли в личный кабинет.</p>
  <a id="logout" href="/logout">Logout</a>
</div>
"""


def rnd_class():
    # имитация автоматически сгенерированных CSS-классов (нестабильные селекторы)
    return "css-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form.get("username", "")
        pwd = request.form.get("password", "")
        if USERS.get(user) == pwd:
            session["user"] = user
            return redirect(url_for("dashboard"))
        error = "Неверный логин или пароль"
    return render_template_string(LOGIN_HTML, error=error, rnd=rnd_class())


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template_string(DASHBOARD_HTML, user=session["user"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(port=5003)
