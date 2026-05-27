import { AUTO_API, WAREHOUSE_API, api, requireRole, logout } from './api.js';
import './style.css';
const user = requireRole(['admin']);
document.querySelector('#adminName').textContent = user.fullname;
document.querySelector('#logoutBtn').onclick = logout;
const tbody = document.querySelector('#ordersBody');
const partsBody = document.querySelector('#partsBody');
const employeesSelect = document.querySelector('#employeeSelect');
async function loadEmployees() {
    const list = await api(AUTO_API, '/employees');
    employeesSelect.innerHTML =
        '<option value="">Без мастера</option>' +
        list.map((e) => `<option value="${e.id}">${e.fullname} — ${e.position}</option>`).join('');
}
async function loadOrders() {
    const orders = await api(AUTO_API, '/orders');
    tbody.innerHTML = orders
        .map(
            (o) =>
                `<tr><td>#${o.id}</td><td>${o.client.fullname}<br><span class="muted">${o.client.phone}</span></td><td>${o.car.brand} ${o.car.model}</td><td>${o.service_name}</td><td><span class="badge">${o.status}</span></td><td>${o.employee ? o.employee.fullname : '—'}</td><td><button class="btn btn-primary" data-edit="${o.id}">Обновить</button></td></tr>`
        )
        .join('');
    document
        .querySelectorAll('[data-edit]')
        .forEach((b) => (b.onclick = () => updateOrder(b.dataset.edit)));
}
async function updateOrder(id) {
    const status = prompt('Новый статус: Новый / В работе / Выполнен / Закрыт', 'В работе');
    if (!status) return;
    const employee_id = employeesSelect.value ? Number(employeesSelect.value) : null;
    await api(AUTO_API, `/orders/${id}`, 'PATCH', { status, employee_id });
    await loadOrders();
}
async function loadParts() {
    const parts = await api(WAREHOUSE_API, '/parts');
    partsBody.innerHTML = parts
        .map(
            (p) =>
                `<tr><td>${p.name}</td><td>${p.sku}</td><td>${p.price} ₽</td><td>${p.stock}</td></tr>`
        )
        .join('');
}
document.querySelector('#partForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.target;
    try {
        await api(WAREHOUSE_API, '/parts/', 'POST', {
            name: f.name.value,
            sku: f.sku.value,
            price: Number(f.price.value),
            stock: Number(f.stock.value),
        });
        f.reset();
        loadParts();
    } catch (err) {
        alert(err.message);
    }
});
await loadEmployees();
await loadOrders();
await loadParts();
