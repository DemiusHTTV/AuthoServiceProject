/**
 * main.js — логика главной страницы: авторизация, заявки, ЛК (гамбургер-сайдбар)
 */

const API = '';  // same-origin
let servicesCache = [];

// ============ Утилиты ============
function $(sel) { return document.querySelector(sel); }
function $$(sel) { return document.querySelectorAll(sel); }

function getUser() {
    const raw = localStorage.getItem('user');
    return raw ? JSON.parse(raw) : null;
}

function setUser(u) {
    localStorage.setItem('user', JSON.stringify(u));
    updateUI();
}

function clearUser() {
    localStorage.removeItem('user');
    updateUI();
}

// ============ UI-состояние ============
function updateUI() {
    const user = getUser();
    if (user) {
        $('#authBlock').classList.add('hidden');
        $('#profileBlock').classList.remove('hidden');
        $('#profileName').textContent = user.name;
        // Показываем гамбургер ЛК
        $('#userHamburger').classList.remove('hidden');
        $('#sidebarUserName').textContent = user.name;
        $('#sidebarUserEmail').textContent = user.email;
        // Автозаполнение формы заявки
        $('#orderName').value = user.name || '';
        $('#orderName').readOnly = true;
        $('#orderEmail').value = user.email || '';
        $('#orderEmail').readOnly = true;
        $('#orderPhone').value = user.phone || '';
        $('#orderPhone').readOnly = true;
        refreshBonusPanel();
    } else {
        $('#authBlock').classList.remove('hidden');
        $('#profileBlock').classList.add('hidden');
        $('#userHamburger').classList.add('hidden');
        $('#userSidebar').classList.remove('open');
        $('#userHamburger').classList.remove('open');
        $('#orderName').value = '';
        $('#orderName').readOnly = false;
        $('#orderEmail').value = '';
        $('#orderEmail').readOnly = false;
        $('#orderPhone').value = '';
        $('#orderPhone').readOnly = false;
        $('#bonusPanel').classList.add('hidden');
        $('#bonusToSpend').value = '0';
        $('#bonusRange').value = '0';
    }
}

// ============ Загрузка услуг ============
async function loadServices() {
    try {
        const resp = await fetch(API + '/api/services');
        const services = await resp.json();
        servicesCache = services;

        // Карточки услуг
        const grid = $('#servicesGrid');
        grid.innerHTML = services.map(s => `
            <div class="card">
                <h3>${s.name}</h3>
                <p>${s.description}</p>
                <span class="price">от ${s.base_price} ₽</span>
            </div>
        `).join('');

        // Селект в форме заявки
        const sel = $('#orderServiceSelect');
        sel.innerHTML = '<option value="">Выберите услугу</option>' +
            services.map(s => `<option value="${s.id}">${s.name} — от ${s.base_price}₽</option>`).join('');
    } catch (e) {
        console.error('Ошибка загрузки услуг:', e);
    }
}

function getSelectedService() {
    const serviceId = parseInt($('#orderServiceSelect').value);
    if (!serviceId) return null;
    return servicesCache.find(service => service.id === serviceId) || null;
}

function refreshBonusPanel() {
    const user = getUser();
    const service = getSelectedService();
    const panel = $('#bonusPanel');
    const range = $('#bonusRange');
    const bonusInput = $('#bonusToSpend');

    if (!user || !service) {
        panel.classList.add('hidden');
        range.value = '0';
        range.max = '0';
        bonusInput.value = '0';
        $('#bonusSpendLabel').textContent = 'Списывается: 0 ₽';
        $('#bonusFinalPriceLabel').textContent = 'К оплате: 0 ₽';
        return;
    }

    panel.classList.remove('hidden');
    const maxBonus = Math.max(0, Math.min(
        Math.floor(Number(user.bonus_balance || 0)),
        Math.floor(Number(service.base_price || 0))
    ));
    const currentValue = Math.min(Number(range.value || 0), maxBonus);
    range.max = String(maxBonus);
    range.value = String(currentValue);
    bonusInput.value = String(currentValue);
    $('#bonusAvailableLabel').textContent = `Доступно: ${Number(user.bonus_balance || 0)} ₽`;
    $('#bonusSpendLabel').textContent = `Списывается: ${currentValue} ₽`;
    $('#bonusFinalPriceLabel').textContent = `К оплате: ${Math.max(Number(service.base_price || 0) - currentValue, 0)} ₽`;
}

// ============ Модалки ============
function openModal(id) { document.getElementById(id).classList.add('active'); }
function closeModal(id) { document.getElementById(id).classList.remove('active'); }

$('#openLogin').addEventListener('click', () => {
    openModal('authModal');
    showTab('login');
});
$('#openRegister').addEventListener('click', () => {
    openModal('authModal');
    showTab('register');
});
$('#closeAuth').addEventListener('click', () => closeModal('authModal'));
$('#openOrder').addEventListener('click', () => openModal('orderModal'));
$('#closeOrder').addEventListener('click', () => closeModal('orderModal'));

// Закрытие по клику на фон
$$('.modal').forEach(m => {
    m.addEventListener('click', e => {
        if (e.target === m) m.classList.remove('active');
    });
});

// ============ Табы авторизации ============
function showTab(tab) {
    if (tab === 'login') {
        $('#tabLogin').classList.add('active');
        $('#tabReg').classList.remove('active');
        $('#loginForm').classList.remove('hidden');
        $('#registerForm').classList.add('hidden');
    } else {
        $('#tabLogin').classList.remove('active');
        $('#tabReg').classList.add('active');
        $('#loginForm').classList.add('hidden');
        $('#registerForm').classList.remove('hidden');
    }
}

$('#tabLogin').addEventListener('click', () => showTab('login'));
$('#tabReg').addEventListener('click', () => showTab('register'));

// ============ Логин клиента ============
$('#loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
        const resp = await fetch(API + '/api/clients/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: fd.get('email'),
                password: fd.get('password')
            })
        });
        if (!resp.ok) {
            const err = await resp.json();
            alert(err.detail || 'Ошибка входа');
            return;
        }
        const user = await resp.json();
        setUser(user);
        closeModal('authModal');
        e.target.reset();
    } catch (err) {
        alert('Ошибка сети');
    }
});

// ============ Регистрация ============
$('#registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
        const resp = await fetch(API + '/api/clients/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: fd.get('fullname'),
                phone: fd.get('phone'),
                email: fd.get('email'),
                password: fd.get('password')
            })
        });
        if (!resp.ok) {
            const err = await resp.json();
            alert(err.detail || 'Ошибка регистрации');
            return;
        }
        const user = await resp.json();
        setUser(user);
        closeModal('authModal');
        e.target.reset();
        alert('Регистрация успешна! Вам начислено 3000 бонусов 🎉');
    } catch (err) {
        alert('Ошибка сети');
    }
});

// ============ Выход ============
$('#logoutBtn').addEventListener('click', clearUser);
$('#sidebarLogout').addEventListener('click', (e) => {
    e.preventDefault();
    clearUser();
});

$('#orderServiceSelect').addEventListener('change', refreshBonusPanel);
$('#bonusRange').addEventListener('input', () => {
    const value = Number($('#bonusRange').value || 0);
    $('#bonusToSpend').value = String(value);
    refreshBonusPanel();
});

// ============ Создание заявки ============
$('#orderForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const user = getUser();

    const body = {
        client_name: fd.get('fullname'),
        client_email: fd.get('email'),
        client_phone: fd.get('phone'),
        car_brand: fd.get('brand'),
        car_model: fd.get('model'),
        car_year: fd.get('year') ? parseInt(fd.get('year')) : null,
        service_id: fd.get('service_id') ? parseInt(fd.get('service_id')) : null,
        description: fd.get('description'),
        client_id: user ? user.id : null,
        bonus_to_spend: fd.get('bonus_to_spend') ? parseFloat(fd.get('bonus_to_spend')) : 0
    };

    try {
        const resp = await fetch(API + '/api/requests/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (!resp.ok) {
            const err = await resp.json();
            alert(err.detail || 'Ошибка отправки заявки');
            return;
        }
        const result = await resp.json();
        closeModal('orderModal');
        e.target.reset();
        if (user) {
            if (typeof result.bonus_balance === 'number') {
                setUser({ ...user, bonus_balance: result.bonus_balance });
            }
            $('#orderName').value = user.name;
            $('#orderEmail').value = user.email;
            $('#orderPhone').value = user.phone || '';
        }
        refreshBonusPanel();
        alert(`Заявка отправлена! К оплате: ${result.final_price} ₽ ✅`);
    } catch (err) {
        alert('Ошибка сети');
    }
});

// ============ Гамбургер — ЛК клиента ============
$('#userHamburger').addEventListener('click', () => {
    $('#userHamburger').classList.toggle('open');
    $('#userSidebar').classList.toggle('open');
});

// Навигация в сайдбаре ЛК
$('#navMyRequests').addEventListener('click', async (e) => {
    e.preventDefault();
    const user = getUser();
    if (!user) return;
    try {
        const resp = await fetch(API + `/api/clients/${user.id}`);
        const data = await resp.json();
        const cont = $('#sidebarContent');

        const statusLabels = {
            'new': '🟡 Новая',
            'accepted': '🔵 Принята',
            'in_progress': '🟠 В работе',
            'completed': '🟢 Завершена',
            'rejected': '🔴 Отклонена'
        };

        if (data.requests.length === 0) {
            cont.innerHTML = '<p>У вас пока нет заявок</p>';
        } else {
            cont.innerHTML = data.requests.map(r => `
                <div style="background:#2a2a34;padding:12px;border-radius:6px;margin-bottom:10px">
                    <div style="font-weight:bold;color:#fff">${r.car_brand} ${r.car_model}</div>
                    <div style="font-size:0.85rem;color:#aaa">${r.service_name || 'Без услуги'}</div>
                    <div style="font-size:0.85rem">${r.description || ''}</div>
                    <div style="margin-top:6px">${statusLabels[r.status] || r.status}</div>
                    <div style="font-size:0.75rem;color:#777;margin-top:4px">${r.created_at}</div>
                </div>
            `).join('');
        }
    } catch (e) {
        console.error(e);
    }
});

$('#navMyBonuses').addEventListener('click', async (e) => {
    e.preventDefault();
    const user = getUser();
    if (!user) return;
    try {
        const resp = await fetch(API + `/api/clients/${user.id}`);
        const data = await resp.json();
        const cont = $('#sidebarContent');
        cont.innerHTML = `
            <div style="background:linear-gradient(135deg,#1e1e24,#3a3a44);padding:20px;border-radius:8px;margin-bottom:15px">
                <div style="font-size:0.9rem;color:#aaa">Баланс бонусов</div>
                <div style="font-size:2rem;font-weight:bold;color:#ff4d4d">${data.client.bonus_balance} ₽</div>
            </div>
            <h4 style="color:#fff;margin-bottom:10px">История начислений</h4>
            ${data.bonuses.map(b => `
                <div style="background:#2a2a34;padding:10px;border-radius:6px;margin-bottom:8px">
                    <div style="color:${b.amount < 0 ? '#ff6b6b' : '#4caf50'};font-weight:bold">${b.amount > 0 ? '+' : ''}${b.amount} ₽</div>
                    <div style="font-size:0.85rem">${b.reason}</div>
                    <div style="font-size:0.75rem;color:#777">${b.created_at}</div>
                </div>
            `).join('')}
        `;
    } catch (e) {
        console.error(e);
    }
});

$('#navNewRequest').addEventListener('click', (e) => {
    e.preventDefault();
    // Закрываем сайдбар и открываем модалку заявки
    $('#userSidebar').classList.remove('open');
    $('#userHamburger').classList.remove('open');
    openModal('orderModal');
});

// ============ Анимации при скролле ============
function initScrollAnimations() {
    // Если браузер не поддерживает IntersectionObserver, просто показываем элементы
    if (!window.IntersectionObserver) {
        $$('.anim-fade-up, .anim-slide-in, .anim-zoom-in').forEach(el => {
            el.classList.add('animated');
        });
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, { threshold: 0.05 });

    $$('.anim-fade-up, .anim-slide-in, .anim-zoom-in').forEach(el => {
        observer.observe(el);
    });
}

// ============ Инициализация ============
document.addEventListener('DOMContentLoaded', () => {
    updateUI();
    loadServices();
    initScrollAnimations();
});
