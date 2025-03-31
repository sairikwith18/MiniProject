from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def connect_db():
    return sqlite3.connect("users.db")

@app.route("/check_email")
def check_email():
    email = request.args.get("email")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    return jsonify({"exists": bool(user)})

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
        else:
            conn = connect_db()
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                               (username, email, password))
                conn.commit()
                flash("Account created successfully! Redirecting to login...", "success")
                conn.close()
                return redirect(url_for("home"))
            except sqlite3.IntegrityError:
                flash("Email already registered!", "danger")

            conn.close()

    return render_template("signup.html")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_email"] = email  
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password!", "danger")

    return render_template("login.html")

bus_routes = {
    "300": ["Mehdipatnam", "Attapur", "Aramghar", "Chandrayangutta", "LB Nagar", "Uppal X Roads"],
    "113M": ["Mehdipatnam", "Lakdikapul", "Koti", "Dilsukhnagar", "Uppal", "Ghatkesar"],
    "1ZL": ["Secunderabad", "Tank Bund", "Liberty", "Abids", "Koti", "Langar House"],
    "505": ["Shankarpally", "CBIT", "Narsingi", "Ibrahim Bagh", "Langar House", "Mehdipatnam"],
    "5K": ["Secunderabad", "Patny", "Tank Bund", "Lakdikapul", "Masab Tank", "Mehdipatnam"],
    "49M": ["Secunderabad", "Panjagutta", "Nampally", "Lakdikapul", "Masab Tank", "Mehdipatnam"],
    "188/251": ["Shamshabad", "Aramghar", "Kismatpur", "Bandlaguda", "Langar House", "Mehdipatnam"],
    "126M": ["Secunderabad", "Paradise", "Panjagutta", "Madhapur", "Raidurg", "Gachibowli"],
    "217": ["Patancheru", "Lingampally", "Nanal Nagar", "Mehdipatnam", "NMDC", "Koti"],
    "218H": ["Patancheru", "Beeramguda", "Lingampally", "Miyapur", "Khairatabad", "Hayathnagar"]
}

@app.route("/get_bus_routes")
def get_bus_routes():
    return jsonify(bus_routes)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_email" not in session:
        return redirect(url_for("home"))
    return render_template("dashboard.html")

@app.route("/save_travel_details", methods=["POST"])
def save_travel_details():
    if "user_email" not in session:
        return redirect(url_for("home"))

    bus_number = request.form["bus_number"]
    bus_stop = request.form["bus_stop"]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO travel_details (user_email, bus_number, bus_stop) VALUES (?, ?, ?)",
                   (session["user_email"], bus_number, bus_stop))
    conn.commit()
    conn.close()

    flash("Travel details saved successfully!", "success")
    return redirect(url_for("menu"))  # ✅ Redirect to menu.html

@app.route("/menu")
def menu():
    return render_template("menu.html")  # ✅ Added menu route

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route('/map')
def map_page():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(debug=True)
