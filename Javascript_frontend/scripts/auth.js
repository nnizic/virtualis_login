const BACKEND_URL = 'http://127.0.0.1:8000'; // Update with your backend's URL

// Handle registration
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
      document.getElementById('message').innerText = 'Username and password are required!';
      return;
    }

    const payload = { username, password };

    try {
      const response = await fetch(`${BACKEND_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        alert('Registration successful! Redirecting to login...');
        window.location.href = 'login.html';
      } else {
        document.getElementById('message').innerText = data.detail || 'Registration failed!';
      }
    } catch (error) {
      console.error('Error:', error);
      document.getElementById('message').innerText = 'Error connecting to server.';
    }
  });
}

// Handle login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
      document.getElementById('message').innerText = 'Username and password are required!';
      return;
    }

    const payload = { username, password };

    try {
      const response = await fetch(`${BACKEND_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        console.log(data);
        localStorage.setItem('username', data.username);
        localStorage.setItem('user_uuid', data.user_uuid);
        localStorage.setItem('verification_code', data.verification_code);

        alert('Login successful! Redirecting to welcome...');
        window.location.href = 'welcome.html';
      } else {
        document.getElementById('message').innerText = data.detail || 'Login failed!';
      }
    } catch (error) {
      console.error('Error:', error);
      document.getElementById('message').innerText = 'Error connecting to server.';
    }
  });
}
