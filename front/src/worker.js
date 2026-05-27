import { AUTO_API, api, requireRole, logout } from './api.js';
import './style.css';
const user = requireRole(['worker', 'admin']);
document.querySelector('#workerName').textContent = user.fullname;
document.querySelector('#logoutBtn').onclick = logout;
async function load() {
    const orders = await api(AUTO_API, '/orders');
    document.querySelector('#ordersBody').innerHTML = orders
        .filter((o) => o.status !== 'Закрыт')
        .map(
            (o) =>
                `<tr><td>#${o.id}</td><td>${o.car.brand} ${o.car.model}</td><td>${o.service_name}<br><span class="muted">${o.description || ''}</span></td><td><span class="badge">${o.status}</span></td><td><button class="btn btn-primary" data-status="В работе" data-id="${o.id}">В работу</button> <button class="btn btn-primary" data-status="Выполнен" data-id="${o.id}">Выполнен</button></td></tr>`
        )
        .join('');
    document.querySelectorAll('[data-status]').forEach(
        (b) =>
            (b.onclick = async () => {
                await api(AUTO_API, `/orders/${b.dataset.id}`, 'PATCH', {
                    status: b.dataset.status,
                });
                load();
            })
    );
}
load();
