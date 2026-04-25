import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# Определяем основные параметры
MIN_LENGTH = 4
MAX_LENGTH = 20
history_file = 'password_history.json'


def load_history():
    """Загружает историю паролей из JSON файла."""
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []


def save_history(history):
    """Сохраняет историю паролей в JSON файл."""
    with open(history_file, 'w') as file:
        json.dump(history, file, indent=4)


def generate_password():
    """Генерирует случайный пароль согласно выбранным параметрам."""
    length = length_slider.get()
    if length < MIN_LENGTH or length > MAX_LENGTH:
        messagebox.showerror("Ошибка", f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH} символов.")
        return

    characters = ''
    if letters_var.get():
        characters += string.ascii_letters  # Буквы
    if digits_var.get():
        characters += string.digits          # Цифры
    if symbols_var.get():
        characters += string.punctuation     # Символы

    if not characters:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    result_label.config(text=password)

    # Сохранение пароля в историю
    history.append(password)
    history_listbox.insert(tk.END, password)
    save_history(history)


# Создаем главное окно
root = tk.Tk()
root.title("Генератор случайных паролей")

# Ползунок длины пароля
length_slider = tk.Scale(root, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL, label="Длина пароля")
length_slider.pack()

# Чекбоксы для выбора типов символов
letters_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=False)
symbols_var = tk.BooleanVar(value=False)

letters_check = tk.Checkbutton(root, text="Буквы", variable=letters_var)
digits_check = tk.Checkbutton(root, text="Цифры", variable=digits_var)
symbols_check = tk.Checkbutton(root, text="Символы", variable=symbols_var)

letters_check.pack()
digits_check.pack()
symbols_check.pack()

# Кнопка генерации пароля
generate_button = tk.Button(root, text="Сгенерировать", command=generate_password)
generate_button.pack()

# Метка для отображения сгенерированного пароля
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack()

# Таблица истории
history_label = tk.Label(root, text="История паролей:")
history_label.pack()

history = load_history()
history_listbox = tk.Listbox(root)
for item in history:
    history_listbox.insert(tk.END, item)

history_listbox.pack()

# Запуск основного цикла приложения
root.mainloop()
