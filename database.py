import sqlite3


DATABASE_NAME = "mediqr.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            allergies TEXT,
            medical_conditions TEXT,
            medications TEXT,
            emergency_contact TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Add user_id to existing patient tables if it does not exist
    columns = connection.execute(
        "PRAGMA table_info(patients)"
    ).fetchall()

    column_names = [column["name"] for column in columns]

    if "user_id" not in column_names:
        connection.execute(
            "ALTER TABLE patients ADD COLUMN user_id INTEGER"
        )
    connection.commit()
    connection.close()


def add_patient(
    patient_id,
    user_id,
    name,
    age,
    gender,
    blood_group,
    allergies,
    medical_conditions,
    medications,
    emergency_contact
):
    connection = get_connection()

    connection.execute("""
    INSERT INTO patients (
        patient_id,
        user_id,
        name,
        age,
        gender,
        blood_group,
        allergies,
        medical_conditions,
        medications,
        emergency_contact
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    patient_id,
    user_id,
    name,
    age,
    gender,
    blood_group,
    allergies,
    medical_conditions,
    medications,
    emergency_contact
))

    connection.commit()
    connection.close()


def get_patient(patient_id):
    connection = get_connection()

    patient = connection.execute(
        "SELECT * FROM patients WHERE patient_id = ?",
        (patient_id,)
    ).fetchone()

    connection.close()

    return patient


def update_patient(
    patient_id,
    name,
    age,
    gender,
    blood_group,
    allergies,
    medical_conditions,
    medications,
    emergency_contact
):
    connection = get_connection()

    connection.execute("""
        UPDATE patients
        SET
            name = ?,
            age = ?,
            gender = ?,
            blood_group = ?,
            allergies = ?,
            medical_conditions = ?,
            medications = ?,
            emergency_contact = ?
        WHERE patient_id = ?
    """, (
        name,
        age,
        gender,
        blood_group,
        allergies,
        medical_conditions,
        medications,
        emergency_contact,
        patient_id
    ))

    connection.commit()
    connection.close()


def create_user(username, password):
    connection = get_connection()

    existing_user = connection.execute(
        "SELECT user_id FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if existing_user:
        connection.close()
        return False

    connection.execute(
        """
        INSERT INTO users (username, password)
        VALUES (?, ?)
        """,
        (username, password)
    )

    connection.commit()
    connection.close()

    return True


def get_user(username, password):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT user_id, username
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    ).fetchone()


    connection.close()

    return user
def get_patient_by_user(user_id):
    connection = get_connection()

    patient = connection.execute(
        "SELECT * FROM patients WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    connection.close()

    return patient