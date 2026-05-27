import { AUTO_API, api, getUser, setUser, logout } from './api.js';
import './style.css';

const $ = (s) => document.querySelector(s);
const user = getUser();
const authBlock = $('#authBlock'),
    profileBlock = $('#profileBlock'),
    profileName = $('#profileName');
if (user) {
    authBlock.classList.add('hidden');
    profileBlock.classList.remove('hidden');
    profileName.textContent = `${user.fullname} (${user.role})`;
}
$('#logoutBtn')?.addEventListener('click', logout);
$('#panelLink')?.addEventListener('click', () => {
    const u = getUser();
    if (!u) return openAuth('login');
    location.href =
        u.role === 'admin' ? '/admin.html' : u.role === 'worker' ? '/worker.html' : '/#cabinet';
});

function openAuth(tab = 'login') {
    $('#authModal').classList.add('active');
    switchTab(tab);
}
function closeAuth() {
    $('#authModal').classList.remove('active');
}
function switchTab(tab) {
    $('#loginForm').classList.toggle('hidden', tab !== 'login');
    $('#registerForm').classList.toggle('hidden', tab !== 'register');
    $('#tabLogin').classList.toggle('active', tab === 'login');
    $('#tabReg').classList.toggle('active', tab === 'register');
}
$('#openLogin').onclick = () => openAuth('login');
$('#openRegister').onclick = () => openAuth('register');
$('#closeAuth').onclick = closeAuth;
$('#tabLogin').onclick = () => switchTab('login');
$('#tabReg').onclick = () => switchTab('register');

$('#registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.target;
    try {
        await api(AUTO_API, '/register', 'POST', {
            fullname: f.fullname.value,
            phone: f.phone.value,
            email: f.email.value,
            password: f.password.value,
        });
        alert('Регистрация успешна, теперь войдите');
        switchTab('login');
        f.reset();
    } catch (err) {
        alert(err.message);
    }
});
$('#loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.target;
    try {
        const data = await api(AUTO_API, '/login', 'POST', {
            email: f.email.value,
            password: f.password.value,
        });
        setUser(data.user);
        if (data.user.role === 'admin') location.href = '/admin.html';
        else if (data.user.role === 'worker') location.href = '/worker.html';
        else location.reload();
    } catch (err) {
        alert(err.message);
    }
});

$('#openOrder').onclick = () => $('#orderModal').classList.add('active');
$('#closeOrder').onclick = () => $('#orderModal').classList.remove('active');
$('#orderForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.target;
    try {
        await api(AUTO_API, '/orders/public', 'POST', {
            fullname: f.fullname.value,
            phone: f.phone.value,
            brand: f.brand.value,
            model: f.model.value,
            service_name: f.service_name.value,
            description: f.description.value,
        });
        alert('Заявка создана! Администратор увидит её в панели.');
        f.reset();
        $('#orderModal').classList.remove('active');
    } catch (err) {
        alert(err.message);
    }
});

async function loadCabinet() {
    const u = getUser();
    if (!u || u.role !== 'client') return;
    try {
        const data = await api(AUTO_API, `/users/cabinet/${u.email}`);
        $('#cabinetContent').innerHTML =
            `<h3>Личный кабинет</h3><p><b>${data.fullname}</b></p><h4>Мои авто</h4>${data.cars.length ? data.cars.map((c) => `<div class="card">${c.brand} ${c.model}, VIN: ${c.vin}</div>`).join('') : '<p class="muted">Пока нет авто</p>'}<h4>Мои заявки</h4>${data.orders.length ? data.orders.map((o) => `<div class="card">#${o.id} ${o.car}: ${o.service_name}<br><span class="badge">${o.status}</span></div>`).join('') : '<p class="muted">Пока нет заявок</p>'}`;
    } catch (e) {
        $('#cabinetContent').innerHTML = '<p>Не удалось загрузить кабинет</p>';
    }
}
loadCabinet();
