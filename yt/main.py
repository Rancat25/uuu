import flet as ft
import mysql.connector

# الاتصال بقاعدة البيانات
def save_to_database(name_v, phone_v, email_v, wilaya_v, address_v, image_data):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # تأكد من تغييرها لكلمة المرور الخاصة بك في MySQL
            database='my_database'
        )
        cursor = conn.cursor()
        sql = "INSERT INTO my_table (name, phone, email, wilaya, addres, image) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name_v, phone_v, email_v, wilaya_v, address_v, image_data))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return False

def search_in_database(keyword):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # تأكد من تغييرها لكلمة المرور الخاصة بك في MySQL
            database='my_database'
        )
        cursor = conn.cursor()
        sql = "SELECT name, phone, email, wilaya, addres FROM my_table WHERE name LIKE %s OR phone LIKE %s OR email LIKE %s OR wilaya LIKE %s OR addres LIKE %s"
        search_keyword = '%' + keyword + '%'
        cursor.execute(sql, (search_keyword, search_keyword, search_keyword, search_keyword, search_keyword))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return []

# واجهة Flet
def main(page: ft.Page):
    page.title = "Database Interface"
    page.bgcolor = "#f0e4ec"

    # متغير لتخزين بيانات الصورة
    image_data = None

    # مكونات الإدخال
    name_input = ft.TextField(label="Name")
    phone_input = ft.TextField(label="Phone")
    email_input = ft.TextField(label="Email")
    wilaya_input = ft.TextField(label="Wilaya")
    address_input = ft.TextField(label="Address")

    # إعداد FilePicker لاختيار الصورة
    def on_file_selected(e):
        nonlocal image_data
        if e.files:
            with open(e.files[0].path, "rb") as f:
                image_data = f.read()
            ft.Toast("Image selected!").show()

    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)

    # زر اختيار الصورة
    def select_image(e):
        file_picker.pick_file(accept=[".png", ".jpg", ".jpeg", ".bmp"])

    # زر الإدخال إلى قاعدة البيانات
    def on_submit_click(e):
        nonlocal image_data
        if not image_data:
            ft.Toast("Please select an image first.").show()
            return

        if save_to_database(name_input.value, phone_input.value, email_input.value, wilaya_input.value, address_input.value, image_data):
            ft.Toast("Data added successfully!").show()
            name_input.value = ""
            phone_input.value = ""
            email_input.value = ""
            wilaya_input.value = ""
            address_input.value = ""
            image_data = None
            page.update()

    # زر البحث
    search_input = ft.TextField(label="Search")
    search_results = ft.DataTable(columns=[
        ft.DataColumn(label=ft.Text("Name")),
        ft.DataColumn(label=ft.Text("Phone")),
        ft.DataColumn(label=ft.Text("Email")),
        ft.DataColumn(label=ft.Text("Wilaya")),
        ft.DataColumn(label=ft.Text("Address"))
    ])

    def on_search_click(e):
        keyword = search_input.value
        results = search_in_database(keyword)
        search_results.rows.clear()
        for row_data in results:
            search_results.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row_data]))
        page.update()

    # تصميم الواجهة
    page.add(
        ft.Column([
            ft.Row([
                name_input,
                phone_input,
                email_input,
                wilaya_input,
                address_input
            ]),
            ft.Row([
                ft.ElevatedButton("Select Image", on_click=select_image),
                ft.ElevatedButton("Submit to DB", on_click=on_submit_click)
            ]),
            ft.Divider(),
            ft.Text("Search Database"),
            search_input,
            ft.ElevatedButton("Search", on_click=on_search_click),
            search_results
        ])
    )

ft.app(target=main)
