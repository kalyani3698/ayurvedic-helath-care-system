async function checkAuth(callback) {
  try {
    const res = await fetch('/api/auth/me');
    const user = res.ok ? await res.json() : null;
    updateNavAuth(user);
    if (callback) callback(user);
  } catch { updateNavAuth(null); if (callback) callback(null); }
}

function requireAuth(callback) {
  checkAuth(user => {
    if (!user) { window.location.href = '/login'; return; }
    if (callback) callback(user);
  });
}

function updateNavAuth(user) {
  const el = document.getElementById('authNav');
  if (!el) return;
  if (user) {
    el.innerHTML = `<a href="/dashboard" class="nav-link">Dashboard</a><a href="/dosha-quiz" class="nav-link">Dosha Quiz</a><a href="/symptom-analyzer" class="nav-link">Symptoms</a><a href="/chat" class="nav-link">AI Guide</a><button onclick="logout()" class="btn btn-outline nav-btn">Logout</button>`;
  } else {
    el.innerHTML = `<a href="/login" class="btn btn-outline nav-btn">Log in</a><a href="/register" class="btn btn-primary nav-btn">Get Started</a>`;
  }
}

async function logout() {
  await fetch('/api/auth/logout', {method: 'POST'});
  window.location.href = '/';
}

function toggleMenu() {
  document.getElementById('navLinks').classList.toggle('open');
}

document.addEventListener('DOMContentLoaded', () => { checkAuth(() => {}); });
