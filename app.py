from flask import Flask, render_template, request, send_file, redirect
import sqlite3
import pandas as pd

app = Flask(__name__)

# LOGIN SYSTEM

@app.route("/login", methods=["GET","POST"])
def login():

    users = {
        "zonal": {"password":"1234","page":"/entries"},
        "hebbal": {"password":"1234","page":"/hebbal"},
        "whitefield": {"password":"1234","page":"/whitefield"},
        "koramangala": {"password":"1234","page":"/koramangala"},
        "yeshwanthpur": {"password":"1234","page":"/yeshwanthpur"},
        "yelahanka": {"password":"1234","page":"/yelahanka"},
        "rtnagar": {"password":"1234","page":"/rtnagar"},
        "banaswadi": {"password":"1234","page":"/banaswadi"},
        "horamavu": {"password":"1234","page":"/horamavu"}
    }

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username]["password"] == password:
            return redirect(users[username]["page"])

        else:
            return "Invalid login"

    return render_template("login.html")


# MAIN FORM

@app.route("/", methods=["GET","POST"])
def home():

    if request.method == "POST":

        zone = request.form.get("zone")
        area = request.form.get("area")
        sitting = request.form.get("sitting")
        name = request.form.get("name")
        place = request.form.get("place")
        date = request.form.get("date")
        duration = request.form.get("duration")
        contact_way = request.form.get("contact_way")
        phone = request.form.get("phone")
        language = request.form.get("language")
        evangelist = request.form.get("evangelist")
        supported_by = request.form.get("supported_by")
        topics = request.form.get("topics")
        status = request.form.get("status")
        sathvartha = request.form.get("sathvartha")

        conn = sqlite3.connect("evangelisation.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zone TEXT,
        area TEXT,
        sitting TEXT,
        name TEXT,
        place TEXT,
        date TEXT,
        duration TEXT,
        contact_way TEXT,
        phone TEXT,
        language TEXT,
        evangelist TEXT,
        supported_by TEXT,
        topics TEXT,
        status TEXT,
        sathvartha TEXT
        )
        """)

        cursor.execute("""
        INSERT INTO entries (
        zone, area, sitting, name, place, date, duration,
        contact_way, phone, language, evangelist,
        supported_by, topics, status, sathvartha
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
        zone, area, sitting, name, place, date, duration,
        contact_way, phone, language, evangelist,
        supported_by, topics, status, sathvartha
        ))

        conn.commit()
        conn.close()

    return render_template("index.html")


# ALL ENTRIES

@app.route("/entries")
def entries():

    conn = sqlite3.connect("evangelisation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entries")
    data = cursor.fetchall()

    conn.close()

    return render_template("entries.html", data=data)


# ZONE DASHBOARDS

@app.route("/hebbal")
def hebbal():

    conn = sqlite3.connect("evangelisation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entries WHERE zone='Hebbal'")
    data = cursor.fetchall()

    conn.close()

    return render_template("entries.html", data=data)


@app.route("/whitefield")
def whitefield():

    conn = sqlite3.connect("evangelisation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entries WHERE zone='Whitefield'")
    data = cursor.fetchall()

    conn.close()

    return render_template("entries.html", data=data)


@app.route("/koramangala")
def koramangala():

    conn = sqlite3.connect("evangelisation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entries WHERE zone='Koramangala'")
    data = cursor.fetchall()

    conn.close()

    return render_template("entries.html", data=data)


# AREA DASHBOARDS

@app.route("/yeshwanthpur")
def yeshwanthpur():

    conn = sqlite3.connect("evangelisation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entries WHERE area='Yeshwanthpur'")
    data = cursor.fetchall()

    conn.close()

    return render_template("entries.html", data=data)


@app.route("/yelahanka")
def yelahanka():

    conn = sqlite3.connect("evangelisation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entries WHERE area='Yelahanka'")
    data = cursor.fetchall()

    conn.close()

    return render_template("entries.html", data=data)


@app.route("/rtnagar")
def rtnagar():

    conn = sqlite3.connect("evangelisation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entries WHERE area='RT Nagar'")
    data = cursor.fetchall()

    conn.close()

    return render_template("entries.html", data=data)


@app.route("/banaswadi")
def banaswadi():

    conn = sqlite3.connect("evangelisation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entries WHERE area='Banaswadi'")
    data = cursor.fetchall()

    conn.close()

    return render_template("entries.html", data=data)


@app.route("/horamavu")
def horamavu():

    conn = sqlite3.connect("evangelisation.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entries WHERE area='Horamavu'")
    data = cursor.fetchall()

    conn.close()

    return render_template("entries.html", data=data)


# EXCEL DOWNLOAD

@app.route("/download")
def download():

    conn = sqlite3.connect("evangelisation.db")

    df = pd.read_sql_query("SELECT * FROM entries", conn)

    file = "evangelisation_report.xlsx"
    df.to_excel(file, index=False)

    conn.close()

    return send_file(file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)