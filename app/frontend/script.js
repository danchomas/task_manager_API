// frontend/script.js
// Базовый URL API (относительный путь)
const API_BASE = "/tasks";

// Получение задач
async function loadTasks() {
  try {
    const response = await fetch(`${API_BASE}/`);
    const tasks = await response.json();

    const container = document.getElementById("tasks-container");
    const countElement = document.getElementById("task-count");

    countElement.textContent = `${tasks.length} ${getTaskWordForm(tasks.length)}`;

    if (tasks.length === 0) {
      container.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-inbox fs-1 text-muted"></i>
                    <p class="mt-2 text-muted">Задачи не найдены. Создайте первую задачу!</p>
                </div>
            `;
      return;
    }

    container.innerHTML = tasks
      .map(
        (task) => `
            <div class="card task-card mb-3 fade-in">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h5 class="card-title">${escapeHtml(task.name)}</h5>
                            ${task.description ? `<p class="card-text task-description text-muted">${escapeHtml(task.description)}</p>` : ""}
                        </div>
                        <span class="status-badge status-${task.status}">
                            ${getStatusText(task.status)}
                        </span>
                    </div>
                    <div class="task-actions mt-3">
                        <button class="btn btn-sm btn-outline-primary" onclick="editTask('${task.id}')">
                            <i class="bi bi-pencil"></i> Редактировать
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteTask('${task.id}')">
                            <i class="bi bi-trash"></i> Удалить
                        </button>
                    </div>
                </div>
            </div>
        `,
      )
      .join("");
  } catch (error) {
    console.error("Ошибка загрузки задач:", error);
    alert("Не удалось загрузить задачи");
  }
}

// Создание задачи
document.getElementById("task-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("task-name").value;
  const description = document.getElementById("task-description").value;
  const status = document.getElementById("task-status").value;

  try {
    const response = await fetch(`${API_BASE}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, description, status }),
    });

    if (response.ok) {
      document.getElementById("task-form").reset();
      loadTasks();
      showNotification("Задача успешно создана!", "success");
    } else {
      throw new Error("Ошибка создания задачи");
    }
  } catch (error) {
    console.error("Ошибка создания задачи:", error);
    alert("Не удалось создать задачу");
  }
});

// Редактирование задачи
async function editTask(taskId) {
  try {
    const response = await fetch(`${API_BASE}/${taskId}`);
    const task = await response.json();

    document.getElementById("edit-task-id").value = task.id;
    document.getElementById("edit-task-name").value = task.name;
    document.getElementById("edit-task-description").value =
      task.description || "";
    document.getElementById("edit-task-status").value = task.status;

    const modal = new bootstrap.Modal(document.getElementById("editModal"));
    modal.show();
  } catch (error) {
    console.error("Ошибка загрузки задачи:", error);
    alert("Не удалось загрузить задачу для редактирования");
  }
}

// Сохранение изменений
document.getElementById("save-edit").addEventListener("click", async () => {
  const taskId = document.getElementById("edit-task-id").value;
  const name = document.getElementById("edit-task-name").value;
  const description = document.getElementById("edit-task-description").value;
  const status = document.getElementById("edit-task-status").value;

  try {
    const response = await fetch(`${API_BASE}/${taskId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, description, status }),
    });

    if (response.ok) {
      const modal = bootstrap.Modal.getInstance(
        document.getElementById("editModal"),
      );
      modal.hide();
      loadTasks();
      showNotification("Задача успешно обновлена!", "success");
    } else {
      throw new Error("Ошибка обновления задачи");
    }
  } catch (error) {
    console.error("Ошибка обновления задачи:", error);
    alert("Не удалось обновить задачу");
  }
});

// Удаление задачи
async function deleteTask(taskId) {
  if (!confirm("Вы уверены, что хотите удалить эту задачу?")) {
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/${taskId}`, {
      method: "DELETE",
    });

    if (response.ok) {
      loadTasks();
      showNotification("Задача успешно удалена!", "success");
    } else {
      throw new Error("Ошибка удаления задачи");
    }
  } catch (error) {
    console.error("Ошибка удаления задачи:", error);
    alert("Не удалось удалить задачу");
  }
}

// Вспомогательные функции
function getStatusText(status) {
  const statusMap = {
    created: "Создана",
    in_progress: "В процессе",
    completed: "Завершена",
  };
  return statusMap[status] || status;
}

function getTaskWordForm(count) {
  if (count % 10 === 1 && count % 100 !== 11) {
    return "задача";
  } else if (
    count % 10 >= 2 &&
    count % 10 <= 4 &&
    (count % 100 < 10 || count % 100 >= 20)
  ) {
    return "задачи";
  } else {
    return "задач";
  }
}

function escapeHtml(text) {
  const map = {
    "&": "&amp;",
    "<": "<",
    ">": ">",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

function showNotification(message, type = "info") {
  // Простая реализация уведомлений
  const alertClass = type === "success" ? "alert-success" : "alert-info";
  const notification = document.createElement("div");
  notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
  notification.style.cssText =
    "top: 20px; right: 20px; z-index: 1000; min-width: 300px;";
  notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
  document.body.appendChild(notification);

  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 3000);
}

// Инициализация
document.addEventListener("DOMContentLoaded", () => {
  loadTasks();
});
