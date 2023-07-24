import os
import random
import string
from flask import Flask, render_template, redirect, request, abort

app = Flask(__name__)
app.secret_key = os.urandom(12)
shortener_urls = dict()


def generate_short_url(length: int = 6) -> str:
    chars = string.digits + string.ascii_letters
    short_url = ""

    while len(short_url) == 0 or short_url in shortener_urls:
        short_url = "".join(random.choice(chars) for _ in range(length))

    return short_url


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']

        if not long_url:
            abort(404)

        short_url = generate_short_url()
        shortener_urls[short_url] = long_url

        return render_template("short_url.html", result=f'{request.url_root}{short_url}')

    return render_template("index.html")


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortener_urls.get(short_url)

    if long_url:
        return redirect(long_url)

    return "URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)
