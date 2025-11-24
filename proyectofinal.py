# Copia de seguridad
# submodulo
# Autor: Flores Padilla Ahmed Zaid
# Y Mendez Fiol Yocelin Guadalupe

import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox
from PIL import Image, ImageTk 
from datetime import datetime

# -------------------------
# FUNCIONES
# -------------------------
def abrir_registro_productos():
    reg = tk.Toplevel()
    reg.title("Registro de Productos")
    reg.geometry("400x400")
    reg.resizable(False, False)

    # --- Etiquetas y Campos de Texto ---
    lbl_id = tk.Label(reg, text="ID del Producto:", font=("Arial", 12))
    lbl_id.pack(pady=5)
    txt_id = tk.Entry(reg, font=("Arial", 12))
    txt_id.pack(pady=5)
    lbl_desc = tk.Label(reg, text="Descripción:", font=("Arial", 12))
    lbl_desc.pack(pady=5)
    txt_desc = tk.Entry(reg, font=("Arial", 12))
    txt_desc.pack(pady=5)
    lbl_precio = tk.Label(reg, text="Precio:", font=("Arial", 12))
    lbl_precio.pack(pady=5)
    txt_precio = tk.Entry(reg, font=("Arial", 12))
    txt_precio.pack(pady=5)
    lbl_categoria = tk.Label(reg, text="Categoría:", font=("Arial", 12))
    lbl_categoria.pack(pady=5)
    txt_categoria = tk.Entry(reg, font=("Arial", 12))
    txt_categoria.pack(pady=5)

    # --- Función para guardar ---
    def guardar_producto():
        id_prod = txt_id.get().strip()
        descripcion = txt_desc.get().strip()
        precio = txt_precio.get().strip()
        categoria = txt_categoria.get().strip()
        
        # Validaciones
        if id_prod == "" or descripcion == "" or precio == "" or categoria == "":
            messagebox.showwarning("Campos Vacíos", "Por favor complete todos los campos.")
            return
        
        # Validar precio como número y formatear a 2 decimales
        try:
            precio_float = float(precio.replace(",", ".")) # Permite usar coma como decimal
            precio_guardar = f"{precio_float:.2f}"
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        # Guardar en archivo de texto
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            archivo_path = os.path.join(BASE_DIR, "productos.txt")
            
            with open(archivo_path, "a", encoding="utf-8") as archivo:
                archivo.write(f"{id_prod}|{descripcion}|{precio_guardar}|{categoria}\n")
                messagebox.showinfo("Guardado", "Producto registrado correctamente.")
                
                # Limpiar campos
                txt_id.delete(0, tk.END)
                txt_desc.delete(0, tk.END)
                txt_precio.delete(0, tk.END)
                txt_categoria.delete(0, tk.END)
        
        except Exception as e:
            messagebox.showerror("Error de Archivo", f"No se pudo guardar el archivo 'productos.txt'. Error: {e}")
            
    # --- Botón Guardar ---
    btn_guardar = ttk.Button(reg, text="Guardar Producto", command=guardar_producto)
    btn_guardar.pack(pady=20)


# MODIFICACIÓN: La función ahora acepta 'logo_img' como argumento
def mostrar_ticket(producto, precio, cantidad, total, logo_img=None):
    ticket = tk.Toplevel() 
    ticket.title("Ticket De Venta")
    ticket.geometry("300x450") # Se amplía un poco para el logo
    ticket.resizable(False, False)
    
    # 🎨 FONDO: Fondo de la ventana del ticket a NEGRO (#000000) para que combine con el logo
    ticket.configure(bg="#000000")

    # Si se proporcionó un logo, lo mostramos
    if logo_img:
        lbl_logo_ticket = tk.Label(ticket, image=logo_img, bg="#000000")
        lbl_logo_ticket.image = logo_img # Mantenemos la referencia
        lbl_logo_ticket.pack(pady=10) # Un poco de padding
        
    # Fecha y hora
    fecha_hora = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p") 

    # Texto Ticket
    texto = (
    "*** PUNTO DE VENTA ***\n"
    "-----------------------\n"
    f"Fecha: {fecha_hora}\n"
    "-----------------------\n"
    f"Producto: {producto}\n"
    f"Precio: ${float(precio):.2f}\n" 
    f"Cantidad: {int(cantidad)}\n" 
    "-----------------------\n"
    f"Total: ${float(total):.2f}\n" 
    "-----------------------\n"
    " ¡ GRACIAS POR SU COMPRA!\n"
    )

    # 🎨 CONFIGURACIÓN: El texto del ticket también a blanco para contraste con el fondo negro
    lbl_ticket = tk.Label(ticket, text=texto, justify="left", font=("consolas", 11), bg="#000000", fg="white")
    lbl_ticket.pack(pady=15)

    btn_cerrar = ttk.Button(ticket, text="Cerrar", command=ticket.destroy) 
    btn_cerrar.pack(pady=20)


def abrir_registro_ventas():
    ven = tk.Toplevel()
    ven.title("Registro de Ventas")
    ven.geometry("420x430")
    ven.resizable(False, False)
    
    # ------------------------------------
    # Cargar productos desde productos.txt
    # ------------------------------------
    productos = {}
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivof = os.path.join(BASE_DIR,"productos.txt")
        with open(archivof, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")
                if len(partes) == 4:
                    idp, desc, precio_str, cat = partes
                    try:
                        productos[desc] = float(precio_str.replace(",", "."))
                    except ValueError:
                        continue 
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo productos.txt. No se pueden registrar ventas.")
        ven.destroy()
        return

    # Lista de nombres de productos
    lista_productos = list(productos.keys())
    
    # ------------------------------------
    # FUNCIONES
    # ------------------------------------
    def calcular_total(*args):
        try:
            cant = float(txt_cantidad.get().replace(",", ".")) 
            precio = float(txt_precio.get().replace(",", ".")) 
            
            if cant <= 0:
                 total = 0.00
            else:
                 total = cant * precio
            
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.insert(0, f"{total:.2f}") 
            txt_total.config(state="readonly")
        except:
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.config(state="readonly")
            
    def actualizar_precio(event):
        prod = cb_producto.get()
        if prod in productos:
            precio = productos[prod]
            txt_precio.config(state="normal")
            txt_precio.delete(0, tk.END)
            txt_precio.insert(0, f"{precio:.2f}") 
            txt_precio.config(state="readonly")
            calcular_total()
            
    def registrar_venta():
        prod = cb_producto.get()
        precio = txt_precio.get()
        cant = txt_cantidad.get()
        total = txt_total.get()

        if prod == "" or precio == "" or cant == "" or total == "":
            messagebox.showwarning("Campos Vacíos", "Todos los campos deben estar completos.")
            return
        
        try:
            precio_float = float(precio.replace(",", "."))
            cant_float = float(cant.replace(",", ".")) 
            total_float = float(total.replace(",", "."))
            
            if cant_float <= 0:
                 messagebox.showwarning("Cantidad Inválida", "La cantidad debe ser un número positivo.")
                 return
            
            if abs(total_float - (precio_float * cant_float)) > 0.01:
                 messagebox.showwarning("Error de Cálculo", "El total calculado parece ser incorrecto.")
                 return
                 
        except ValueError:
             messagebox.showerror("Error de Datos", "Precio, Cantidad o Total contienen valores no numéricos válidos.")
             return
             
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivov = os.path.join(BASE_DIR, "ventas.txt")
        
        with open(archivov, "a", encoding="utf-8") as archivo:
            archivo.write(f"{prod}|{precio}|{cant}|{total}\n")
            
        
        
        # MODIFICACIÓN: Pasamos el logo a la función mostrar_ticket
        # Usamos 'ventana.logo_img' que se cargó globalmente en la ventana principal.
        mostrar_ticket(prod, precio_float, cant_float, total_float, logo_img=ventana.logo_img) 
        
        # Limpiar campos
        cb_producto.set("")
        txt_precio.config(state="normal"); txt_precio.delete(0, tk.END); txt_precio.config(state="readonly")
        txt_cantidad.delete(0, tk.END)
        txt_total.config(state="normal"); txt_total.delete(0, tk.END); txt_total.config(state="readonly")
        
    # ------------------------------------
    # CONTROLES VISUALES
    # ------------------------------------
    main_frame = tk.Frame(ven)
    main_frame.pack(padx=10, pady=10, fill="x") 
    
    lbl_prod = tk.Label(main_frame, text="Producto:", font=("Arial", 12))
    lbl_prod.pack(pady=5)
    cb_producto = ttk.Combobox(main_frame, values=lista_productos, font=("Arial", 12), state="readonly", width=30)
    cb_producto.pack(pady=5)
    
    lbl_precio = tk.Label(main_frame, text="Precio:", font=("Arial", 12))
    lbl_precio.pack(pady=5)
    txt_precio = tk.Entry(main_frame, font=("Arial", 12), state="readonly", width=30)
    txt_precio.pack(pady=5)
    
    lbl_cantidad = tk.Label(main_frame, text="Cantidad:", font=("Arial", 12))
    lbl_cantidad.pack(pady=5)
    cantidad_var = tk.StringVar(ven)
    ven.cantidad_var = cantidad_var 
    txt_cantidad = tk.Entry(main_frame, font=("Arial", 12), textvariable=cantidad_var, width=30)
    txt_cantidad.pack(pady=5) 
    
    cantidad_var.trace_add("write", calcular_total)
    
    lbl_total = tk.Label(main_frame, text="Total:", font=("Arial", 12))
    lbl_total.pack(pady=5)
    txt_total = tk.Entry(main_frame, font=("Arial", 12), state="readonly", width=30)
    txt_total.pack(pady=5)
    
    cb_producto.bind("<<ComboboxSelected>>", actualizar_precio)
    btn_guardar = ttk.Button(main_frame, text="Registrar Venta", command=registrar_venta)
    btn_guardar.pack(pady=25)


def abrir_reportes():
    messagebox.showinfo("Reportes", "Aquí irá el módulo de reportes.")

def abrir_acerca_de():
    messagebox.showinfo("Acerca de", "Distribuidora - Flores-Gan\nProyecto Escolar\nVersión 1.0")

# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Distribuidora - Flores-Gan")
ventana.geometry("500x600")
ventana.resizable(False, False)
ventana.configure(bg="#000000") 


# -------------------------
# LOGO (carga del logo para la ventana principal y para el ticket)
# -------------------------
# Se añade una variable para almacenar el logo, accesible globalmente o como atributo de ventana
ventana.logo_img = None 
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "ventas2025.png")
    
    imagen = Image.open(logo_path) 
    imagen = imagen.resize((150, 150)) # Se reduce el tamaño del logo para que encaje mejor en el ticket
    ventana.logo_img = ImageTk.PhotoImage(imagen) # Guarda la referencia en el atributo de la ventana

    lbl_logo = tk.Label(ventana, image=ventana.logo_img, bg="#000000") 
    lbl_logo.pack(pady=20)
    
    # La referencia ya está guardada en ventana.logo_img
    
except Exception as e: 
    lbl_sin_logo = tk.Label(ventana, text="(Aquí va el logo del sistema)", font=("Arial", 14), bg="#000000", fg="white")
    lbl_sin_logo.pack(pady=40)
    print(f"Error al cargar el logo: {e}") 


# -------------------------
# BOTONES PRINCIPALES
# -------------------------
estilo = ttk.Style()
estilo.configure("TButton", 
                 font=("Arial", 12, "bold"), 
                 padding=10,
                 width=25, 
                 background="white", 
                 foreground="black", 
                 relief="flat") 

estilo.map('TButton', background=[('active', '#dddddd')]) 


btn_reg_prod = ttk.Button(ventana, text="Registro de Productos", command=abrir_registro_productos)
btn_reg_prod.pack(pady=10)

btn_reg_ventas = ttk.Button(ventana, text="Registro de Ventas", command=abrir_registro_ventas)
btn_reg_ventas.pack(pady=10)

btn_reportes = ttk.Button(ventana, text="Reportes", command=abrir_reportes)
btn_reportes.pack(pady=10)

btn_acerca = ttk.Button(ventana, text="Acerca de", command=abrir_acerca_de)
btn_acerca.pack(pady=10)


ventana.mainloop()