// --- 1. ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ---
// Восстанавливаем сессию, если она была (автологин)
let currentUser = JSON.parse(localStorage.getItem('user')) || null;

// --- API SERVICE (Общий помощник) ---
const API_URL = 'http://127.0.0.1:8000';

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (data) options.body = JSON.stringify(data);
    
    const response = await fetch(`${API_URL}${endpoint}`, options);
    const result = await response.json();
    
    if (!response.ok) throw new Error(result.detail || "Request failed");
    return result;
}

// --- 2. ЭЛЕМЕНТЫ DOM (твои без изменений) ---
const authModal = document.getElementById('authModal');
const openLoginBtn = document.getElementById('openLoginBtn');
const openRegisterBtn = document.getElementById('openRegisterBtn');
const closeAuthModalBtn = document.getElementById('closeAuthModalBtn');
const tabLoginBtn = document.getElementById('tabLoginBtn');
const tabRegisterBtn = document.getElementById('tabRegisterBtn');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const authBlock = document.getElementById('authBlock');
const profileBlock = document.getElementById('profileBlock');
const headerUserName = document.getElementById('headerUserName');
const logoutBtn = document.getElementById('logoutBtn');
const userHamburgerBtn = document.getElementById('userHamburgerBtn');
const userSidebar = document.getElementById('userSidebar');
const orderModal = document.getElementById('orderModal');
const heroOrderBtn = document.getElementById('heroOrderBtn');
const closeOrderModalBtn = document.getElementById('closeOrderModalBtn');
const orderForm = document.getElementById('orderForm');
const cabinetModal = document.getElementById('cabinetModal');
const closeCabinetModalBtn = document.getElementById('closeCabinetModalBtn');

// --- 3. ФУНКЦИИ УПРАВЛЕНИЯ UI ---
function showModal(modalNode) { modalNode.style.display = 'flex'; }
function hideModal(modalNode) { modalNode.style.display = 'none'; }

function switchAuthTab(tab) {
    const isLogin = tab === 'login';
    tabLoginBtn.classList.toggle('active', isLogin);
    tabRegisterBtn.classList.toggle('active', !isLogin);
    loginForm.classList.toggle('active', isLogin);
    registerForm.classList.toggle('active', !isLogin);
}

function loginUser(userData) {
    currentUser = userData;
    localStorage.setItem('user', JSON.stringify(currentUser));
    hideModal(authModal);
    authBlock.style.display = 'none';
    profileBlock.style.display = 'flex';
    userHamburgerBtn.style.display = 'flex';
    headerUserName.innerText = currentUser.fullname;
}

// --- 4. ЛОГИКА API ---
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        await apiRequest('/register', 'POST', {
            fullname: document.getElementById('regName').value,
            phone: document.getElementById('regPhone').value,
            email: document.getElementById('regEmail').value,
            password: document.getElementById('regPassword').value
        });
        alert("Регистрация успешна!");
        switchAuthTab('login');
        registerForm.reset();
    } catch (err) { alert("Ошибка: " + err.message); }
});

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const data = await apiRequest('/login', 'POST', {
            email: document.getElementById('loginEmail').value,
            password: document.getElementById('loginPassword').value
        });
        loginUser(data.user);
    } catch (err) { alert("Ошибка входа: " + err.message); }
});

// --- 5. ОБРАБОТЧИКИ СОБЫТИЙ ---
openLoginBtn.addEventListener('click', () => { switchAuthTab('login'); showModal(authModal); });
openRegisterBtn.addEventListener('click', () => { switchAuthTab('register'); showModal(authModal); });
closeAuthModalBtn.addEventListener('click', () => hideModal(authModal));
tabLoginBtn.addEventListener('click', () => switchAuthTab('login'));
tabRegisterBtn.addEventListener('click', () => switchAuthTab('register'));

logoutBtn.addEventListener('click', () => {
    currentUser = null;
    localStorage.removeItem('user');
    location.reload();
});

// Инициализация интерфейса при загрузке страницы
if (currentUser) loginUser(currentUser);

// Остальные обработчики (hamburger, modal и т.д.)
userHamburgerBtn.addEventListener('click', () => {
    userHamburgerBtn.classList.toggle('open');
    userSidebar.classList.toggle('open');
});
async function loadCabinetData() {
    if (!currentUser) return;

    try {
        const data = await apiRequest(`/users/cabinet/${currentUser.email}`);
        
        // Очищаем и наполняем контент кабинета
        cabinetTargetContent.innerHTML = `
            <h3>Привет, ${data.fullname}!</h3>
            <h4>Твои авто:</h4>
            <ul>${data.cars.map(c => `<li>${c.brand} ${c.model} (VIN: ${c.vin})</li>`).join('')}</ul>
            <h4>Твои заказы:</h4>
            <ul>${data.orders.map(o => `<li>Статус: ${o.status}</li>`).join('')}</ul>
        `;
    } catch (err) {
        cabinetTargetContent.innerHTML = `<p>Ошибка загрузки данных: ${err.message}</p>`;
    }
}

heroOrderBtn.addEventListener('click', () => showModal(orderModal));
closeOrderModalBtn.addEventListener('click', () => hideModal(orderModal));
closeCabinetModalBtn.addEventListener('click', () => hideModal(cabinetModal));

window.openCabinetSection = function(section) {
    userSidebar.classList.remove('open');
    userHamburgerBtn.classList.remove('open');
    
    // Вызываем загрузку данных
    loadCabinetData();
    
    showModal(cabinetModal);
};