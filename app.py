from flask import Flask, render_template, request, redirect, flash
import sqlite3
import pickle
import re
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "health_prediction"

model = pickle.load(open("model.pkl", "rb"))

# Home Page
@app.route('/')
def home():

    search = request.args.get("search", "")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM patients WHERE full_name LIKE ?",
            ('%' + search + '%',)
        )
    else:
        cursor.execute("SELECT * FROM patients")

    patients = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        patients=patients,
        total_patients=total_patients
    )

# Add Patient
@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == "POST":

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']

        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            flash("Invalid Email Address")
            return redirect('/add')

        if datetime.strptime(dob, "%Y-%m-%d").date() > date.today():
            flash("DOB cannot be a future date")
            return redirect('/add')

        prediction = model.predict(
            [[glucose, haemoglobin, cholesterol]]
        )

        remarks = prediction[0]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO patients
        (
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        remarks
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("add.html")


# Edit Patient
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']

        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        prediction = model.predict(
            [[glucose, haemoglobin, cholesterol]]
        )

        remarks = prediction[0]

        cursor.execute("""
        UPDATE patients
        SET full_name=?,
            dob=?,
            email=?,
            glucose=?,
            haemoglobin=?,
            cholesterol=?,
            remarks=?
        WHERE id=?
        """,
        (
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks,
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute(
        "SELECT * FROM patients WHERE id=?",
        (id,)
    )

    patient = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        patient=patient
    )


# Delete Patient
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)