// Handle welcome page actions
const usernameSpan = document.getElementById('username');
if (usernameSpan) {
  const username = localStorage.getItem('username');
  const useruuid = localStorage.getItem('user_uuid');
  if (username && useruuid) {
    console.log(username);
    usernameSpan.textContent = username;
    document
      .getElementById('userPageLink')
      .setAttribute('href', `user_page.html?user_uuid=${useruuid}`);
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

// Handle user verification
const verifyForm = document.getElementById('verifyForm');
if (verifyForm) {
  verifyForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const enteredCode = document.getElementById('verification_code').value;
    const storedCode = localStorage.getItem('verification_code');

    if (enteredCode === storedCode) {
      alert('Verification successful!');
      window.location.href = 'user_page.html';
    } else {
      document.getElementById('message').innerText = 'Invalid verification code.';
    }
  });
}
