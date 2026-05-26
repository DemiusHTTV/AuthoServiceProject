// В твоем src/main.js
const registerForm = document.getElementById('registerForm');

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const userData = {
        fullname: document.getElementById('regName').value,
        phone: document.getElementById('regPhone').value,
        email: document.getElementById('regEmail').value,
        password: document.getElementById('regPassword').value // Теперь оно тут есть!
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/api/users/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            alert("Регистрация прошла успешно! Теперь войдите в систему.");
            switchAuthTab('login'); // Переключаем на вкладку входа
        } else {
            const errorData = await response.json();
            alert("Ошибка: " + (errorData.detail || "Что-то пошло не так"));
        }
    } catch (error) {
        console.error("Ошибка сети:", error);
    }
});