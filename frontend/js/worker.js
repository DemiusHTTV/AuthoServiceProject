/**
 * worker.js — логика панели работника: задачи, смена статусов
 */

const API = '';

function $(sel) { return document.querySelector(sel); }
function $$(sel) { return document.querySelectorAll(sel); }

// ============ Авторизация ============
function getWorker() {
    const raw = localStorage.getItem('worker');
    return raw ? JSON.parse(raw) : null;
}

function checkAuth() {
    const worker = getWorker();
    if (!worker) {
        $('#workerLoginModal').classList.add('active');
    } else {
        $('#workerLoginModal').classList.remove('active');
        $('#workerInfo').textContent = `${worker.name} (${worker.specialization || ''})`;
        loadTasks();
    }
}

$('#workerLoginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
        const resp = await fetch(API + '/api/workers/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login: fd.get('login'), password: fd.get('password') })
        });
        if (!resp.ok) {
            alert('Неверный логин или пароль');
            return;
        }
        const worker = await resp.json();
        localStorage.setItem('worker', JSON.stringify(worker));
        checkAuth();
    } catch (err) {
        alert('Ошибка сети');
    }
});

$('#workerLogout').addEventListener('click', () => {
    localStorage.removeItem('worker');
    window.location.href = '/';
});

// ============ Задачи ============
let allTasks = [];
let currentFilter = 'all';

async function loadTasks() {
    const worker = getWorker();
    if (!worker) return;
    try {
        const resp = await fetch(API + `/api/workers/${worker.id}/tasks`);
        allTasks = await resp.json();
        renderTasks(currentFilter);
    } catch (e) { console.error(e); }
}

function renderTasks(filter) {
    currentFilter = filter;
    const filtered = filter === 'all' ? allTasks : allTasks.filter(t => t.task_status === filter);
    const cont = $('#tasksList');

    const statusLabels = {
        'not_started': { text: 'Не начато', color: '#fff3cd', textColor: '#856404' },
        'in_progress': { text: 'В работе', color: '#ffe0b2', textColor: '#e65100' },
        'done': { text: 'Выполнено', color: '#e8f5e9', textColor: '#2e7d32' }
    };

    if (filtered.length === 0) {
        cont.innerHTML = '<div class="card"><p>Нет задач</p></div>';
        return;
    }

    cont.innerHTML = filtered.map(t => {
        const sl = statusLabels[t.task_status] || { text: t.task_status, color: '#eee', textColor: '#333' };
        return `
        <div class="card" style="margin-bottom:15px">
            <div style="display:flex;justify-content:space-between;align-items:start;flex-wrap:wrap;gap:10px">
                <div>
                    <h3 style="margin-bottom:5px">${t.car_brand} ${t.car_model} ${t.car_year || ''}</h3>
                    <p><strong>Клиент:</strong> ${t.client_name}</p>
                    <p><strong>Услуга:</strong> ${t.service_name || '—'}</p>
                    <p><strong>Описание:</strong> ${t.description || '—'}</p>
                    <p style="margin-top:8px">
                        <span style="display:inline-block;padding:4px 10px;border-radius:4px;font-weight:bold;font-size:0.85rem;background:${sl.color};color:${sl.textColor}">${sl.text}</span>
                    </p>
                    <p class="muted" style="font-size:0.8rem;margin-top:5px">Назначено: ${t.assigned_at || ''}</p>
                    ${t.completed_at ? `<p class="muted" style="font-size:0.8rem">Завершено: ${t.completed_at}</p>` : ''}
                </div>
                <div style="display:flex;flex-direction:column;gap:6px">
                    ${t.task_status === 'not_started' ? `
                        <button class="btn btn-primary" style="padding:6px 14px;font-size:0.85rem" onclick="changeStatus(${t.assignment_id}, 'in_progress')">▶ Начать</button>
                    ` : ''}
                    ${t.task_status === 'in_progress' ? `
                        <button class="btn btn-primary" style="padding:6px 14px;font-size:0.85rem;background:#2e7d32" onclick="changeStatus(${t.assignment_id}, 'done')">✓ Выполнено</button>
                        <button class="btn btn-light" style="padding:6px 14px;font-size:0.85rem" onclick="changeStatus(${t.assignment_id}, 'not_started')">⏸ Пауза</button>
                    ` : ''}
                </div>
            </div>
        </div>
        `;
    }).join('');
}

// Смена статуса
window.changeStatus = async function(assignmentId, newStatus) {
    try {
        const resp = await fetch(API + `/api/workers/tasks/${assignmentId}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        if (resp.ok) {
            loadTasks();
        } else {
            alert('Ошибка обновления статуса');
        }
    } catch (e) {
        alert('Ошибка сети');
    }
};

// Фильтры
$$('[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
        renderTasks(btn.dataset.filter);
    });
});

// ============ Init ============
document.addEventListener('DOMContentLoaded', checkAuth);
