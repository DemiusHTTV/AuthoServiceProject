/**
 * main.js — логика главной страницы: авторизация, заявки, ЛК (гамбургер-сайдбар)
 */
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

function updateUI() {
    const user = getUser();
    if (user) {
        $('#authBlock').classList.add('hidden');
        $('#profileBlock').classList.remove('hidden');
        $('#profileName').textContent = user.name;
        $('#userHamburger').classList.remove('hidden');
        $('#sidebarUserName').textContent = user.name;
        $('#sidebarUserEmail').textContent = user.email;
        $('#orderName').value = user.name || '';
        $('#orderName').readOnly = true;
        $('#orderEmail').value = user.email || '';
        $('#orderEmail').readOnly = true;
        $('#orderPhone').value = user.phone || '';
        $('#orderPhone').readOnly = true;
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
    }
}

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

$$('.modal').forEach(m => {
    m.addEventListener('click', e => {
        if (e.target === m) m.classList.remove('active');
    });
});

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

$('#loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    setUser({ name: 'Пользователь', email: fd.get('email'), phone: '' });
    closeModal('authModal');
    e.target.reset();
});

$('#registerForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    setUser({ name: fd.get('fullname'), email: fd.get('email'), phone: fd.get('phone') });
    closeModal('authModal');
    e.target.reset();
    alert('Регистрация успешна! Вам начислено 3000 бонусов 🎉');
});

$('#logoutBtn').addEventListener('click', clearUser);
$('#sidebarLogout').addEventListener('click', (e) => {
    e.preventDefault();
    clearUser();
});

$('#orderForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const user = getUser();
    closeModal('orderModal');
    e.target.reset();
    if (user) {
        $('#orderName').value = user.name;
        $('#orderEmail').value = user.email;
        $('#orderPhone').value = user.phone || '';
    }
    alert('Заявка отправлена! ✅');
});

$('#userHamburger').addEventListener('click', () => {
    $('#userHamburger').classList.toggle('open');
    $('#userSidebar').classList.toggle('open');
});

$('#navNewRequest').addEventListener('click', (e) => {
    e.preventDefault();
    $('#userSidebar').classList.remove('open');
    $('#userHamburger').classList.remove('open');
    openModal('orderModal');
});

function initScrollAnimations() {
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

document.addEventListener('DOMContentLoaded', () => {
    updateUI();
    initScrollAnimations();
});