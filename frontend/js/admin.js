/**
 * admin.js — логика админ-панели: заявки, работники, склад, статистика
 */

const API = '';

function $(sel) { return document.querySelector(sel); }
function $$(sel) { return document.querySelectorAll(sel); }

function getAdmin() {
    return localStorage.getItem('admin_auth') === 'true';
}

function checkAuth() {
    if (!getAdmin()) {
        $('#adminLoginModal').classList.add('active');
        $('#mainContent').style.opacity = '0.3';
        $('#mainContent').style.pointerEvents = 'none';
    } else {
        $('#adminLoginModal').classList.remove('active');
        $('#mainContent').style.opacity = '1';
        $('#mainContent').style.pointerEvents = 'auto';
        loadRequests();
        loadWorkers();
    }
}

// ============ Логин ============
$('#adminLoginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
        const resp = await fetch(API + '/api/admin/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login: fd.get('login'), password: fd.get('password') })
        });
        if (!resp.ok) {
            alert('Неверный логин или пароль');
            return;
        }
        localStorage.setItem('admin_auth', 'true');
        checkAuth();
    } catch (err) {
        alert('Ошибка сети');
    }
});

$('#adminLogout').addEventListener('click', () => {
    localStorage.removeItem('admin_auth');
    window.location.href = '/';
});

// ============ Навигация по секциям ============
$$('.nav-item[data-section]').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const section = item.dataset.section;
        $$('.nav-item').forEach(n => n.classList.remove('active'));
        item.classList.add('active');
        $$('.content-section').forEach(s => s.classList.remove('active'));
        $(`#sec-${section}`).classList.add('active');

        if (section === 'warehouse') loadWarehouse();
        if (section === 'stats') loadStats();
    });
});

// ============ Гамбургер (мобильный) ============
$('#hamburger').addEventListener('click', () => {
    $('#hamburger').classList.toggle('open');
    $('#sidebar').classList.toggle('open');
});


let allRequests = [];
let allWorkers = [];

async function loadRequests() {
    try {
        const resp = await fetch(API + '/api/admin/requests');
        allRequests = await resp.json();
        renderRequests('all');
    } catch (e) { console.error(e); }
}

function renderRequests(filter) {
    const tbody = $('#requestsTable tbody');
    const filtered = filter === 'all' ? allRequests : allRequests.filter(r => r.status === filter);

    const statusLabels = {
        'new': '<span class="badge" style="background:#fff3cd;color:#856404">Новая</span>',
        'accepted': '<span class="badge" style="background:#d1ecf1;color:#0c5460">Принята</span>',
        'in_progress': '<span class="badge" style="background:#ffe0b2;color:#e65100">В работе</span>',
        'completed': '<span class="badge green">Завершена</span>',
        'rejected': '<span class="badge" style="background:#ffebee;color:#c62828">Отклонена</span>'
    };

    tbody.innerHTML = filtered.map(r => `
        <tr>
            <td>${r.id}</td>
            <td>${r.client_name}</td>
            <td>${r.car_brand} ${r.car_model}</td>
            <td>${r.service_name || '—'}</td>
            <td>${statusLabels[r.status] || r.status}</td>
            <td>${r.created_at || ''}</td>
            <td>
                <button class="btn btn-light" style="padding:5px 10px;font-size:0.8rem" onclick="viewRequest(${r.id})">👁</button>
                ${r.status === 'new' ? `
                    <button class="btn btn-primary" style="padding:5px 10px;font-size:0.8rem" onclick="acceptRequest(${r.id})">✓</button>
                    <button class="btn btn-danger" style="padding:5px 10px;font-size:0.8rem" onclick="rejectRequest(${r.id})">✗</button>
                ` : ''}
                ${(r.status === 'accepted' || r.status === 'in_progress') ? `
                    <button class="btn btn-light" style="padding:5px 10px;font-size:0.8rem" onclick="openAssign(${r.id})">+👷</button>
                ` : ''}
            </td>
        </tr>
    `).join('');
}

// Фильтры заявок
$$('[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
        if (btn.closest('#sec-requests')) {
            renderRequests(btn.dataset.filter);
        }
    });
});

// Просмотр заявки
window.viewRequest = async function(id) {
    try {
        const resp = await fetch(API + `/api/requests/${id}`);
        const r = await resp.json();
        const cont = $('#requestDetailContent');
        cont.innerHTML = `
            <p><strong>Клиент:</strong> ${r.client_name}</p>
            <p><strong>Email:</strong> ${r.client_email || '—'}</p>
            <p><strong>Телефон:</strong> ${r.client_phone || '—'}</p>
            <p><strong>Авто:</strong> ${r.car_brand} ${r.car_model} ${r.car_year || ''}</p>
            <p><strong>Услуга:</strong> ${r.service_name || '—'} ${r.base_price ? '(' + r.base_price + ' ₽)' : ''}</p>
            <p><strong>Описание:</strong> ${r.description || '—'}</p>
            <p><strong>Статус:</strong> ${r.status}</p>
            <p><strong>Создана:</strong> ${r.created_at}</p>
            ${r.assignments && r.assignments.length > 0 ? `
                <h3 style="margin-top:15px">Назначенные работники:</h3>
                ${r.assignments.map(a => `
                    <div style="background:#f5f5f5;padding:8px;border-radius:4px;margin-top:6px">
                        <strong>${a.worker_name}</strong> (${a.specialization || '—'}) — ${a.status}
                    </div>
                `).join('')}
            ` : ''}
        `;
        $('#requestDetailModal').classList.add('active');
    } catch (e) { console.error(e); }
};

$('#closeRequestDetail').addEventListener('click', () => {
    $('#requestDetailModal').classList.remove('active');
});

// Принять/отклонить
window.acceptRequest = async function(id) {
    await fetch(API + `/api/admin/requests/${id}/accept`, { method: 'PUT' });
    loadRequests();
};

window.rejectRequest = async function(id) {
    if (!confirm('Отклонить заявку?')) return;
    await fetch(API + `/api/admin/requests/${id}/reject`, { method: 'PUT' });
    loadRequests();
};

// ============ Назначение работника ============
window.openAssign = function(requestId) {
    $('#assignRequestId').value = requestId;
    const sel = $('#assignWorkerSelect');
    sel.innerHTML = '<option value="">Выберите работника</option>' +
        allWorkers.map(w => `<option value="${w.id}">${w.name} (${w.specialization || '—'})</option>`).join('');
    $('#assignModal').classList.add('active');
};

$('#closeAssign').addEventListener('click', () => {
    $('#assignModal').classList.remove('active');
});

$('#assignForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const requestId = parseInt($('#assignRequestId').value);
    const workerId = parseInt($('#assignWorkerSelect').value);
    if (!workerId) return;

    try {
        const resp = await fetch(API + '/api/admin/assign', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ request_id: requestId, worker_id: workerId })
        });
        if (resp.ok) {
            $('#assignModal').classList.remove('active');
            loadRequests();
            alert('Работник назначен ✅');
        } else {
            const err = await resp.json();
            alert(err.detail || 'Ошибка');
        }
    } catch (e) {
        alert('Ошибка сети');
    }
});

// ============ Работники ============
async function loadWorkers() {
    try {
        const resp = await fetch(API + '/api/admin/workers');
        allWorkers = await resp.json();
        const tbody = $('#workersTable tbody');
        tbody.innerHTML = allWorkers.map(w => `
            <tr>
                <td>${w.id}</td>
                <td>${w.name}</td>
                <td>${w.specialization || '—'}</td>
                <td>${w.phone}</td>
                <td>${w.login}</td>
            </tr>
        `).join('');
    } catch (e) { console.error(e); }
}

// ============ Склад ============
async function loadWarehouse(query) {
    try {
        const url = query
            ? API + `/api/warehouse/parts/search/${encodeURIComponent(query)}`
            : API + '/api/warehouse/parts';
        const resp = await fetch(url);
        const parts = await resp.json();
        const tbody = $('#warehouseTable tbody');
        tbody.innerHTML = parts.map(p => `
            <tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.article}</td>
                <td>${p.price}</td>
                <td><span class="badge ${p.quantity < 10 ? 'red' : 'green'}">${p.quantity}</span></td>
                <td>${p.category}</td>
            </tr>
        `).join('');
    } catch (e) {
        $('#warehouseTable tbody').innerHTML = '<tr><td colspan="6">Склад недоступен</td></tr>';
    }
}

$('#warehouseSearch').addEventListener('input', (e) => {
    const q = e.target.value.trim();
    loadWarehouse(q || null);
});

// ============ Статистика ============
async function loadStats() {
    try {
        const resp = await fetch(API + '/api/admin/stats');
        const s = await resp.json();
        const cont = $('#statsCards');
        cont.innerHTML = `
            <div class="stat-box"><h3>${s.total_requests}</h3><p>Всего заявок</p></div>
            <div class="stat-box"><h3>${s.new_requests}</h3><p>Новых</p></div>
            <div class="stat-box"><h3>${s.in_progress}</h3><p>В работе</p></div>
            <div class="stat-box"><h3>${s.completed}</h3><p>Завершено</p></div>
            <div class="stat-box"><h3>${s.workers_count}</h3><p>Работников</p></div>
        `;
    } catch (e) { console.error(e); }
}

// Закрытие модалок по фону
$$('.modal').forEach(m => {
    m.addEventListener('click', e => {
        if (e.target === m && m.id !== 'adminLoginModal') m.classList.remove('active');
    });
});

// ============ Init ============
document.addEventListener('DOMContentLoaded', checkAuth);
