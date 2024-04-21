from db import *
from pdf_generator import createPdfFile
from datetime import datetime
import tkinter as tk
import subprocess
import re
import os

def main():

    def postUser():
      vin = vin_entry.get()
      car_number = car_number_entry.get()
      fio = fio_entry.get()
      date = datetime.now().strftime("%Y-%m-%d %H:%M")

      # post_to_database_user(vin, car_number, fio, date)

      work_data()

    def postWork():
      work = work_entry.get()
      amount = amount_entry.get()
      count = count_entry.get()
      work_entry.delete(0, tk.END)
      amount_entry.delete(0, tk.END)
      count_entry.delete(0, tk.END)
      validate_entries()
      last_id = get_last_inserted_user_id()
      post_to_database_works(work, amount, count, last_id)
      getWork_entry = get_all_from_works(last_id)

      scrollbar.pack(side="right", fill="y")
      scrollbar.config(command=text_widget.yview)
      text_widget.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
      # Добавляем данные в текстовое поле с разделителями между строками
      text_widget.delete("1.0", tk.END)
      for i, data in enumerate(getWork_entry, start=1):
          text_widget.insert(tk.END, f"{i}. Работа: ", "bold")  # Жирный стиль текста
          text_widget.insert(tk.END, f"{data[1]} - ", "normal")  # Обычный стиль текста
          text_widget.insert(tk.END, "Вартість: ", "bold")  # Жирный стиль текста
          text_widget.insert(tk.END, f"{str(data[2])}, ", "normal")  # Обычный стиль текста
          text_widget.insert(tk.END, "Кількість: ", "bold")  # Жирный стиль текста
          text_widget.insert(tk.END, f"{str(data[3])}\n", "normal")  # Обычный стиль текста
          # Добавляем разделитель между строками, кроме последней
          if i < len(getWork_entry):
              text_widget.insert(tk.END, "\n" + "-" * 80 + "\n")

    def validate_entries():
      if work_entry.get() and amount_entry.get() and count_entry.get():
          submit_button_work.config(state=tk.NORMAL)
      else:
          submit_button_work.config(state=tk.DISABLED)

    def work_data():
      # Удаление всех элементов на экране
      list = create_screen.grid_slaves()
      for l in list:
          l.destroy()

      # Создаем фрейм для формы
      form_frame = tk.Frame(create_screen)
      create_screen.geometry("1000x500")
      form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

      # Создаем виджеты для новой формы
      tk.Label(form_frame, text="Робота:").grid(row=0, column=0, sticky="w")
      tk.Label(form_frame, text="Вартість:").grid(row=1, column=0, sticky="w")
      tk.Label(form_frame, text="Кількість:").grid(row=2, column=0, sticky="w")

      global work_entry, amount_entry, count_entry, submit_button_work, text_widget
      work_entry = tk.Entry(form_frame)
      amount_entry = tk.Entry(form_frame)
      count_entry = tk.Entry(form_frame)
      work_entry.grid(row=0, column=1)
      amount_entry.grid(row=1, column=1)
      count_entry.grid(row=2, column=1)

      amount_entry.config(validate="key", validatecommand=(root.register(lambda P: P.isdigit() or P == ""), "%P"))
      count_entry.config(validate="key", validatecommand=(root.register(lambda P: P.isdigit() or P == ""), "%P"))
      work_entry.bind("<KeyRelease>", lambda event: validate_entries())
      amount_entry.bind("<KeyRelease>", lambda event: validate_entries())
      count_entry.bind("<KeyRelease>", lambda event: validate_entries())


      # Кнопка для отправки данных на сервер
      submit_button_work = tk.Button(form_frame, text="Відправити", command=postWork)
      validate_entries()
      submit_button_work.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

      # Кнопка для создания pdf
      submit_button_pdf = tk.Button(create_screen, text="Створити pdf", command=createPdfFile)
      validate_entries()
      submit_button_pdf.grid(row=4, column=0, columnspan=2)

      # Создаем фрейм для скроллинга
      global scroll_frame, scrollbar, getWork_entry
      scroll_frame = tk.Frame(create_screen)
      scroll_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

      # Создаем скроллбар для списка записей
      scrollbar = tk.Scrollbar(scroll_frame)
      scrollbar.pack(side="right", fill="y")

      text_widget = tk.Text(scroll_frame, wrap="word", yscrollcommand=scrollbar.set)
      text_widget.pack(side="left", fill="both", expand=True)


    def show_search_screen():
        output_directory = "D:/Table/Order/ProgramFile/STO/pdf_files"
        def find_files(search_term):
            results = []
            search_pattern = re.compile(rf".*{search_term}.*", flags=re.IGNORECASE)
            for filename in os.listdir(output_directory):
                if filename.endswith(".pdf") and search_pattern.search(filename):
                    results.append(filename)
            return results

        def search():
            search_term = entry.get()
            results = find_files(search_term)
            if results:
                result_window = tk.Toplevel(create_find_screen)
                result_window.geometry("500x400")
                result_window.title("Результати пошуку")
                for result in results:
                    file_frame = tk.Frame(result_window)
                    file_frame.pack()
                    label = tk.Label(file_frame, text=result)
                    label.pack(side=tk.LEFT)
                    open_button = tk.Button(file_frame, text="Відкрити", command=lambda file=result: open_pdf(file))
                    open_button.pack(side=tk.LEFT)
            else:
                tk.messagebox.showinfo("Результати пошуку", "Нічого не знайдено")

        def open_pdf(filename):
            pdf_path = os.path.join(output_directory, filename)
            subprocess.Popen(["C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", pdf_path])

        # Создаем  окно
        create_find_screen = tk.Toplevel(root)
        create_find_screen.title("Пошук PDF файлів")
        create_find_screen.geometry("400x200")
        # Добавляем поле для ввода
        entry = tk.Entry(create_find_screen, width=50)
        entry.pack(pady=10)

        # Добавляем кнопку "Найти"
        search_button = tk.Button(create_find_screen, text="Знайти", command=search, padx=10, pady=10)
        search_button.pack(pady=5)

    def show_create_screen():
      global create_screen
      create_screen = tk.Toplevel(root)  # Создание дочернего окна
      create_screen.geometry("400x300")
      # Создание виджетов для ввода данных
      tk.Label(create_screen, text="VIN:").grid(row=0, column=0)
      tk.Label(create_screen, text="Номер автівки:").grid(row=1, column=0)
      tk.Label(create_screen, text="ПІБ:").grid(row=2, column=0)
      
      global vin_entry, car_number_entry, fio_entry
      vin_entry = tk.Entry(create_screen, width=30)
      car_number_entry = tk.Entry(create_screen, width=30)
      fio_entry = tk.Entry(create_screen, width=30)
      
      vin_entry.grid(row=0, column=1)
      car_number_entry.grid(row=1, column=1)
      fio_entry.grid(row=2, column=1)
      
      # Кнопка для отправки данных на сервер
      submit_button = tk.Button(create_screen, text="Далі", command=postUser, padx=10, pady=7)
      submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
      
    # Создание основного окна
    root = tk.Tk()

    root.geometry("400x300")

    # Создание кнопок
    search_button = tk.Button(root, text="Знайти", command=show_search_screen,
                                font=("Helvetica", 12),
                              borderwidth=2, relief="raised", padx=10, pady=5)
    create_button = tk.Button(root, text="Створити", command=show_create_screen,
                                font=("Helvetica", 12),
                              borderwidth=2, relief="raised", padx=10, pady=5)

    # Размещение кнопок на основном окне
    search_button.pack(pady=5)
    create_button.pack(pady=5)

    # Запуск цикла обработки событий
    root.mainloop()

if __name__ == "__main__":
    main()