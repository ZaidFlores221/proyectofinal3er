#Copia de seguridad
#submodulo
#Autor: Flores Padilla Ahmed Zaid
# Y Mendez Fiol Yocelin Guadalupe

import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox
from PIL import Image, ImageTk 

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
                        # Almacenar el precio como float para cálculos
                        productos[desc] = float(precio_str.replace(",", "."))
                    except ValueError:
                        # Si el precio no es un número, se ignora el producto o se alerta
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
            # Sanitizar entrada: permitir coma como separador decimal, luego convertir a float, y a int para cantidad
            cant = int(float(txt_cantidad.get().replace(",", "."))) 
            precio = float(txt_precio.get().replace(",", ".")) 
            
            if cant <= 0:
                 raise ValueError("Cantidad no positiva")
                 
            total = cant * precio
            
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            # Mostrar el total con dos decimales
            txt_total.insert(0, f"{total:.2f}") 
            txt_total.config(state="readonly")
        except:
            # Si no hay número válido en cantidad o precio, limpiar el total
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.config(state="readonly")
            
    def actualizar_precio(event):
        prod = cb_producto.get()
        if prod in productos:
            precio = productos[prod]
            txt_precio.config(state="normal")
            txt_precio.delete(0, tk.END)
            # Mostrar el precio con dos decimales
            txt_precio.insert(0, f"{precio:.2f}") 
            txt_precio.config(state="readonly")
            calcular_total()
            
    def registrar_venta():
        prod = cb_producto.get()
        precio = txt_precio.get()
        cant = txt_cantidad.get()
        total = txt_total.get()

        # Validaciones de campos vacíos
        if prod == "" or precio == "" or cant == "" or total == "":
            messagebox.showwarning("Campos Vacíos", "Todos los campos deben estar completos.")
            return
        
        # Validaciones de números y lógica (opcional pero recomendado)
        try:
            precio_float = float(precio.replace(",", "."))
            cant_int = int(float(cant.replace(",", ".")))
            total_float = float(total.replace(",", "."))
            
            if cant_int <= 0:
                 messagebox.showwarning("Cantidad Inválida", "La cantidad debe ser un número entero positivo.")
                 return
            
            # Revalidar que el total calculado sea correcto (opcional para seguridad)
            if abs(total_float - (precio_float * cant_int)) > 0.01:
                 messagebox.showwarning("Error de Cálculo", "El total calculado parece ser incorrecto.")
                 # Se puede preguntar si desea guardar de todas formas o forzar el cálculo
                 # Por ahora, seguiremos, asumiendo que el usuario confía en el cálculo mostrado.
                 
        except ValueError:
             messagebox.showerror("Error de Datos", "Precio, Cantidad o Total contienen valores no numéricos válidos.")
             return
             
        # Guardar venta
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivov = os.path.join(BASE_DIR, "ventas.txt")
        
        # Usamos la ruta completa y segura (archivov)
        with open(archivov, "a", encoding="utf-8") as archivo:
            archivo.write(f"{prod}|{precio}|{cant}|{total}\n")
            
        messagebox.showinfo("Venta Registrada", "La venta se registró correctamente.")
        
        # Limpiar campos
        cb_producto.set("")
        txt_precio.config(state="normal"); txt_precio.delete(0, tk.END); txt_precio.config(state="readonly")
        txt_cantidad.delete(0, tk.END)
        txt_total.config(state="normal"); txt_total.delete(0, tk.END); txt_total.config(state="readonly")
        
    # ------------------------------------
    # CONTROLES VISUALES
    # ------------------------------------
    # Se usa un Frame para agrupar controles y centrar mejor
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
    
    # Evento para recalcular el total al cambiar la cantidad
    cantidad_var.trace_add("write", lambda *args: calcular_total())
    
    lbl_total = tk.Label(main_frame, text="Total:", font=("Arial", 12))
    lbl_total.pack(pady=5)
    txt_total = tk.Entry(main_frame, font=("Arial", 12), state="readonly", width=30)
    txt_total.pack(pady=5)
    
    # ------------------------------------
    # EVENTOS Y BOTÓN
    # ------------------------------------
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
# 🎨 FONDO: Fondo de la ventana principal a NEGRO (#000000)
ventana.configure(bg="#000000") 


# -------------------------
# LOGO 
# -------------------------
try:
    # Usa la ruta BASE_DIR para encontrar el logo, como lo tenías definido.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "ventas2025.png")
    
    imagen = Image.open(logo_path) 
    imagen = imagen.resize((250, 250)) # Tamaño recomendado
    img_logo = ImageTk.PhotoImage(imagen)

    # 🎨 CONFIGURACIÓN: Fondo de la etiqueta del logo a NEGRO
    lbl_logo = tk.Label(ventana, image=img_logo, bg="#000000") 
    lbl_logo.pack(pady=20)
    
    # 🌟 CORRECCIÓN CRÍTICA: Mantenemos la referencia del objeto PhotoImage
    lbl_logo.image = img_logo 
    
except Exception as e: 
    # 🎨 CONFIGURACIÓN: Fondo de la etiqueta sin logo a NEGRO y texto a blanco para contraste
    lbl_sin_logo = tk.Label(ventana, text="(Aquí va el logo del sistema)", font=("Arial", 14), bg="#000000", fg="white")
    lbl_sin_logo.pack(pady=40)
    # print(f"Error al cargar el logo: {e}") 


# -------------------------
# BOTONES PRINCIPALES
# -------------------------
estilo = ttk.Style()
# 🎨 CAMBIOS: Ancho uniforme y texto negro sobre fondo blanco
estilo.configure("TButton", 
                 font=("Arial", 12, "bold"), 
                 padding=10,
                 width=25, 
                 background="white", 
                 foreground="black", 
                 relief="flat") 

# Opcional: Estilo al pasar el ratón (hover)
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