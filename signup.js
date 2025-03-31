document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault(); // Stop form submission temporarily

    let usernameField = document.querySelector("input[name='username']");
    let email = document.querySelector("input[name='email']").value;
    let password = document.querySelector("input[name='password']").value;
    let confirmPasswordField = document.querySelector("input[name='confirm_password']");

    if (usernameField && usernameField.value.length < 8) {
        alert("Username must be at least 8 characters long!");
        return;
    }

    let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(email)) {
        alert("Invalid email format!");
        return;
    }

    let passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!passwordPattern.test(password)) {
        alert("Password must be at least 8 characters long and include uppercase, lowercase, a number, and a special character!");
        return;
    }

    if (confirmPasswordField && password !== confirmPasswordField.value) {
        alert("Passwords do not match!");
        return;
    }

    // ✅ Check if email already exists
    fetch(`/check_email?email=${email}`)
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                alert("Email already exists! Please use another email.");
            } else {
                alert("Signup successful! Redirecting to login...");
                document.querySelector("form").submit(); // Proceed with form submission
            }
        })
        .catch(error => {
            console.error("Error checking email:", error);
        });
});
