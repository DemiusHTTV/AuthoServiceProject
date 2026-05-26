import tkinter as tk
from tkinter import messagebox

# Импортируем наши обновленные функции
from app.api import (
    login,
    get_worker_requests,
    update_request_status,
)


class WorkerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoService Worker")
        self.root.geometry("620x500")
        
        # Хранилище для ID текущего вошедшего мастера
        self.current_worker_id = None 

        self.show_login()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        self.current_worker_id = None # Сбрасываем сессию при выходе

        tk.Label(
            self.root,
            text="Вход мастера",
            font=("Arial", 18, "bold"),
        ).pack(pady=30)

        tk.Label(self.root, text="Логин").pack()

        self.login_entry = tk.Entry(
            self.root,
            width=30,
        )
        self.login_entry.pack(pady=5)

        tk.Label(self.root, text="Пароль").pack()

        self.password_entry = tk.Entry(
            self.root,
            show="*",
            width=30,
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Войти",
            width=20,
            command=self.handle_login,
        ).pack(pady=20)

    def handle_login(self):
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        try:
            data = login(username, password)

            # Проверяем роль, которую прислал бэкенд
            role = data.get("type") or data.get("role")
            
            if role != "worker":
                messagebox.showerror(
                    "Ошибка",
                    "Это приложение только для мастеров",
                )
                return

            # 🔥 СОХРАНЯЕМ ID мастера из ответа бэкенда
            self.current_worker_id = data.get("worker_id") or data.get("user_id")
            
            if not self.current_worker_id:
                raise Exception("ID мастера не найден в ответе сервера")

            self.show_requests()

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось выполнить вход: {str(e)}",
            )

    def show_requests(self):
        self.clear()

        top = tk.Frame(self.root)
        top.pack(fill="x", padx=20, pady=15)

        tk.Label(
            top,
            text="Мои заявки",
            font=("Arial", 18, "bold"),
        ).pack(side="left")

        tk.Button(
            top,
            text="Обновить",
            command=self.show_requests,
        ).pack(side="right")

        try:
            # 🔥 Передаем ID мастера, чтобы получить только его задачи
            requests = get_worker_requests(self.current_worker_id)

        except Exception:
            messagebox.showerror(
                "Ошибка",
                "Не удалось загрузить заявки",
            )
            requests = []

        if not requests:
            tk.Label(
                self.root,
                text="Назначенных заявок нет",
            ).pack(pady=30)

        # Контейнер со скроллом или просто пакуем списком
        for item in requests:
            self.render_request(item)

        tk.Button(
            self.root,
            text="Выйти",
            command=self.show_login,
        ).pack(pady=15)

    def render_request(self, item: dict):
        frame = tk.Frame(
            self.root,
            borderwidth=1,
            relief="solid",
            padx=10,
            pady=8,
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=8,
        )

        request_id = item["id"]

        # Поддерживаем и старые, и новые ключи из Pydantic-схем, чтобы ничего не упало
        client = item.get("client_name") or item.get("client") or "Неизвестный клиент"
        car_brand = item.get("car_brand") or ""
        car_model = item.get("car_model") or item.get("car_name") or "Неизвестное авто"
        service = item.get("service_name") or item.get("service") or "Неизвестная услуга"
        status = item.get("status", "unknown")

        tk.Label(
            frame,
            text=f"Заявка №{request_id}",
            font=("Arial", 12, "bold"),
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=f"Клиент: {client}",
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=f"Автомобиль: {car_brand} {car_model}".strip(),
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=f"Услуга: {service}",
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=f"Статус: {status}",
        ).pack(anchor="w")

        buttons = tk.Frame(frame)
        buttons.pack(anchor="e", pady=5)

        tk.Button(
            buttons,
            text="В работу",
            command=lambda: self.change_status(
                request_id,
                "В работе", # Передаем красивую строку статуса вместо 'in_work'
            ),
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Выполнено",
            command=lambda: self.change_status(
                request_id,
                "Выполнено", # Передаем красивую строку статуса вместо 'done'
            ),
        ).pack(side="left", padx=5)

    def change_status(
        self,
        request_id: int,
        status: str,
    ):
        try:
            update_request_status(
                request_id,
                status,
            )

            messagebox.showinfo(
                "Готово",
                "Статус обновлен",
            )

            self.show_requests()

        except Exception:
            messagebox.showerror(
                "Ошибка",
                "Не удалось обновить статус",
            )

    def run(self):
        self.root.mainloop()