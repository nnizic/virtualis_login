const BACKEND_URL = 'http://127.0.0.1:8000'; // Backend URL

// Handle login form submission
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch(`${BACKEND_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        // Store relevant data in localStorage
        localStorage.setItem('username', data.username);
        localStorage.setItem('user_uuid', data.user_uuid);
        localStorage.setItem('verification_code', data.verification_code);

        alert('Login successful! You will now be redirected to verification.');

        // Redirect to the verification page
        window.location.href = `verify_code.html?user_uuid=${data.user_uuid}`;
      } else {
        const errorData = await response.json();
        document.getElementById('message').innerText = errorData.detail || 'Login failed!';
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });
}

// Handle verification form submission
const verifyForm = document.getElementById('verifyForm');
if (verifyForm) {
  verifyForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const enteredCode = document.getElementById('verification_code').value;
    const storedCode = localStorage.getItem('verification_code');

    if (enteredCode === storedCode) {
      alert('Verification successful! Redirecting to user page...');
      const user_uuid = localStorage.getItem('user_uuid');
      window.location.href = `user_page.html?user_uuid=${user_uuid}`;
    } else {
      document.getElementById('message').innerText = 'Invalid verification code. Please try again.';
    }
  });
}

// Handle welcome page actions
const usernameSpan = document.getElementById('username');
if (usernameSpan) {
  const username = localStorage.getItem('username');
  const user_uuid = localStorage.getItem('user_uuid');

  if (username && user_uuid) {
    usernameSpan.textContent = username;
    document
      .getElementById('userPageLink')
      .setAttribute('href', `user_page.html?user_uuid=${user_uuid}`);
  } else {
    alert('You need to log in first!');
    localStorage.clear();
    window.location.href = 'login.html';
  }
}

// Handle logout
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
  logoutBtn.addEventListener('click', () => {
    localStorage.clear();
    window.location.href = 'index.html';
  });
}
