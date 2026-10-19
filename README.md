# MediQR — QR-Based Emergency Medical Information System

MediQR is a student-built web application that stores a user's medical profile and generates a QR code linked to that profile. It is intended as an educational prototype exploring how web technologies and QR codes can help make emergency medical information easier to retrieve.

> **Important:** This is a demo project, not a production-ready medical records system. Do not use it to store real patient information or rely on it for emergency care.

## Features

- Account signup, login, and logout
- Personal dashboard
- Medical profile creation and editing
- Medical details including name, age, gender, blood group, allergies, medical conditions, medications, and emergency contact
- Unique MediQR patient ID generation
- QR code image generation for a patient ID
- Patient record lookup by patient ID
- Browser-based QR scanning interface using the `html5-qrcode` library
- SQLite database storage

## Technology Stack

- **Python** — application logic
- **Flask** — web framework and routes
- **SQLite** — database
- **HTML** — page structure and templates
- **CSS** — page styling
- **JavaScript** — form requests, QR scanning, search, and page interactions
- **qrcode** and **Pillow** — QR image generation

## Project Structure

```text
MediQR/
├── app.py                 # Flask application and routes
├── database.py            # SQLite database operations
├── requirements.txt       # Python dependencies
├── .gitignore
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── register.html
│   ├── edit.html
│   └── patient.html
└── static/
    ├── script.js          # Browser interactions and QR scanner
    ├── style.css
    └── qr_codes/          # Generated QR images (created/used by the app)
```

The SQLite database (`mediqr.db`) is created/initialized by the application. Generated QR images may be stored under `static/qr_codes/`.

## Run Locally

### 1. Install Python

Install a supported Python 3 version if it is not already installed.

### 2. Clone the repository

```bash
git clone https://github.com/rbhavya277-glitch/MediQR.git
cd MediQR
```

### 3. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the application

```bash
python app.py
```

Open the local address printed in the terminal (typically `http://127.0.0.1:5000`) in your browser.

To stop the server, press `Ctrl+C` in the terminal.

## How It Works

1. A user creates an account and signs in.
2. The dashboard lets the user create or view a medical profile.
3. Flask validates the submitted fields and stores profile data in SQLite.
4. The application generates a unique MediQR ID and creates a QR image containing that ID.
5. The patient ID can be used to look up the associated record in the application.
6. The JavaScript scanner uses the browser camera (with permission) to read a QR code and navigate to the corresponding patient record.

Camera access may require `localhost` or HTTPS and permission from the browser. The QR scanner library is loaded from a third-party CDN, so an internet connection is needed for that feature.

## Privacy and Security Notice

This repository is an educational prototype and has **not** been hardened for real medical data. Before any real-world deployment, important changes are required, including:

- Store passwords using a secure password-hashing method instead of plain text.
- Replace the demo Flask secret key with a strong secret loaded from an environment variable.
- Restrict patient record access so users can only view or edit records they are authorized to access.
- Protect sensitive endpoints, including patient-data API routes.
- Add robust input validation, CSRF protection where appropriate, secure cookie settings, and production server configuration.
- Keep real patient records, local databases, credentials, and generated private data out of the public repository.
- Perform security and privacy testing before deployment.

**Never commit real patient records or secrets to GitHub.** The database and QR images in a local development folder should be reviewed before publishing.

## Future Improvements

- Strengthen authentication and role-based access control
- Improve privacy protections for patient record retrieval
- Add emergency-contact workflows
- Improve mobile usability and accessibility
- Add automated tests and clearer error handling
- Prepare a secure deployment configuration

## License

Check the repository for a `LICENSE` file. If no license is present, reuse and redistribution permissions have not been explicitly granted.
