// Dark mode functionality for the website that respects user's preferences while also allowing manual toggling with tailwindcss
// It should save the user's preference in the flask session so that it persists across page loads
// It should also update the UI to reflect the user's preference

function toggleDarkMode() {
    // Get the current state of dark mode from the body
    const body = document.body;
    const currentMode = body.classList.contains('dark');

    // If the current mode is dark, remove it, otherwise add it
    if (currentMode) {
        body.classList.remove('dark');
    } else {
        body.classList.add('dark');
    }

    // Save the user's preference in the session
    const darkMode = body.classList.contains('dark');
    fetch('/dark_mode', {
        method: 'POST',
        body: JSON.stringify({darkmode: darkMode}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(r => r.json())
        .then(data => {
            console.log(data);
        });
}

// Get the current state of dark mode from the session
fetch('/dark_mode', {
    method: 'GET'
}).then(r => r.json()).then(data => {if (data.darkmode) {document.body.classList.add('dark');}});

