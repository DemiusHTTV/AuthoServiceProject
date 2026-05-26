const BASE_URL = 'http://localhost:8000/api'; // Порт твоего FastAPI автосервиса

async function sendRequest(endpoint, method = 'GET', body = null) {
    const url = `${BASE_URL}${endpoint}`;
    
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    };

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
            throw new Error(errorData.detail || errorData.message || `Ошибка сервера: ${response.status}`);
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
    
    // Вход: бэк проверит логин/пароль и вернет id пользователя и тип (клиент/менеджер)
    login: (credentials) => {
        return sendRequest('/auth/login', 'POST', credentials);
    },

    // Регистрация нового клиента
    register: (userData) => {
        return sendRequest('/auth/register', 'POST', userData);
    },

    // Получить данные клиента по его ID (вместо токена передаем id параметром)
    getCurrentUser: (clientId) => {
        return sendRequest(`/auth/me?client_id=${clientId}`, 'GET');
    },

    // Получить список всех клиентов (для таблицы в админке менеджера)
    getAllClients: () => {
        return sendRequest('/clients', 'GET');
    },


    // ==========================================
    // 2. ЗАЯВКИ И ЗАПИСИ НА РЕМОНТ (APPOINTMENTS)
    // ==========================================
    
    // Создать новую заявку на ремонт (передаем данные + client_id)
    createAppointment: (appointmentData) => {
        return sendRequest('/appointments', 'POST', appointmentData);
    },

    // Получить записи конкретного клиента для его Личного Кабинета
    getClientAppointments: (clientId) => {
        return sendRequest(`/appointments/my?client_id=${clientId}`, 'GET');
    },

    // Получить ВСЕ заявки (для таблицы в панели администратора)
    getAllAppointments: () => {
        return sendRequest('/appointments', 'GET');
    },

    // Изменить статус заявки (Менеджер одобряет/меняет статус)
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
    
    // Получить список машин конкретного клиента
    getGarage: (clientId) => {
        return sendRequest(`/garage?client_id=${clientId}`, 'GET');
    },

    // Добавить новый автомобиль в гараж
    addCarToGarage: (carData) => {
        return sendRequest('/garage', 'POST', carData);
    },


    // ==========================================
    // 4. БОНУСНАЯ ПРОГРАММА (BONUSES)
    // ==========================================
    
    // Получить текущий баланс баллов клиента
    getBonusInfo: (clientId) => {
        return sendRequest(`/bonuses?client_id=${clientId}`, 'GET');
    }
};