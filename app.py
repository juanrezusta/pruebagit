import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime
import sqlite3

conn=sqlite3.connect("database.db")
c=conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            lastname TEXT,
            email TEXT,
            phone TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS products (
            item_id_sql INTEGER PRIMARY KEY AUTOINCREMENT ,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            color TEXT NOT NULL ,
            size TEXT NOT NULL,
            value INTEGER NOT NULL     
)''')

c.execute('''CREATE TABLE IF NOT EXISTS orders (
            order_id_sql INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            total_items_in_sell INTEGER NOT NULL,
            total_amount_sell INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)''')

c.execute('''CREATE TABLE IF NOT EXISTS orderdetails(
            orderdetail_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id_sql INTEGER,
            item_id_sql INTEGER,
            quantity INTEGER,
            total_item_value INTEGER,
            FOREIGN KEY (order_id_sql) REFERENCES orders(order_id_sql),
            FOREIGN KEY (item_id_sql) REFERENCES products(item_id_sql)
)''')


main_window = tk.Tk()
main_window.title("SEVENSINS")
main_window.geometry("800x600")  # Ancho x Alto
main_window.resizable(False, False)
main_window.configure(bg="white")

icono = tk.PhotoImage(file='sevensins_logo.png')

# Establece el icono en la ventana
main_window.iconphoto(True, icono)

def erase_item():
    selected_items = stock_table.selection()
        
    if selected_items:
        for item in selected_items:
            item_id = stock_table.item(item)['values'][0]
            c.execute('''DELETE FROM products WHERE item_id_sql=?''', (item_id,))
            conn.commit()
            stock_table.delete(item)

        charge_data()
        refresh_count_label()
        refresh_totalstocklabel()   
    else:
        print("Ningún elemento seleccionado para eliminar.")


def erase_order():
    selected_items = orders_table.selection()
        
    if selected_items:
        for item in selected_items:
            item_id = orders_table.item(item)['values'][0]
            c.execute('''DELETE FROM orders WHERE order_id_sql=?''', (item_id,))
            c.execute('''DELETE FROM orderdetails WHERE order_id_sql=?''',(item_id,))
            conn.commit()
            orders_table.delete(item)

        charge_data()
        refresh_count_label()
        refresh_totalstocklabel()   
    else:
        print("Ningún elemento seleccionado para eliminar.")

#,table_in_sql,where,whereawnser

    



def charge_data():
    stock_table.delete(*stock_table.get_children())
    c.execute('SELECT * FROM products order by name')
    previous_data_stock=c.fetchall()    
    
    for item in previous_data_stock:
        usableitem=item[0:]
        stock_table.insert("","end",values=usableitem)

    customers_table.delete(*customers_table.get_children())
    c.execute('SELECT * FROM customers order by firstname')
    previous_data_customers=c.fetchall()

    for item in previous_data_customers:
        customersdata=item[0:]
        customers_table.insert("","end",values=customersdata)

    orders_table.delete(*orders_table.get_children())
    c.execute('SELECT * FROM orders')
    previous_data_orders=c.fetchall()

    for item in previous_data_orders:
        orderdata=item[0:]
        orders_table.insert("","end",values=orderdata)


    orderdetails_table.delete(*orderdetails_table.get_children())
    c.execute('SELECT * FROM orderdetails')
    previous_data_orders=c.fetchall()

    for item in previous_data_orders:
        orderdata=item[0:]
        orderdetails_table.insert("","end",values=orderdata)
    
    refresh_count_label()
    refresh_totalstocklabel()



def count_items_sql():
    c.execute('''SELECT COUNT(item_id_sql) from products''')
    quantity_items_stock=c.fetchone()[0]
    
    return quantity_items_stock

def refresh_count_label():
    total=count_items_sql()

    total_label.config(text=f"Items en stock: {total}")
    
def count_total_quantity_sql():
    c.execute('''SELECT SUM(quantity) FROM products''')
    result = c.fetchone()
    if result and result[0] is not None:
        quantity_totalstock = result[0]
        return quantity_totalstock
    else:
        return 0

def refresh_totalstocklabel():
    total=round(count_total_quantity_sql())
    total_quantitylabel.config(text=f"Stock total: {total}")

def erase_customer():
    selected_items = customers_table.selection()
    
    if selected_items:
        for item in selected_items:
            customers_table.item(item, tags=[])  # Eliminar todas las etiquetas
            
            item_id = customers_table.item(item, "values")[0]
            if item_id is not None:
                c.execute('''DELETE FROM customers WHERE customer_id=?''', (item_id,))
                conn.commit()
                customers_table.delete(item)
            else:
                print("No se pudo eliminar el cliente: ID no válido.")
                
        charge_data()
        refresh_count_label()
        refresh_totalstocklabel()   
    else:
        print("Ningún elemento seleccionado para eliminar.")

#HERE THE VISUAL ELEMENTS FOR THE TREEVIEW
main_notebook = ttk.Notebook(main_window)
main_notebook.pack(fill="both", expand=True)

stock_treeframe = ttk.Frame(main_notebook)
main_notebook.add(stock_treeframe, text="Stock")

orders_treeframe = ttk.Frame(main_notebook)
main_notebook.add(orders_treeframe, text="Ventas")

orderdetails_treeframe=ttk.Frame(main_notebook)
main_notebook.add(orderdetails_treeframe,text="Detalles")

customers_treeframe=ttk.Frame(main_notebook)
main_notebook.add(customers_treeframe,text="Clientes")


buttons_table_frame = ttk.Frame(stock_treeframe)
buttons_table_frame.place(x=200, y=200)

buttons_sell_frame= ttk.Frame(orders_treeframe)
buttons_sell_frame.place(x=200,y=200)

buttons_orderdetails_frame=ttk.Frame(orderdetails_treeframe)
buttons_orderdetails_frame.place(x=200,y=200)

buttons_customers_frame=ttk.Frame(customers_treeframe)
buttons_customers_frame.place(x=200,y=200)



#Labels de la stock_table
total_label = tk.Label(stock_treeframe, text="Total de Items en Stock:")
total_label.place(x=10,y=540)
total_label.config(background="#E3DED8")


total_quantitylabel=tk.Label(stock_treeframe,text="Total de products en stock:")
total_quantitylabel.place(x=245,y=540)
total_quantitylabel.config(background="#E3DED8")



#--------------------------------------------------------------ESTRUCTURA--------------------------------------------
stock_table = ttk.Treeview(stock_treeframe, columns=("item_id_sql","Item", "cantidad", "color", "talle", "precio"), show="headings")
stock_table.heading("item_id_sql",text="ID",anchor="center",command=lambda:ordenar_columna(1,stock_table))
stock_table.heading("Item", text="Producto",anchor="center", command=lambda: ordenar_columna(2,stock_table))
stock_table.heading("cantidad", text="Cantidad",anchor="center", command=lambda: ordenar_columna(3,stock_table))
stock_table.heading("color",text="Color",anchor="center", command=lambda: ordenar_columna(4,stock_table))
stock_table.heading("talle",text="Talle",anchor="center", command=lambda: ordenar_columna(5,stock_table))
stock_table.heading("precio",text="Precio",anchor="center", command=lambda: ordenar_columna(6,stock_table))

stock_table.column("item_id_sql", width=30, minwidth=220, stretch="NO",anchor="w")
stock_table.column("Item", width=220, minwidth=220, stretch="NO",anchor="w")
stock_table.column("cantidad", width=139, minwidth=139, stretch="NO",anchor="center")
stock_table.column("color", width=139, minwidth=139, stretch="NO",anchor="center")
stock_table.column("talle", width=139, minwidth=140, stretch="NO",anchor="center")
stock_table.column("precio", width=110, minwidth=140, stretch="NO",anchor="center")


stock_table.place(x=10,y=80,width=780,height=450)


orders_table= ttk.Treeview(orders_treeframe, columns=("order_id_sql","customer_id","customer_name","total_items_in_sell","total_amount_sell","order_date"), show="headings")
orders_table.heading("order_id_sql",text="Orden",anchor="center",command=lambda: ordenar_columna(0,orders_table))
orders_table.heading("customer_id",text="Cliente",anchor="center",command=lambda: ordenar_columna(1,orders_table))
orders_table.heading("customer_name",text="Nombre de Cliente",anchor="center",command=lambda:ordenar_columna(2,orders_table))
orders_table.heading("total_items_in_sell",text="Bultos",anchor="center",command=lambda: ordenar_columna(3,orders_table))
orders_table.heading("total_amount_sell",text="Monto Total",anchor="center",command=lambda: ordenar_columna(4,orders_table))
orders_table.heading("order_date",text="Fecha",anchor="center",command=lambda: ordenar_columna(5,orders_table))


orders_table.column("order_id_sql", width=50, minwidth=220, stretch="NO",anchor="center")
orders_table.column("customer_id", width=50, minwidth=139, stretch="NO",anchor="center")
orders_table.column("customer_name",width=239, minwidth=140, stretch="NO",anchor="center")
orders_table.column("total_items_in_sell", width=50, minwidth=140, stretch="NO",anchor="center")
orders_table.column("total_amount_sell", width=199, minwidth=140, stretch="NO",anchor="center")
orders_table.column("order_date", width=189, minwidth=140, stretch="NO",anchor="center")




orders_table.place(x=10,y=80,width=780,height=450)

orderdetails_table=ttk.Treeview(orderdetails_treeframe,columns=("orderdetail_id","order_id_sql","item_id_sql","quantity","total_item_value"), show="headings")
orderdetails_table.heading("orderdetail_id", text="ID",anchor="center", command=lambda: ordenar_columna(0,orderdetails_table))
orderdetails_table.heading("order_id_sql", text="Orden",anchor="center", command=lambda: ordenar_columna(1,orderdetails_table))
orderdetails_table.heading("item_id_sql",text="Producto",anchor="center", command=lambda: ordenar_columna(2,orderdetails_table))
orderdetails_table.heading("quantity",text="Cantidad",anchor="center", command=lambda: ordenar_columna(3,orderdetails_table))
orderdetails_table.heading("total_item_value",text="Valor Item",anchor="center", command=lambda: ordenar_columna(4,orderdetails_table))


orderdetails_table.column("orderdetail_id", width=30, minwidth=220, stretch="NO",anchor="w")
orderdetails_table.column("order_id_sql", width=57, minwidth=139, stretch="NO",anchor="center")
orderdetails_table.column("item_id_sql", width=230, minwidth=139, stretch="NO",anchor="center")
orderdetails_table.column("quantity", width=230, minwidth=140, stretch="NO",anchor="center")
orderdetails_table.column("total_item_value", width=230, minwidth=140, stretch="NO",anchor="center")

orderdetails_table.place(x=10,y=80,width=780,height=450)



customers_table=ttk.Treeview(customers_treeframe,columns=("customer_id","firstname","lastname","email","phone"), show="headings")
customers_table.heading("#1", text="ID",anchor="center", command=lambda: ordenar_columna(0,customers_table))
customers_table.heading("#2", text="Nombre",anchor="center", command=lambda: ordenar_columna(1,customers_table))
customers_table.heading("#3",text="Apellido",anchor="center", command=lambda: ordenar_columna(2,customers_table))
customers_table.heading("#4",text="Email",anchor="center", command=lambda: ordenar_columna(3,customers_table))
customers_table.heading("#5",text="Teléfono",anchor="center", command=lambda: ordenar_columna(4,customers_table))


customers_table.column("#1", width=30, minwidth=220, stretch="NO",anchor="center")
customers_table.column("#2", width=200, minwidth=139, stretch="NO",anchor="center")
customers_table.column("#3", width=200, minwidth=139, stretch="NO",anchor="center")
customers_table.column("#4", width=208, minwidth=140, stretch="NO",anchor="center")
customers_table.column("#5", width=139, minwidth=140, stretch="NO",anchor="center")

customers_table.place(x=10,y=80,width=780,height=450)




#HERE IS THE APP VISUAL ELEMENTS FOR THE NEW ITEM WINDOW   
def newitem_window():
    
    x=main_window.winfo_x()
    y=main_window.winfo_y()
    newitem_window=tk.Toplevel(main_window)
    newitem_window.title("Agregue producto")
    newitem_window.geometry(f"400x400+{x+100}+{y+100}")
    newitem_window.grab_set()
    newitem_window.resizable(False, False)
    newitem_window.attributes("-topmost",True)
    newitem_window.lift()
    
       
        
    def send_info():
        name = entry_item.get().capitalize()
        quantity = entry_cantidad.get()
        color = entry_color.get()
        size = combo_talle.get()
        value = entry_precio.get()

        
        c.execute('''INSERT INTO products (name, quantity, color, size, value) VALUES (?, ?, ?, ?, ?)''', (name, quantity, color, size, value))
        conn.commit()

        
        
        newitem_window.destroy()
        charge_data()     

    label_item=ttk.Label(newitem_window,text="Item:")
    label_item.place(x=10,y=10)

    entry_item=ttk.Entry(newitem_window)
    entry_item.place(x=100,y=10,width=200,height=25)

    label_cantidad=ttk.Label(newitem_window,text="Cantidad:")
    label_cantidad.place(x=10,y=60)

    entry_cantidad=ttk.Entry(newitem_window)
    entry_cantidad.place(x=100,y=60,width=200,height=25)


    label_color=ttk.Label(newitem_window,text="Color:")
    label_color.place(x=10,y=110)

    entry_color=ttk.Entry(newitem_window)
    entry_color.place(x=100,y=110,width=200,height=25)


    
    label_talle=ttk.Label(newitem_window,text="Talle:")
    label_talle.place(x=10,y=160)

    combo_talle=ttk.Combobox(newitem_window,values=["XXS","XS","S","M","L","XL","XXL","XXXL"])
    combo_talle.place(x=100,y=160)

    label_precio=ttk.Label(newitem_window,text="Precio:")
    label_precio.place(x=10,y=210)

    entry_precio=ttk.Entry(newitem_window)
    entry_precio.place(x=100,y=210,width=200,height=25)

    newitem_button=ttk.Button(newitem_window ,text="Confirmar ingreso")
    newitem_button.place(x=100,y=250,width=200,height=25)
    newitem_button.config(command=send_info)
    newitem_button.focus_set()



def newcustomer_window():
    x=main_window.winfo_x()
    y=main_window.winfo_y()
    newcustomer_window=tk.Toplevel(main_window)
    newcustomer_window.title("Agregue Cliente Nuevo")
    newcustomer_window.geometry(f"400x400+{x+100}+{y+100}")
    newcustomer_window.grab_set()
    newcustomer_window.resizable(False, False)
    newcustomer_window.attributes("-topmost",True)
    newcustomer_window.lift()
    
    def send_info_customers():
        firstname = entry_firstname.get().capitalize()
        lastname = entry_lastname.get()
        email = entry_email.get()
        phone = entry_telefono.get()
        
        # Insertar en la base de datos sin proporcionar el valor de item_id
        c.execute('''INSERT INTO customers (firstname, lastname, email, phone) VALUES (?, ?, ?, ?)''', (firstname, lastname, email, phone))
        conn.commit()
        
        
        newcustomer_window.destroy()
        charge_data()  

    label_firstname=ttk.Label(newcustomer_window,text="Nombre:")
    label_firstname.place(x=10,y=10)

    entry_firstname=ttk.Entry(newcustomer_window)
    entry_firstname.place(x=100,y=10,width=200,height=25)

    label_lastname=ttk.Label(newcustomer_window,text="Apellido:")
    label_lastname.place(x=10,y=60)

    entry_lastname=ttk.Entry(newcustomer_window)
    entry_lastname.place(x=100,y=60,width=200,height=25)


    label_email=ttk.Label(newcustomer_window,text="Email:")
    label_email.place(x=10,y=110)

    entry_email=ttk.Entry(newcustomer_window)
    entry_email.place(x=100,y=110,width=200,height=25)


    
    label_phone=ttk.Label(newcustomer_window,text="Telefono:")
    label_phone.place(x=10,y=160)

    entry_telefono=ttk.Entry(newcustomer_window)
    entry_telefono.place(x=100,y=160)

    

    newitem_button=ttk.Button(newcustomer_window ,text="Confirmar ingreso")
    newitem_button.place(x=100,y=250,width=200,height=25)
    newitem_button.config(command=send_info_customers)
    newitem_button.focus_set()




def neworder_window():
    query_products=c.execute('''SELECT name FROM PRODUCTS order by name''')
    query_products_fetch=query_products.fetchall()
    product_names = [row[0] for row in query_products_fetch]
    
    query_customers=c.execute('SELECT firstname,lastname from customers order by firstname ')
    query_customers_fetch=query_customers.fetchall()
    
    
    customer_names=[f"{firstname} {lastname}" for firstname,lastname in query_customers_fetch]
    x=main_window.winfo_x()
    y=main_window.winfo_y()
    neworder_window=tk.Toplevel(main_window)
    neworder_window.title("Agregue Orden")
    neworder_window.geometry(f"400x400+{x+100}+{y+100}")
    neworder_window.grab_set()    
    neworder_window.resizable(False, False)
    neworder_window.attributes("-topmost",True)
    neworder_window.lift()
    #AGREGO COMENTARIO
    #OTRO COMENTARIO SAPE   
    "OTRO PARA GIT"

    def send_orderinfo():
        
        customer_fullname = combo_customer_in_orders.get().capitalize()
        customer_firstname = customer_fullname.split()[0]
        c.execute("SELECT customer_id FROM customers WHERE firstname = ?", (customer_firstname,))
        result_customer_id = c.fetchone()
        finalresult_id=result_customer_id[0]
        
        product_combo1, product_combo2, product_combo3 = combo_product_in_orders1.get(),combo_product_in_orders2.get(),combo_product_in_orders3.get()
        quantity_spin1_str,quantity_spin2_str,quantity_spin3_str=spinbox_combo1.get(),spinbox_combo2.get(),spinbox_combo3.get()
        quantity_spin1_int,quantity_spin2_int,quantity_spin3_int=int(quantity_spin1_str),int(quantity_spin2_str),int(quantity_spin3_str)
        total_items_in_sell=quantity_spin1_int+quantity_spin2_int+quantity_spin3_int
        actual_date=datetime.now()
        formatted_date=actual_date.strftime("%d-%m-%Y %H:%M:%S")        

        total_amount=0
        c.execute("INSERT INTO Orders (customer_id,customer_name,total_items_in_sell,total_amount_sell,order_date) values(?,?,?,?,?)",(finalresult_id,customer_fullname,total_items_in_sell,total_amount,formatted_date))
        last_inserted_id_orders = c.lastrowid
        
        #----sacando lo seleccionado--->
        if product_combo1 != "---Elija producto---":
            c.execute('''SELECT item_id_sql from products where name =?''',(product_combo1,))
            chosen_product1=c.fetchall()
            if chosen_product1:
                chosen_product1=chosen_product1[0][0]        
                c.execute('''SELECT value FROM products where item_id_sql=?''',(chosen_product1,))
                chosen_product1_value=c.fetchall()
                chosen_product1_value=int(chosen_product1_value[0][0])
                total_item_value1=(chosen_product1_value*quantity_spin1_int)
                total_amount+=total_item_value1
                c.execute('''INSERT INTO orderdetails (order_id_sql,item_id_sql,quantity,total_item_value) values (?,?,?,?)''',(last_inserted_id_orders,product_combo1,quantity_spin1_int,total_item_value1))
                
                c.execute('''UPDATE products SET quantity = quantity - ? WHERE item_id_sql = ?''',(quantity_spin1_int,chosen_product1))
                
            else:
                print("No se encontraron resultados para el producto 1")
        else:
            print("NO HAY PRIMER ITEM")
                
                
        if product_combo2 != "---Elija producto---":
            c.execute('''SELECT item_id_sql from products where name = ?''', (product_combo2,))
            chosen_product2 = c.fetchall()
            if chosen_product2:
                chosen_product2 = chosen_product2[0][0]
                c.execute('''SELECT value FROM products where item_id_sql=?''',(chosen_product2,))
                chosen_product2_value=c.fetchall()
                chosen_product2_value=int(chosen_product2_value[0][0])
                total_item_value2=(chosen_product2_value*quantity_spin2_int)
                total_amount+=total_item_value2
                c.execute('''INSERT INTO orderdetails (order_id_sql,item_id_sql,quantity,total_item_value) values (?,?,?,?)''',(last_inserted_id_orders,product_combo2,quantity_spin2_int,total_item_value2))
                
                c.execute('''UPDATE products SET quantity = quantity - ? WHERE item_id_sql = ?''',(quantity_spin2_int,chosen_product2))
                           
            else:
                print("No se encontraron resultados para el producto 2")
        else:
            print("NO HAY SEGUNDO ITEM")


        if product_combo3 != "---Elija producto---":
            c.execute('''SELECT item_id_sql from products where name = ?''', (product_combo3,))
            chosen_product3 = c.fetchall()
            if chosen_product3:
                chosen_product3 = chosen_product3[0][0]
                c.execute('''SELECT value FROM products where item_id_sql=?''',(chosen_product3,))
                chosen_product3_value=c.fetchall()
                chosen_product3_value=int(chosen_product3_value[0][0])
                total_item_value3=(chosen_product3_value*quantity_spin3_int)
                total_amount+=total_item_value3
                c.execute('''INSERT INTO orderdetails (order_id_sql,item_id_sql,quantity,total_item_value) values (?,?,?,?)''',(last_inserted_id_orders,product_combo3,quantity_spin3_int,total_item_value3))
                
                c.execute('''UPDATE products SET quantity = quantity - ? WHERE item_id_sql = ?''',(quantity_spin3_int,chosen_product3))
                
            else:
                print("No se encontraron resultados para el producto 3")
        else:
            print("NO HAY TERCER ITEM")


        c.execute("UPDATE Orders SET total_amount_sell = ? WHERE order_id_sql = ?", (total_amount, last_inserted_id_orders))
        

        conn.commit()
        # treeview_insert(orders_table,(last_inserted_id_orders,finalresult_id,str(total_items_in_sell),formatted_date))
        neworder_window.destroy()
        charge_data()  



    label_customer=ttk.Label(neworder_window,text="Cliente:")
    label_customer.place(x=10,y=10)

    combo_customer_in_orders=ttk.Combobox(neworder_window,values=customer_names)
    combo_customer_in_orders.place(x=100,y=10,width=200,height=25)
    combo_customer_in_orders.set("---Elija un cliente---")


    label_product=ttk.Label(neworder_window,text="Productos:")
    label_product.place(x=10,y=60)

    combo_product_in_orders1=ttk.Combobox(neworder_window,values=product_names)
    combo_product_in_orders1.place(x=100,y=60,width=200,height=25)
    combo_product_in_orders1.set("---Elija producto---")

    spinbox_combo1 = ttk.Spinbox(neworder_window, from_=0, to=100)
    spinbox_combo1.place(x=350,y=60,width=35,height=25)
    spinbox_combo1.set(0)

    combo_product_in_orders2=ttk.Combobox(neworder_window,values=product_names)
    combo_product_in_orders2.place(x=100,y=110,width=200,height=25)
    combo_product_in_orders2.set("---Elija producto---")

    spinbox_combo2 = ttk.Spinbox(neworder_window, from_=0, to=100)
    spinbox_combo2.place(x=350,y=110,width=35,height=25)
    spinbox_combo2.set(0)
    
    combo_product_in_orders3=ttk.Combobox(neworder_window,values=product_names)
    combo_product_in_orders3.place(x=100,y=160,width=200,height=25)
    combo_product_in_orders3.set("---Elija producto----")

    spinbox_combo3 = ttk.Spinbox(neworder_window, from_=0, to=100)
    spinbox_combo3.place(x=350,y=160,width=35,height=25)
    spinbox_combo3.set(0)
    

    newitem_button=ttk.Button(neworder_window ,text="Confirmar ingreso")
    newitem_button.place(x=100,y=250,width=200,height=25)
    newitem_button.config(command=send_orderinfo)
    newitem_button.focus_set()


def ordenar_columna(columna,tabla, reverse=False):
    contenido = [(tabla.set(i, columna), i) for i in tabla.get_children('')]
    contenido.sort(key=lambda x: x[0], reverse=reverse)
    for index, item in enumerate(contenido):
        tabla.move(item[1], '', index)
    tabla.heading(columna, command=lambda: ordenar_columna(columna, not reverse))

 
 
def treeview_insert(treeview,tuple_data):
    treeview.insert("", "end", values=tuple_data)

 
 
class create_button:
    def __init__(self,where,text,function,x,y):
        self.button=ttk.Button(where,text=text)
        self.button.place(x=x,y=y,width=120,height=30)
        self.button.config(command=function)

def modify_item(): 
    selected_items=stock_table.selection()

    if selected_items:
        for item in selected_items:
            item_id= stock_table.item(item)['values'][2]
            print(item_id)


newitem_button=create_button(stock_treeframe,"Ingresar Producto",newitem_window,40,40)
modifyitem_button=create_button(stock_treeframe,"Modificar Item",modify_item,480,40)
erase_button=create_button(stock_treeframe,"Eliminar Producto",erase_item,650,40)



new_customer_button=create_button(customers_treeframe,"Nuevo Cliente",newcustomer_window,40,40)
modifycustomer_button=create_button(customers_treeframe,"Modificar Cliente","modify_customer",480,40)
del_customer_button=create_button(customers_treeframe,"Eliminar Cliente",erase_customer,650,40)

new_order_button=create_button(orders_treeframe,"Nueva Venta",neworder_window,40,40)
erase_order_button=create_button(orders_treeframe,"Eliminar Orden",erase_order,640,40)



charge_data()

style=ttk.Style(main_window)
style.theme_use("clam")

main_window.mainloop()