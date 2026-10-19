# MediQR 🏥

### QR-Based Emergency Medical Information System

MediQR is a web-based emergency medical information system designed to make essential medical information accessible during emergencies using a QR code.

The project allows users to manage their medical profiles and generate QR codes that can help others access important medical information when needed.

## 🚀 Features

- **User Login:** Provides a login interface for users.
- **Medical Dashboard:** Allows users to view their medical profile.
- **Profile Management:** Enables users to add or update their medical information.
- **QR Code Generation:** Generates a QR code associated with the user's medical profile.
- **QR Code Scanning:** Includes a QR scanning interface to support access to medical information.
- **Web Interface:** Provides a simple interface for interacting with the system.

## 🛠️ Technologies Used

- **HTML** — Structures the web pages.
- **CSS** — Styles the interface and improves the user experience.
- **JavaScript** — Handles client-side interactions and QR-related functionality.
- **Python (Flask)** — Provides the backend web application.
- **SQLite** — Stores application data.

## ⚙️ How It Works

1. The user logs in to the application.
2. The user accesses their medical dashboard.
3. The user adds or updates their medical profile.
4. The application generates a QR code associated with the profile.
5. The QR code can be scanned to access the information supported by the application.

**Note:** The information displayed and the scanning functionality depend on the application's implementation and configuration.

## 📂 Project Structure

The project contains the frontend, backend, and supporting files required to run the application.

Typical components include:

- HTML files for the web pages.
- CSS files for styling.
- JavaScript files for client-side functionality.
- Python files for Flask routes and backend logic.
- An SQLite database for application data.
- QR code-related files or functionality.

The exact file structure may vary depending on the current version of the project.

## ▶️ Getting Started

### Prerequisites

Install Python and ensure that Git is available if you want to clone the repository.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rbhavya277-glitch/MediQR.git
   ```

2. Navigate to the project directory:

   ```bash
   cd MediQR
   ```

3. Create and activate a virtual environment (recommended):

   **Windows PowerShell:**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. Install the dependencies listed in the project's `requirements.txt`, if available:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask application using the appropriate entry-point file.

   For example, if the main Flask file is named `app.py`:

   ```bash
   python app.py
   ```

6. Open the local URL displayed in your terminal.

**Important:** The exact installation commands depend on the filenames and dependencies in the repository. Make sure the entry-point file and dependency list match the actual project.

## 🔒 Security and Privacy

Medical information is sensitive. A production version should implement appropriate authentication, access controls, secure data storage, and protection against unauthorized access.

This project is an educational prototype and should not be used as a substitute for professional emergency medical services.

## 🔮 Future Improvements

- Improve QR scanning and medical profile retrieval.
- Strengthen authentication and authorization.
- Add emergency contact information.
- Improve mobile responsiveness.
- Enhance data privacy and security.
- Deploy the application for wider accessibility after appropriate security testing.

## 👥 Team Project

MediQR was developed as a student project to explore how web technologies and QR codes can support access to medical information during emergencies.

## 📄 License

See the [LICENSE](LICENSE) file for licensing information, if included in the repository.
