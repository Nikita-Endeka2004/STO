import pdfkit
from jinja2 import FileSystemLoader, Environment
from datetime import date
import os
from db import get_last_inserted_user_id, get_all_from_works_json, get_last_inserted_user
import subprocess
def createPdfFile():
    def open_pdf(filename):
        output_directory = "D:/Table/Order/ProgramFile/STO/pdf_files"
        pdf_path = os.path.join(output_directory, filename)
        subprocess.Popen(["C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", pdf_path])


    def render_html(data, currentDate, totalCost, lastUser):
        env = Environment(loader=FileSystemLoader('D:/Table/Order/ProgramFile/STO/'))
        template = env.get_template('test.html')
        html_out = template.render(data=data, currentDate=currentDate, totalCost=totalCost, lastUser=lastUser)
        return html_out

    def create_pdf(html_content, filename):
        output_directory = "D:/Table/Order/ProgramFile/STO/pdf_files"
        output_path = os.path.join(output_directory, filename)
        if os.path.exists(output_path):  # Проверяем, существует ли файл с таким же именем
            base_name, ext = os.path.splitext(filename)
            counter = 1
            while True:
                new_filename = f"{base_name} ({counter}){ext}"  # Создаем новое имя файла с припиской
                output_path = os.path.join(output_directory, new_filename)
                if not os.path.exists(output_path):  # Проверяем, существует ли файл с новым именем
                    break
                counter += 1
        options = {
            'enable-local-file-access': None  # Enable local file access
        }
        pdfkit.from_string(html_content, output_path, configuration=pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"), options=options)

    # Пример данных для таблицы
    last_id = get_last_inserted_user_id()
    data = get_all_from_works_json(last_id)
    lastUser = get_last_inserted_user()
    today = date.today()
    currentDate = today.strftime("%d/%m/%Y")
    totalCost = 0
    for cost in data:
        totalCost += cost['amount']
    # Рендерим HTML из шаблона
    html_content = render_html(data,currentDate,totalCost, lastUser)
    # Создаем PDF-файл
    filename = f"{lastUser["vin"]}_{lastUser["car_number"]}_{lastUser["fio"]}.pdf"
    create_pdf(html_content, filename)
    open_pdf(filename)