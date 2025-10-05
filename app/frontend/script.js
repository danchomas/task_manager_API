let authToken = null;

// DOM
const authScreen = document.getElementById('auth-screen');
const tasksScreen = document.getElementById('tasks-screen');
const notification = document.getElementById('notification');

// Auth
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form-inner');
const showRegister = document.getElementById('show-register');
const showLogin = document.getElementById('show-login');
const registerCard = document.getElementById('register-form');

// Tasks
const tasksList = document.getElementById('tasks-list');
const addTaskBtn = document.getElementById('add-task-btn');
const taskModal = document.getElementById('task-modal');
const taskForm = document.getElementById('task-form');
const modalTitle = document.getElementById('modal-title');
const closeBtn = document.querySelector('.close');
const logoutBtn = document.getElementById('logout-btn');

// Notification
function showNotification(message, isError = false) {
  notification.textContent = message;
  notification.style.backgroundColor = isError ? '#e74c3c' : '#27ae60';
  notification.style.display = 'block';
  setTimeout(() => {
    notification.style.display = 'none';
  }, 3000);
}

// Token management
function setAuthToken(token) {
  authToken = token;
  localStorage.setItem('authToken', token);
}

function getAuthToken() {
  if (!authToken) {
    authToken = localStorage.getItem('authToken');
  }
  return authToken;
}

function clearAuth() {
  authToken = null;
  localStorage.removeItem('authToken');
}

// API request
async function apiRequest(url, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };

  const token = getAuthToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers
  };

  try {
    const response = await fetch(url, config);
    if (!response.ok) {
      let message = `Ошибка ${response.status}`;
      try {
        const error = await response.json();
        if (Array.isArray(error.detail)) {
          message = error.detail.map(err => err.msg).join('; ');
        } else if (typeof error.detail === 'string') {
          message = error.detail;
        }
      } catch (e) {
        // fallback to status text
      }
      throw new Error(message);
    }
    return await response.json();
  } catch (error) {
    showNotification(error.message || 'Ошибка сети', true);
    throw error;
  }
}

// Screens
function showAuthScreen() {
  authScreen.style.display = 'block';
  tasksScreen.style.display = 'none';
}

function showTasksScreen() {
  authScreen.style.display = 'none';
  tasksScreen.style.display = 'block';
}

// Auth
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  try {
    const data = await apiRequest('/users/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    // FastAPI возвращает { access_token: "...", token_type: "bearer" }
    setAuthToken(data.access_token); // ← только JWT!
    await loadTasks();
    showTasksScreen();
  } catch (err) {
    // Ошибка уже показана
  }
});

registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('reg-username').value;
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;

  try {
    await apiRequest('/users/create_user', {
      method: 'POST',
      body: JSON.stringify({ username, email, password })
    });
    showNotification('Регистрация успешна! Войдите в систему.');
    registerCard.style.display = 'none';
  } catch (err) {
    // Ошибка уже показана
  }
});

showRegister.addEventListener('click', (e) => {
  e.preventDefault();
  registerCard.style.display = 'block';
});

showLogin.addEventListener('click', (e) => {
  e.preventDefault();
  registerCard.style.display = 'none';
});

// Tasks
async function loadTasks() {
  try {
    const tasks = await apiRequest('/tasks/my_tasks', { method: 'POST' });
    renderTasks(tasks);
  } catch (err) {
    if (err.message.includes('401') || err.message.includes('Invalid token')) {
      showNotification('Сессия истекла. Войдите снова.', true);
      clearAuth();
      showAuthScreen();
    }
  }
}

function renderTasks(tasks) {
  tasksList.innerHTML = '';
  if (tasks.length === 0) {
    tasksList.innerHTML = '<p>У вас пока нет задач.</p>';
    return;
  }

  tasks.forEach(task => {
    const statusClass = `status-${task.status}`;
    const desc = task.description || '';
    const taskEl = document.createElement('div');
    taskEl.className = 'task-item';
    taskEl.innerHTML = `
      <div class="task-info">
        <h3>${escapeHtml(task.name)}</h3>
        <p>${escapeHtml(desc)}</p>
        <span class="task-status ${statusClass}">${task.status}</span>
      </div>
      <div class="task-actions">
        <button onclick="editTask('${task.id}', '${escapeJs(task.name)}', '${escapeJs(desc)}', '${task.status}')">✏️</button>
        <button onclick="deleteTask('${task.id}')">🗑️</button>
      </div>
    `;
    tasksList.appendChild(taskEl);
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function escapeJs(str) {
  return str.replace(/['\\]/g, '\\$&');
}

function openTaskModal(id = null, name = '', desc = '', status = 'created') {
  document.getElementById('task-id').value = id || '';
  document.getElementById('task-name').value = name;
  document.getElementById('task-description').value = desc;
  document.getElementById('task-status').value = status;
  modalTitle.textContent = id ? 'Редактировать задачу' : 'Новая задача';
  taskModal.style.display = 'flex';
}

function closeTaskModal() {
  taskModal.style.display = 'none';
  taskForm.reset();
  document.getElementById('task-id').value = '';
}

addTaskBtn.addEventListener('click', () => openTaskModal());
closeBtn.addEventListener('click', closeTaskModal);
taskModal.addEventListener('click', (e) => {
  if (e.target === taskModal) closeTaskModal();
});

taskForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('task-id').value;
  const name = document.getElementById('task-name').value;
  const description = document.getElementById('task-description').value;
  const status = document.getElementById('task-status').value;

  try {
    if (id) {
      await apiRequest('/tasks/update_task', {
        method: 'POST',
        body: JSON.stringify({ id, name, description, status })
      });
      showNotification('Задача обновлена!');
    } else {
      await apiRequest('/tasks/create_task', {
        method: 'POST',
        body: JSON.stringify({ name, description, status })
      });
      showNotification('Задача создана!');
    }
    await loadTasks();
    closeTaskModal();
  } catch (err) {
    // Ошибка уже показана
  }
});

// Global functions for inline onclick
window.editTask = (id, name, desc, status) => {
  openTaskModal(id, name, desc, status);
};

window.deleteTask = async (id) => {
  if (!confirm('Удалить задачу?')) return;
  try {
    await apiRequest(`/tasks/${id}`, { method: 'DELETE' });
    showNotification('Задача удалена!');
    await loadTasks();
  } catch (err) {
    // Ошибка уже показана
  }
};

logoutBtn.addEventListener('click', () => {
  clearAuth();
  showAuthScreen();
});

// Init
document.addEventListener('DOMContentLoaded', () => {
  const token = getAuthToken();
  if (token) {
    loadTasks().then(() => showTasksScreen()).catch(() => showAuthScreen());
  } else {
    showAuthScreen();
  }
});