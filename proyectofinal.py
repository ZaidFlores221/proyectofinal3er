#Proyecto Final
#submodulo
#Autor: Flores Padilla Ahmed Zaid
# Y Mendez Fiol Yocelin Guadalupe

import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox
from PIL import Image, ImageTk # Necesita instalar pillow: pip install pillow

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
        
        # Validar precio como número
        try:
            float(precio)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        # Guardar en archivo de texto (Usando la lógica de ruta BASE_DIR)
        try:
            # Obtiene la ruta del directorio base para guardar 'productos.txt' junto al script
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            archivo_path = os.path.join(BASE_DIR, "productos.txt")
            
            with open(archivo_path, "a", encoding="utf-8") as archivo:
                archivo.write(f"{id_prod}|{descripcion}|{precio}|{categoria}\n")
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
    messagebox.showinfo("Registro de Ventas", "Aquí irá el módulo de registro de ventas.")

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
# LOGO (Corregido el problema de referencia)
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
                 width=25,               # ✅ Ancho fijo para botones del mismo tamaño
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