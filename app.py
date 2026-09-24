from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from database import (
    initialize_database,
    add_patient,
    get_patient,
    get_patient_by_user,
    update_patient,
    create_user,
    get_user
)
import uuid
import qrcode
import os


app = Flask(__name__)

app.secret_key = "mediqr-demo-secret-key"


def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not session.get("logged_in"):
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return decorated_function


# Initialize the database
initialize_database()


# --------------------------------
# Home
# --------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------
# Dashboard
# --------------------------------

@app.route("/dashboard")
@login_required
def dashboard():

    patient_data = get_patient_by_user(session["user_id"])

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        patient=patient_data
    )

# --------------------------------
# Register Patient
# --------------------------------

@app.route("/register")
@login_required
def register():
    patient_data = get_patient_by_user(session["user_id"])

    if patient_data:
        return render_template(
            "patient.html",
            patient=patient_data,
            message=None
        )

    return render_template("register.html")


@app.route("/register-patient", methods=["POST"])
@login_required
def register_patient():

    try:
        data = request.get_json()

        name = data.get("name", "").strip()
        age = data.get("age")
        gender = data.get("gender", "").strip()
        blood_group = data.get("blood_group", "").strip()
        allergies = data.get("allergies", "").strip()
        medical_conditions = data.get("medical_conditions", "").strip()
        medications = data.get("medications", "").strip()
        emergency_contact = data.get("emergency_contact", "").strip()

        if not name or not age or not gender or not blood_group or not emergency_contact:
            return jsonify({
                "success": False,
                "message": "Please fill in all required fields."
            }), 400

        try:
            age = int(age)
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "message": "Age must be a number."
            }), 400

        patient_id = "MEDIQR-" + uuid.uuid4().hex[:8].upper()

        add_patient(
            patient_id,
            session["user_id"],
            name,
            age,
            gender,
            blood_group,
            allergies,
            medical_conditions,
            medications,
            emergency_contact
        )

        qr_folder = os.path.join("static", "qr_codes")
        os.makedirs(qr_folder, exist_ok=True)

        qr_data = patient_id
        qr = qrcode.make(qr_data)

        qr_filename = patient_id + ".png"
        qr_path = os.path.join(qr_folder, qr_filename)

        qr.save(qr_path)

        return jsonify({
            "success": True,
            "message": "Patient registered successfully.",
            "patient_id": patient_id,
            "qr_code": "/" + qr_path.replace("\\", "/")
        })

    except Exception as error:
        print("Error:", error)

        return jsonify({
            "success": False,
            "message": "Something went wrong while registering the patient."
        }), 500


# --------------------------------
# Patient Details
# --------------------------------

@app.route("/patient/<patient_id>")
@login_required
def patient(patient_id):

    patient_data = get_patient(patient_id)

    if patient_data is None:
        return render_template(
            "patient.html",
            patient=None,
            message="Patient record not found."
        )

    return render_template(
        "patient.html",
        patient=patient_data,
        message=None
    )


# --------------------------------
# Patient API
# --------------------------------

@app.route("/api/patient/<patient_id>")
def patient_api(patient_id):

    patient_data = get_patient(patient_id)

    if patient_data is None:
        return jsonify({
            "success": False,
            "message": "Patient record not found."
        }), 404

    return jsonify({
        "success": True,
        "patient": dict(patient_data)
    })


# --------------------------------
# Edit Patient
# --------------------------------

@app.route("/edit/<patient_id>")
@login_required
def edit_patient_page(patient_id):

    patient_data = get_patient(patient_id)

    if patient_data is None:
        return render_template(
            "patient.html",
            patient=None,
            message="Patient record not found."
        )

    return render_template(
        "edit.html",
        patient=patient_data
    )


# --------------------------------
# Update Patient
# --------------------------------

@app.route("/update-patient", methods=["POST"])
@login_required
def update_patient_record():

    try:
        data = request.get_json()

        patient_id = data.get("patient_id", "").strip()
        name = data.get("name", "").strip()
        age = data.get("age")
        gender = data.get("gender", "").strip()
        blood_group = data.get("blood_group", "").strip()
        allergies = data.get("allergies", "").strip()
        medical_conditions = data.get("medical_conditions", "").strip()
        medications = data.get("medications", "").strip()
        emergency_contact = data.get("emergency_contact", "").strip()

        if not patient_id or not name or not age or not gender or not blood_group or not emergency_contact:
            return jsonify({
                "success": False,
                "message": "Please fill in all required fields."
            }), 400

        try:
            age = int(age)
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "message": "Age must be a number."
            }), 400

        patient_data = get_patient(patient_id)

        if patient_data is None:
            return jsonify({
                "success": False,
                "message": "Patient record not found."
            }), 404

        update_patient(
            patient_id,
            name,
            age,
            gender,
            blood_group,
            allergies,
            medical_conditions,
            medications,
            emergency_contact
        )

        return jsonify({
            "success": True,
            "message": "Patient record updated successfully.",
            "patient_id": patient_id
        })

    except Exception as error:
        print("Error:", error)

        return jsonify({
            "success": False,
            "message": "Something went wrong while updating the patient."
        }), 500


# --------------------------------
# Login
# --------------------------------

@app.route("/login")
def login():

    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/login-user", methods=["POST"])
def login_user():

    try:
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return jsonify({
                "success": False,
                "message": "Please enter username and password."
            }), 400

        user = get_user(username, password)

        if user:

            session["logged_in"] = True
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]

            return jsonify({
                "success": True,
                "message": "Login successful."
            })

        return jsonify({
            "success": False,
            "message": "Invalid username or password."
        }), 401

    except Exception as error:
        print("Login error:", error)

        return jsonify({
            "success": False,
            "message": "Something went wrong during login."
        }), 500


# --------------------------------
# Logout
# --------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# --------------------------------
# Signup
# --------------------------------

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup-user", methods=["POST"])
def signup_user():

    try:
        data = request.get_json()

        username = data.get("username", "").strip()
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")

        if not username or not password or not confirm_password:
            return jsonify({
                "success": False,
                "message": "Please fill in all fields."
            }), 400

        if password != confirm_password:
            return jsonify({
                "success": False,
                "message": "Passwords do not match."
            }), 400

        if len(password) < 6:
            return jsonify({
                "success": False,
                "message": "Password must be at least 6 characters."
            }), 400

        created = create_user(username, password)

        if not created:
            return jsonify({
                "success": False,
                "message": "Username already exists."
            }), 409

        return jsonify({
            "success": True,
            "message": "Account created successfully."
        })

    except Exception as error:
        print("Signup error:", error)

        return jsonify({
            "success": False,
            "message": "Something went wrong while creating the account."
        }), 500


# --------------------------------
# Run Application
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)