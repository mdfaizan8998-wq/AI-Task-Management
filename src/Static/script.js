const API_BASE_URL = "https://ai-task-management-production.up.railway.app";

function switchCard(cardId) {
    document.querySelectorAll('.auth-card, .dashboard-card').forEach(card => card.classList.add('hidden'));
    document.getElementById(cardId).classList.remove('hidden');
}

// 🎯 Smart Error Formatter Helper to destroy [object Object] forever
function formatBackendError(data, defaultMsg = "Action failed") {
    if (!data) return defaultMsg;
    if (typeof data.detail === 'string') return data.detail;
    if (Array.isArray(data.detail)) return data.detail.map(err => err.msg).join(", ");
    if (data.detail && typeof data.detail === 'object') return JSON.stringify(data.detail);
    return defaultMsg;
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');

    // Check if accidently an object is passed straight to toast
    if (typeof message === 'object') {
        toast.textContent = formatBackendError(message, "An unexpected error occurred");
    } else {
        toast.textContent = message;
    }

    toast.style.background = type === 'success' ? '#10b981' : '#ef4444';
    toast.className = "toast show";
    setTimeout(() => { toast.className = "toast"; }, 3500);
}

// ---------------- AUTH CONTROLLERS ----------------
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('reg-name').value,
        username: document.getElementById('reg-username').value,
        email: document.getElementById('reg-email').value,
        password: document.getElementById('reg-password').value
    };
    try {
        const res = await fetch(`${API_BASE_URL}/auth/registration`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const d = await res.json();
        if (res.ok) {
            showToast("OTP sent to your email!");
            document.getElementById('verify-email').value = payload.email;
            switchCard('verify-card');
        } else {
            showToast(formatBackendError(d, "Registration failed"), "error");
        }
    } catch (error) {
        showToast(error.message || "Server connection failed", "error");
    }
});

document.getElementById('verify-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = { email: document.getElementById('verify-email').value, otp: document.getElementById('verify-otp').value };
    try {
        const res = await fetch(`${API_BASE_URL}/auth/verify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const d = await res.json();
        if (res.ok) {
            showToast("Account Verified! Please login.");
            switchCard('login-card');
        } else {
            showToast(formatBackendError(d, "Verification failed"), "error");
        }
    } catch (error) {
        showToast(error.message || "Verification connection failed", "error");
    }
});

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = { email: document.getElementById('login-email').value, password: document.getElementById('login-password').value };
    try {
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem('auth_token', data.token);
            showToast("Logged in successfully!");
            checkAuthAndLoadDashboard();
        } else {
            showToast(formatBackendError(data, "Login failed"), "error");
        }
    } catch (error) {
        showToast(error.message || "Login server offline", "error");
    }
});

// ---------------- TASKS CRUD WORKFLOW ----------------

// 1. READ: Fetch All Tasks & Integration of single one_task via clean endpoint
async function loadUserTasks() {
    const token = localStorage.getItem('auth_token');
    try {
        const res = await fetch(`${API_BASE_URL}/all_task`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const tasks = await res.json();
        const container = document.getElementById('tasks-container');
        container.innerHTML = '';

        if (!res.ok || tasks.length === 0 || tasks.detail) {
            container.innerHTML = `<p class="empty-state">No tasks available. Add some tasks above!</p>`;
            if (!res.ok && tasks.detail) {
                showToast(formatBackendError(tasks, "Failed to load tasks"), "error");
            }
            return;
        }

        tasks.forEach(task => {
            const card = document.createElement('div');
            card.className = 'task-item-card';
            card.innerHTML = `
                <div class="task-meta">
                    <h4>${task.title}</h4>
                    <p>${task.description || 'No description provided'}</p>
                    <div class="tags-row">
                        <span class="tag ${task.priority}">${task.priority}</span>
                        <span class="tag status-badge">${task.status}</span>
                        ${task.due_date ? `<span class="tag date-badge"><i class="fa-regular fa-calendar"></i> ${task.due_date}</span>` : ''}
                    </div>
                </div>
                <div class="task-actions">
                    <button class="btn-icon edit" onclick="setupEditTask(${task.id})"><i class="fa-solid fa-pen"></i></button>
                    <button class="btn-icon delete" onclick="deleteTask(${task.id})"><i class="fa-solid fa-trash"></i></button>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        document.getElementById('tasks-container').innerHTML = `<p class="empty-state">Error fetching tasks</p>`;
        showToast(error.message || "Error fetching tasks", "error");
    }
}

// 2. CREATE & UPDATE SUBMIT HANDLER
document.getElementById('task-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('auth_token');
    const taskId = document.getElementById('task-id-edit').value;

    const payload = {
        title: document.getElementById('task-title').value,
        description: document.getElementById('task-desc').value,
        priority: document.getElementById('task-priority').value,
        status: document.getElementById('task-status').value,
        due_date: document.getElementById('task-date').value || null
    };

    let url = `${API_BASE_URL}/create`;
    let method = 'POST';

    if (taskId) {
        url = `${API_BASE_URL}/update/${taskId}`;
        method = 'PUT';
    }

    try {
        const res = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        const d = await res.json();

        if (res.ok) {
            showToast(taskId ? "Task updated successfully!" : "Task created successfully!");
            resetTaskForm();
            loadUserTasks();
        } else {
            showToast(formatBackendError(d, "Action failed"), "error");
        }
    } catch (error) {
        showToast(error.message || "Network operation error", "error");
    }
});

// 3. DELETE TASK ROUTE
async function deleteTask(id) {
    if (!confirm("Are you sure you want to delete this task?")) return;
    const token = localStorage.getItem('auth_token');
    try {
        const res = await fetch(`${API_BASE_URL}/delete/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            showToast("Task deleted successfully");
            loadUserTasks();
        } else {
            const d = await res.json();
            showToast(formatBackendError(d, "Failed to delete task"), "error");
        }
    } catch (error) {
        showToast(error.message || "Delete request failed", "error");
    }
}

// 4. EDIT POPULATION TRIGGER (Using Clean 'one_task' Backend Endpoint Fetch)
async function setupEditTask(id) {
    const token = localStorage.getItem('auth_token');
    try {
        const res = await fetch(`${API_BASE_URL}/one_task/${id}`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const task = await res.json();

        if (res.ok) {
            document.getElementById('task-id-edit').value = task.id;
            document.getElementById('task-title').value = task.title;
            document.getElementById('task-desc').value = task.description || '';
            document.getElementById('task-priority').value = task.priority;
            document.getElementById('task-status').value = task.status;
            document.getElementById('task-date').value = task.due_date || '';

            document.getElementById('task-submit-btn').textContent = "Update Task";
            document.getElementById('cancel-edit-btn').classList.remove('hidden');
        } else {
            showToast(formatBackendError(task, "Failed to fetch task details"), "error");
        }
    } catch (error) {
        showToast(error.message || "Failed to connect to single task endpoint", "error");
    }
}

function resetTaskForm() {
    document.getElementById('task-id-edit').value = '';
    document.getElementById('task-form').reset();
    document.getElementById('task-submit-btn').textContent = "Add Task";
    document.getElementById('cancel-edit-btn').classList.add('hidden');
}

// Helper utilities
function escapeHTML(str) {
    return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

async function checkAuthAndLoadDashboard() {
    const token = localStorage.getItem('auth_token');
    if (!token) { switchCard('login-card'); return; }
    try {
        const res = await fetch(
            `${API_BASE_URL}/auth/is_auth`,
            {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        const userData = await res.json();
        if (res.ok) {
            document.getElementById('user-display-name').textContent = userData.name || userData.username;
            switchCard('dashboard-card');
            loadUserTasks();
        } else {
            localStorage.removeItem('auth_token');
            switchCard('login-card');
            showToast(formatBackendError(userData, "Session expired"), "error");
        }
    } catch (error) {
        switchCard('login-card');
        showToast(error.message || "Auth verify network error", "error");
    }
}

document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('auth_token');
    switchCard('login-card');
    showToast("Logged out successfully");
});

window.addEventListener('DOMContentLoaded', checkAuthAndLoadDashboard);








document.addEventListener("DOMContentLoaded", () => {
    const askAiBtn = document.getElementById("ask-ai-btn");
    const taskTitleInput = document.getElementById("task-title");
    const taskDescInput = document.getElementById("task-desc");
    const aiTagWrapper = document.getElementById("ai-tag-wrapper");
    const taskTagPreview = document.getElementById("task-tag-preview");

    askAiBtn.addEventListener("click", async () => {
        const titleValue = taskTitleInput.value.trim();

        if (!titleValue) {
            alert("Bhai, pehle 'Task Title' likho tabhi toh AI suggest karega! 😅");
            taskTitleInput.focus();
            return;
        }

        // Loader State
        askAiBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Thinking...`;
        askAiBtn.disabled = true;

        // Purana preview reset/hide karne ke liye animation class hatana
        aiTagWrapper.classList.remove("show-ai");
        aiTagWrapper.style.display = "none";

        try {
            const response = await fetch(`${API_BASE_URL}/suggest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: titleValue })
});
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Automation failed.");
            }

            const data = await response.json();

            // 1. Data Inject karna
            taskDescInput.value = data.description;
            taskTagPreview.textContent = data.tag;

            // 2. Tag Wrapper ko block karke micro-task lagakar animation class trigger karna
            aiTagWrapper.style.display = "inline-block";
            setTimeout(() => {
                aiTagWrapper.classList.add("show-ai");
            }, 50);

            // 3. Textarea par stylish border glow trigger karna
            taskDescInput.classList.add("ai-glow-active");
            setTimeout(() => {
                taskDescInput.classList.remove("ai-glow-active");
            }, 1500); // 1.5s ke baad glow smooth fade out ho jayega

        } catch (error) {
            console.error(error);
            alert(`Error: ${error.message}`);
        } finally {
            askAiBtn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Ask AI`;
            askAiBtn.disabled = false;
        }
    });
});
taskSubmitBtn.addEventListener("click", async (e) => {
        e.preventDefault(); // Form ko automatic reload hone se rokne ke liye

        const title = taskTitleInput.value.trim();
        const description = taskDescInput.value.trim();
        
        // AI Tag ko extract karna (agar text khaali hai toh null ya empty string bhejenge)
        const tag = taskTagPreview.textContent.trim(); 

        if (!title) {
            alert("Bhai, Task Title likhna zaroori hai! 📝");
            taskTitleInput.focus();
            return;
        }
