import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
ventana = tk.Tk()

# Crear el objeto Notebook y agregarlo a la ventana
sell_panel = ttk.Notebook(ventana)
sell_panel.pack()

# Crear un marco para el Treeview de la solapa "Stock"
stock_frame = tk.Frame(sell_panel)
stock_columns = ("ID", "Nombre", "Cantidad")
stock_tree = ttk.Treeview(stock_frame, columns=stock_columns)
stock_tree.pack()

# Agregar el marco como una solapa del Notebook
sell_panel.add(stock_frame, text='Stock')

# Crear un marco para el Treeview de la solapa "Ventas"
sales_frame = tk.Frame(sell_panel)
sales_columns = ("ID", "Nombre", "Precio")
sales_tree = ttk.Treeview(sales_frame, columns=sales_columns)
sales_tree.pack()

putas_frame=tk.Frame(sell_panel)

# Agregar el marco como una solapa del Notebook
sell_panel.add(putas_frame, text='Putas')
sell_panel.add(sales_frame, text='TRABUCOS')

# Iniciar el bucle principal de la aplicación
ventana.mainloop()