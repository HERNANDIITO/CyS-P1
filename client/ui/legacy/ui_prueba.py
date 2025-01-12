from customtkinter import *
from CTkTable import CTkTable
#from functions import aesrsa

# set_appearance_mode("dark")
ruta_archivo = None

def seleccionar_archivo():
    global ruta_archivo
    ruta_archivo = filedialog.askopenfilename(title="Selecciona un archivo")
    
    if ruta_archivo:
        estado.configure(text=f"Archivo seleccionado: {ruta_archivo}")
    else:
        estado.configure(text="No se seleccionó ningún archivo")

def handle_order_id_click(order_id):
    print(f"Order ID clicked: {order_id}")

def handle_item_name_click(item_name):
    print(f"Item Name clicked: {item_name}")

def handle_customer_click(customer):
    print(f"Customer clicked: {customer}")

def cell_click(event):
    # Get the clicked cell's row and column
    row, column = table.get_row_column(event.x, event.y)
    if row >= 0 and column >= 0:  # Check if a valid cell is clicked
        # Get the value of the clicked cell
        cell_value = table.get_value_at(row, column)
        
        # Call different functions based on the column
        if column == 0:  # Order ID
            handle_order_id_click(cell_value)
        elif column == 1:  # Item Name
            handle_item_name_click(cell_value)
        elif column == 2:  # Customer
            handle_customer_click(cell_value)

def ui_prueba(app):
    title = CTkLabel(master=app, text="Asegurados304", font=("Arial", 24))
    subtitle = CTkLabel(master=app, text="Tu software favorito para proteger todos tus archivos multimedia")
    btn_selec_archivo = CTkButton(master=app, text="Seleccionar archivo", corner_radius=32, fg_color="#009DDC", text_color="#ffffff", command=seleccionar_archivo)
    btn_cifrar = CTkButton(master=app, text="Cifrar archivo", corner_radius=32, fg_color="#009DDC", text_color="#ffffff")
    estado = CTkLabel(master=app, text="No se ha seleccionado ningún archivo.")

    table_data = [
        ["Order ID", "Item Name", "Customer", "Address", "Status", "Quantity"],
        ['3833', 'Smartphone', 'Alice', '123 Main St', 'Confirmed', '8'],
        ['6432', 'Laptop', 'Bob', '456 Elm St', 'Packing', '5'],
        ['2180', 'Tablet', 'Crystal', '789 Oak St', 'Delivered', '1'],
        ['5438', 'Headphones', 'John', '101 Pine St', 'Confirmed', '9'],
        ['9144', 'Camera', 'David', '202 Cedar St', 'Processing', '2'],
        ['7689', 'Printer', 'Alice', '303 Maple St', 'Cancelled', '2'],
        ['1323', 'Smartwatch', 'Crystal', '404 Birch St', 'Shipping', '6'],
        ['7391', 'Keyboard', 'John', '505 Redwood St', 'Cancelled', '10'],
        ['4915', 'Monitor', 'Alice', '606 Fir St', 'Shipping', '6'],
        ['5548', 'External Hard Drive', 'David', '707 Oak St', 'Delivered', '10'],
        ['5485', 'Table Lamp', 'Crystal', '808 Pine St', 'Confirmed', '4'],
        ['7764', 'Desk Chair', 'Bob', '909 Cedar St', 'Processing', '9'],
        ['8252', 'Coffee Maker', 'John', '1010 Elm St', 'Confirmed', '6'],
        ['2377', 'Blender', 'David', '1111 Redwood St', 'Shipping', '2'],
        ['5287', 'Toaster', 'Alice', '1212 Maple St', 'Processing', '1'],
        ['7739', 'Microwave', 'Crystal', '1313 Cedar St', 'Confirmed', '8'],
        ['3129', 'Refrigerator', 'John', '1414 Oak St', 'Processing', '5'],
        ['4789', 'Vacuum Cleaner', 'Bob', '1515 Pine St', 'Cancelled', '10']
    ]

    table_frame = CTkScrollableFrame(master=app, fg_color="transparent")
    table_frame.pack(expand=True, fill="both", padx=27, pady=21)
    table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4")
    table.edit_row(0, text_color="#fff", hover_color="#2A8C55")


    title.pack(pady=20)
    subtitle.pack(pady=0)
    btn_selec_archivo.pack(pady=20) 
    btn_cifrar.pack(pady=20) 
    estado.pack(pady=0)
    table.pack(expand=True)

    table.bind("<Button-1>", cell_click)