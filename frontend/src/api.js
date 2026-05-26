const BASE_URL = 'http://localhost:3000/api';

async function sendRequest(endpoint, method = 'GET', body = null) {
    const url = `${BASE_URL}${endpoint}`;
    
    // Получаем токен из localStorage, если пользователь уже авторизован
    const token = localStorage.getItem('token');
    
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    };

    // Если токен есть, добавляем его в заголовки для защищенных роутов
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method: method,
        headers: headers
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(url, config);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Ошибка сервера: ${response.status}`);
        }

        if (response.status === 204) return null;

        return await response.json();
    } catch (error) {
        console.error(`Ошибка при запросе к ${url}:`, error.message);
        throw error;
    }
}

export const api = {
    // ==========================================
    // 1. АВТОРИЗАЦИЯ И ТАБЛИЦА КЛИЕНТОВ (AUTH & USERS)
    // ==========================================
    
    // Вход для клиентов и менеджеров/админов (бэкенд сам поймет по роли или роуту)
    login: (credentials) => {
        return sendRequest('/auth/login', 'POST', credentials);
    },

    // Регистрация нового клиента на сайте
    register: (userData) => {
        return sendRequest('/auth/register', 'POST', userData);
    },

    // Получить данные текущего авторизованного пользователя (сессия)
    getCurrentUser: () => {
        return sendRequest('/auth/me', 'GET');
    },

    // Получить список всех клиентов (для таблицы в админке менеджера)
    getAllClients: () => {
        return sendRequest('/clients', 'GET');
    },


    // ==========================================
    // 2. ЗАЯВКИ И ЗАПИСИ НА РЕМОНТ (APPOINTMENTS)
    // ==========================================
    
    // Создать новую заявку на ремонт (из модалки на главной или формы)
    createAppointment: (appointmentData) => {
        return sendRequest('/appointments', 'POST', appointmentData);
    },

    // Получить записи текущего клиента (для отображения в его Личном Кабинете)
    getClientAppointments: () => {
        return sendRequest('/appointments/my', 'GET');
    },

    // Получить ВСЕ заявки и записи (для таблицы в панели администратора)
    getAllAppointments: () => {
        return sendRequest('/appointments', 'GET');
    },

    // Изменить статус заявки (например: "Ожидает подтверждения" -> "Подтверждена" или "В работе")
    updateAppointmentStatus: (id, status) => {
        return sendRequest(`/appointments/${id}/status`, 'PUT', { status });
    },

    // Удалить или отменить запись/заявку
    deleteAppointment: (id) => {
        return sendRequest(`/appointments/${id}`, 'DELETE');
    },


    // ==========================================
    // 3. ЛИЧНЫЙ ГАРАЖ АВТОМОБИЛЕЙ (GARAGE)
    // ==========================================
    
    // Получить список машин в гараже авторизованного клиента
    getGarage: () => {
        return sendRequest('/garage', 'GET');
    },

    // Добавить новый автомобиль в свой гараж
    addCarToGarage: (carData) => {
        return sendRequest('/garage', 'POST', carData);
    },


    // ==========================================
    // 4. БОНУСНАЯ ПРОГРАММА (BONUSES)
    // ==========================================
    
    // Получить текущий баланс баллов клиента и историю их начислений
    getBonusInfo: () => {
        return sendRequest('/bonuses', 'GET');
    }
};