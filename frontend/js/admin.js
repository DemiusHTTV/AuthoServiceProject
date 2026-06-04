/**
 * admin.js — логика админ-панели: заявки, работники, склад, статистика
 */
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
    }
}

$('#adminLoginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    localStorage.setItem('admin_auth', 'true');
    checkAuth();
});

$('#adminLogout').addEventListener('click', () => {
    localStorage.removeItem('admin_auth');
    window.location.href = '/';
});

$$('.nav-item[data-section]').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const section = item.dataset.section;
        $$('.nav-item').forEach(n => n.classList.remove('active'));
        item.classList.add('active');
        $$('.content-section').forEach(s => s.classList.remove('active'));
        $(`#sec-${section}`).classList.add('active');
    });
});

$('#hamburger').addEventListener('click', () => {
    $('#hamburger').classList.toggle('open');
    $('#sidebar').classList.toggle('open');
});

$('#closeRequestDetail').addEventListener('click', () => {
    $('#requestDetailModal').classList.remove('active');
});

$('#closeAssign').addEventListener('click', () => {
    $('#assignModal').classList.remove('active');
});

$('#assignForm').addEventListener('submit', (e) => {
    e.preventDefault();
    $('#assignModal').classList.remove('active');
    alert('Работник назначен ✅');
});

$$('.modal').forEach(m => {
    m.addEventListener('click', e => {
        if (e.target === m && m.id !== 'adminLoginModal') m.classList.remove('active');
    });
});

document.addEventListener('DOMContentLoaded', checkAuth);