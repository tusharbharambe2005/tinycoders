async function signup() {
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });
    
    const data = await response.json();
    alert(data.message);
    if (response.ok) {
        window.location.href = '/';
    }
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (data.access_token) {
        localStorage.setItem('token', data.access_token);
        alert('Login successful');
        window.location.href = '/';
    } else {
        alert(data.error);
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
}

// Redirect to home if already logged in
if (window.location.pathname === '/' && localStorage.getItem('token')) {
    window.location.href = '/home';
}
