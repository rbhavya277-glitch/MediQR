// ===============================
// MediQR - Main JavaScript
// ===============================


// --------------------------------
// QR Scanner
// --------------------------------

let qrScanner = null;


function showComingSoon() {

    // Create scanner window
    const scannerOverlay = document.createElement("div");

    scannerOverlay.id = "scannerOverlay";

    scannerOverlay.innerHTML = `
        <div class="scanner-box">

            <button class="close-scanner" onclick="closeScanner()">
                ×
            </button>

            <h2>Scan MediQR</h2>

            <p>
                Allow camera access and point it at the patient's QR code.
            </p>

            <div id="qr-reader"></div>

            <p id="scannerMessage">
                Starting camera...
            </p>

        </div>
    `;

    document.body.appendChild(scannerOverlay);


    // Load QR scanner library
    if (typeof Html5Qrcode === "undefined") {

        const script = document.createElement("script");

        script.src =
            "https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js";

        script.onload = function () {
            startQRScanner();
        };

        script.onerror = function () {

            document.getElementById("scannerMessage").textContent =
                "Unable to load the QR scanner. Please check your internet connection.";

        };

        document.head.appendChild(script);

    } else {

        startQRScanner();

    }
}


// --------------------------------
// Start QR Scanner
// --------------------------------

function startQRScanner() {

    const scannerMessage =
        document.getElementById("scannerMessage");


    if (!scannerMessage) {
        return;
    }


    qrScanner = new Html5Qrcode("qr-reader");


    const scannerConfig = {
        fps: 10,
        qrbox: {
            width: 250,
            height: 250
        }
    };


    qrScanner.start(

        {
            facingMode: "environment"
        },

        scannerConfig,

        function (decodedText) {

            // QR code successfully scanned
            console.log("QR Code detected:", decodedText);

            scannerMessage.textContent =
                "QR code detected. Opening patient record...";


            // Stop the camera
            qrScanner.stop()
                .then(function () {

                    qrScanner.clear();

                    // Open the patient record
                    window.location.href =
                        "/patient/" + encodeURIComponent(decodedText);

                })
                .catch(function (error) {

                    console.error(
                        "Unable to stop scanner:",
                        error
                    );

                    window.location.href =
                        "/patient/" + encodeURIComponent(decodedText);

                });

        },

        function (errorMessage) {

            // QR code has not been detected yet.
            // We intentionally do not display every scanning error.
        }

    )
    .catch(function (error) {

        console.error(
            "Camera error:",
            error
        );

        scannerMessage.textContent =
            "Unable to access the camera. Please allow camera permission and try again.";

    });
}


// --------------------------------
// Close QR Scanner
// --------------------------------

function closeScanner() {

    const scannerOverlay =
        document.getElementById("scannerOverlay");


    if (qrScanner) {

        qrScanner.stop()
            .then(function () {

                qrScanner.clear();

                qrScanner = null;

                if (scannerOverlay) {
                    scannerOverlay.remove();
                }

            })
            .catch(function (error) {

                console.error(
                    "Error closing scanner:",
                    error
                );

                qrScanner = null;

                if (scannerOverlay) {
                    scannerOverlay.remove();
                }

            });

    } else {

        if (scannerOverlay) {
            scannerOverlay.remove();
        }

    }
}


// --------------------------------
// Patient Registration
// --------------------------------

const registrationForm =
    document.getElementById("registrationForm");


if (registrationForm) {

    registrationForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const formMessage =
                document.getElementById("formMessage");


            const patientData = {

                name:
                    document.getElementById("name").value.trim(),

                age:
                    document.getElementById("age").value,

                gender:
                    document.getElementById("gender").value,

                blood_group:
                    document.getElementById("blood_group").value,

                allergies:
                    document.getElementById("allergies").value.trim(),

                medical_conditions:
                    document
                        .getElementById("medical_conditions")
                        .value.trim(),

                medications:
                    document
                        .getElementById("medications")
                        .value.trim(),

                emergency_contact:
                    document
                        .getElementById("emergency_contact")
                        .value.trim()
            };


            formMessage.textContent =
                "Registering patient...";


            try {

                const response = await fetch(
                    "/register-patient",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(patientData)
                    }
                );


                const result =
                    await response.json();


                if (result.success) {

                    formMessage.textContent =
                        "Patient registered successfully!";


                    registrationForm.reset();


                    setTimeout(function () {

                        window.location.href =
                            "/patient/" +
                            result.patient_id;

                    }, 1000);


                } else {

                    formMessage.textContent =
                        result.message;

                }

            } catch (error) {

                console.error(
                    "Registration error:",
                    error
                );


                formMessage.textContent =
                    "Unable to connect to the server.";

            }

        }
    );
}
// --------------------------------
// Patient ID Search
// --------------------------------

function searchPatient() {

    const input =
        document.getElementById("patientIdInput");

    const message =
        document.getElementById("searchMessage");


    if (!input || !message) {
        return;
    }


    const patientId =
        input.value.trim().toUpperCase();


    if (!patientId) {

        message.textContent =
            "Please enter a Patient ID.";

        return;
    }


    if (!patientId.startsWith("MEDIQR-")) {

        message.textContent =
            "Please enter a valid MediQR Patient ID.";

        return;
    }


    message.textContent =
        "Searching for patient record...";


    window.location.href =
        "/patient/" + encodeURIComponent(patientId);
}
// --------------------------------
// Edit Patient Record
// --------------------------------

const editPatientForm =
    document.getElementById("editPatientForm");


if (editPatientForm) {

    editPatientForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const editMessage =
                document.getElementById("editMessage");


            const patientData = {

                patient_id:
                    document.getElementById("patient_id").value,

                name:
                    document.getElementById("name").value.trim(),

                age:
                    document.getElementById("age").value,

                gender:
                    document.getElementById("gender").value,

                blood_group:
                    document.getElementById("blood_group").value,

                allergies:
                    document.getElementById("allergies").value.trim(),

                medical_conditions:
                    document
                        .getElementById("medical_conditions")
                        .value.trim(),

                medications:
                    document
                        .getElementById("medications")
                        .value.trim(),

                emergency_contact:
                    document
                        .getElementById("emergency_contact")
                        .value.trim()
            };


            editMessage.textContent =
                "Saving changes...";


            try {

                const response = await fetch(
                    "/update-patient",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(patientData)
                    }
                );


                const result =
                    await response.json();


                if (result.success) {

                    editMessage.textContent =
                        "Patient record updated successfully!";


                    setTimeout(function () {

                        window.location.href =
                            "/patient/" +
                            result.patient_id;

                    }, 1000);


                } else {

                    editMessage.textContent =
                        result.message;

                }

            } catch (error) {

                console.error(
                    "Update error:",
                    error
                );


                editMessage.textContent =
                    "Unable to connect to the server.";

            }

        }
    );
}
// --------------------------------
// Staff Login
// --------------------------------

const loginForm =
    document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const loginMessage =
                document.getElementById("loginMessage");


            const username =
                document.getElementById("username").value.trim();

            const password =
                document.getElementById("password").value;


            loginMessage.textContent =
                "Logging in...";


            try {

                const response = await fetch(
                    "/login-user",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            username: username,
                            password: password
                        })
                    }
                );


                const result =
                    await response.json();


                if (result.success) {

                    loginMessage.textContent =
                        "Login successful!";


                    setTimeout(function () {

                        window.location.href = "/dashboard";

                    }, 700);


                } else {

                    loginMessage.textContent =
                        result.message;

                }

            } catch (error) {

                console.error(
                    "Login error:",
                    error
                );


                loginMessage.textContent =
                    "Unable to connect to the server.";

            }

        }
    );
}
// --------------------------------
// User Signup
// --------------------------------

const signupForm =
    document.getElementById("signupForm");


if (signupForm) {

    signupForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const signupMessage =
                document.getElementById("signupMessage");


            const username =
                document.getElementById("signupUsername").value.trim();

            const password =
                document.getElementById("signupPassword").value;

            const confirmPassword =
                document
                    .getElementById("signupConfirmPassword")
                    .value;


            signupMessage.textContent =
                "Creating account...";


            try {

                const response = await fetch(
                    "/signup-user",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            username: username,
                            password: password,
                            confirm_password: confirmPassword
                        })
                    }
                );


                const result =
                    await response.json();


                if (result.success) {

                    signupMessage.textContent =
                        "Account created successfully!";


                    setTimeout(function () {

                        window.location.href =
                            "/login";

                    }, 1000);


                } else {

                    signupMessage.textContent =
                        result.message;

                }

            } catch (error) {

                console.error(
                    "Signup error:",
                    error
                );


                signupMessage.textContent =
                    "Unable to connect to the server.";

            }

        }
    );
}