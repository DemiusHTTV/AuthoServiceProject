export const AUTO_API = import.meta.env.VITE_AUTO_API || 'http://127.0.0.1:8000';
export const WAREHOUSE_API = import.meta.env.VITE_WAREHOUSE_API || 'http://127.0.0.1:8001';

export async function api(base, endpoint, method = 'GET', data = null) {
    const options = { method, headers: { 'Content-Type': 'application/json' } };
    if (data) options.body = JSON.stringify(data);
    const res = await fetch(`${base}${endpoint}`, options);
    const json = await res.json().catch(() => ({ detail: 'Ошибка ответа сервера' }));
    if (!res.ok) throw new Error(json.detail || 'Ошибка запроса');
    return json;
}
export function getUser() {
    return JSON.parse(localStorage.getItem('user') || 'null');
}
export function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}
export function logout() {
    localStorage.removeItem('user');
    location.href = '/';
}
export function requireRole(roles) {
    const user = getUser();
    if (!user || !roles.includes(user.role)) {
        alert('Доступ запрещен');
        location.href = '/';
    }
    return user;
}
