const user = JSON.parse(localStorage.getItem('user'));
if (!user || user.role !== 'admin') {
    alert("Доступ запрещен!");
    window.location.href = 'index.html';
} else {
    document.getElementById('adminName').innerText = user.fullname;
    document.getElementById('adminData').innerHTML = '<p>Добро пожаловать в панель управления!</p>';
}

document.querySelector('.logout').addEventListener('click', () => {
    localStorage.removeItem('user');
});
