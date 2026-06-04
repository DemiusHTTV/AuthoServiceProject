/**
 * worker.js — логика панели работника: задачи, смена статусов
 */
function $(sel) { return document.querySelector(sel); }
function $$(sel) { return document.querySelectorAll(sel); }

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
    }
}

$('#workerLoginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const mockWorker = { name: 'Мастер', specialization: 'Автомеханик' };
    localStorage.setItem('worker', JSON.stringify(mockWorker));
    checkAuth();
});

$('#workerLogout').addEventListener('click', () => {
    localStorage.removeItem('worker');
    window.location.href = '/';
});

$$('.modal').forEach(m => {
    m.addEventListener('click', e => {
        if (e.target === m && m.id !== 'workerLoginModal') m.classList.remove('active');
    });
});

document.addEventListener('DOMContentLoaded', checkAuth);