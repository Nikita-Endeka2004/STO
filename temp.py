from db import update_one_in_works, get_last_inserted_user_id, get_one_from_works_json
import tkinter as tk

def update_data():
    # Получаем значения из полей
    work = work_entry.get()
    amount = amount_entry.get()
    count = count_entry.get()
    update_one_in_works(data["id"], work, amount, count)

# Создаем главное окно
root = tk.Tk()
root.title("Форма обновления данных")

data = get_one_from_works_json(33)

# Создаем фрейм для формы
form_frame = tk.Frame(root)
form_frame.pack(padx=10, pady=10)

# Создаем метки и поля ввода для каждого параметра
tk.Label(form_frame, text="Робота:").grid(row=0, column=0, sticky="w")
work_entry = tk.Entry(form_frame)
work_entry.grid(row=0, column=1)
work_entry.insert(0, data["work"])

tk.Label(form_frame, text="Вартість:").grid(row=1, column=0, sticky="w")
amount_entry = tk.Entry(form_frame)
amount_entry.grid(row=1, column=1)
amount_entry.insert(0, str(data["amount"]))

tk.Label(form_frame, text="Кількість:").grid(row=2, column=0, sticky="w")
count_entry = tk.Entry(form_frame)
count_entry.grid(row=2, column=1)
count_entry.insert(0, str(data["count"]))

# Кнопка для обновления данных
update_button = tk.Button(root, text="Оновити", command=update_data)
update_button.pack(pady=10)

# Запускаем главный цикл обработки событий
root.mainloop()
